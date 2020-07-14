from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
    url(r'^api/listing$', views.listing_list),
    url(r'^api/listing/(?P<pk>[0-9]+)$', views.listing_detail),
    url(r'^api/listing/published$', views.listing_list_published)
]