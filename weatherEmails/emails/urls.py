from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.SubscribeView.as_view(), name='subscribe'),
    url(r'^success/$', views.SuccessView.as_view(), name='success'),
]
