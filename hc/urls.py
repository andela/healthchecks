# These are for a previous version of django

# from django.conf.urls import include, url
# from django.contrib import admin

# Using more recent import calls from latest django
# from django.urls import include
from django.conf.urls import url, include
# from django.urls import path
from django.contrib import admin

urlpatterns = [
    # We shall use newer methods from django framework to route our apps

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('hc.accounts.urls')),
    url(r'^', include('hc.api.urls')),
    url(r'^', include('hc.front.urls')),
    url(r'^', include('hc.payments.urls'))

    # path("accounts/", include("hc.accounts.urls")),
    # path("", include("hc.api.urls")),
    # path("", include("hc.front.urls")),
    # path("", include("hc.payments.urls")),
    # path("admin/", admin.site.urls),
]
