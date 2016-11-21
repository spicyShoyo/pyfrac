from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'query/$', views.query, name='query'),

    url(r'saved/$', views.saved, name='saveed'),

    url(r'addimg/$', views.addimg, name='addimg'),

    url(r'getfrac/$', views.getfrac, name='getfrac'),

    url(r'noise/$', views.noise, name='noise'),

    url(r'getnoi/$', views.getnoise, name='getnoi'),

    url(r'signin/$', views.signin, name='signin'),
    url(r'imgset/$', views.imgset, name='imgset'),
]
