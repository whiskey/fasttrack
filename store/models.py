from django.db import models


class MobileApp(models.Model):
    name = models.CharField(max_length=128,
                            help_text='The application name as it is seen on the device')
    description = models.TextField(null=True,
                                   help_text='A short description text to help users identifying the correct app')
    version = models.CharField(max_length=32, verbose_name='app version')

    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

