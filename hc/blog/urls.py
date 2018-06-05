from django.conf.urls import url
from hc.blog import views


urlpatterns = [
    url(r'^blog/$', views.all_blogs, name='blog-list'),
]
