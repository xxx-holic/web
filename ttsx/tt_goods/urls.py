from django.conf.urls import url
from . import views
urlpatterns=[
    url('^$',views.index),
    url(r'^list(\d+)/(\d+)/([1-4])/$',views.list),
    url(r'^(\d+)/$',views.detail),
    url(r'^search/$', views.MySearchView.as_view(), name='search_view'),
]
