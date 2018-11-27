from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^blog/', views.BlogIndex.as_view(), name = 'hc-blog')
]