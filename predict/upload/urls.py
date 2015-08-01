from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.form, name='index'),
    url(r'^file$', views.upload, name='upload'),
    url(r'^post', views.auto_post, name='auto_post'),
    url(r'^success', views.success, name='success'),
]