from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'query/$', views.query, name='query'),
    # url(r'projects/$', views.projects, name='projects'),
    # url(r'files/(?P<project_name>\S+)/$', views.files, name='files'),
    # url(r'comments/(?P<project_name>\S+)/$', views.comments, name='files'),
    # url(r'logs/(?P<file_name>\S+)/$', views.logs, name='logs'),
    url(r'getfrac/$', views.getfrac, name='getfrac'),
# url(r'preview/$', views.preview, name='preview'),
]
