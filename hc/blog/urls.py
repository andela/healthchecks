from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
		r'(?P<post>[-\w]+)/$',
		views.post_detail,
		name='post_detail'),
	url (r'^categories/$',
        views.category_list,
        name='category_list'),
	url(r'^categories/(?P<slug>[-\w]+)/$',
        views.category_detail,
        name='category_detail'),
]
