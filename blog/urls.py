from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^blog/$", views.index, name="blog-index"),
    url(r'^blog/([\d]+)$', views.blog_body, name="blog_body"),
]
