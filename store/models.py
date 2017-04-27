from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class MobileApp(models.Model):
    APPLICATION_PLATFORM = (
        ('0', 'iOS'),
        ('1', 'Android')
    )

    name = models.CharField(max_length=128,
                            help_text='The application name as it is seen on the device')
    description = models.TextField(blank=True, null=True,
                                   help_text='A short description text to help users identifying the correct app')
    version = models.CharField(max_length=32, verbose_name='app version')

    # currently one app per platform - might change later!
    app_platform = models.CharField(max_length=1, choices=APPLICATION_PLATFORM, default='0')
    # FIXME: join uploads root with app id
    app_binary = models.FileField(upload_to='binaries', verbose_name='Application Binary',
                                  help_text='This should have the following file extensions: ' +
                                            '<code>.ipa</code> for iOS and <code>.apk</code> for Android apps')
    app_icon = models.ImageField(upload_to='icons', verbose_name='Icon',
                                 help_text='An application icon. Recommended size 512x512px')
    app_manifest = models.FileField(upload_to='manifests', blank=True, null=True, verbose_name='Manifest',
                                    help_text='[Optional] field for iOS manifest files (<code>.plist</code>)')

    last_modified = models.DateTimeField(auto_now=True)

    @property
    def normalized_name(self):
        return self.name.replace(' ', '_').lower()

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(MobileApp, self).save(*args, **kwargs)
        # create permission to view/load this app
        apps_group, created = Group.objects.get_or_create(name='apps')
        # Code to add permission to group ???
        ct = ContentType.objects.get_for_model(MobileApp)

        # Now what - Say I want to add 'Can add project' permission to new_group?
        permission = Permission.objects.create(codename='can_access_{}'.format(self.normalized_name),
                                               name='Can access {}'.format(self.normalized_name),
                                               content_type=ct)
        apps_group.permissions.add(permission)

    class Meta:
        ordering = ['name']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'


@receiver(pre_delete, sender=MobileApp)
def _app_delete(sender, instance, **kwargs):
    perm = Permission.objects.filter(codename='can_access_{}'.format(instance.normalized_name))
    perm.delete()
