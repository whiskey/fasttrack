from django.conf.urls import url

from . import views

app_name = 'store'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^app/(?P<app_id>[0-9]+)$', views.detail, name='detail'),
]