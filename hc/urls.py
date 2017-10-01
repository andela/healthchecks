from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('hc.accounts.urls')),
    url(r'^', include('hc.api.urls')),
    url(r'^blog/', include('hc.blog.urls',
    					   namespace='blog',
    					   app_name='blog')),
    url(r'^', include('hc.front.urls')),
    url(r'^', include('hc.payments.urls'))
]
