from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^[0-9]+$', views.form, name='index'),
    url(r'^parts$', views.parts, name='parts'),
]