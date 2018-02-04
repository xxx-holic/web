from django.conf.urls import url
from . import views
urlpatterns=[
    url('^register/$',views.register),
    url('^register_handle/$',views.register_handle),
    url('^register_uname/$',views.register_uname),
    url(r'^active/$',views.active),
    url('^login/$',views.login),
    url('^login_handle/$',views.login_handle),
    url('^info/$',views.info),
    url('^site/$',views.site),
    url('^site_add/$',views.site_add),
    url('^sheng/$',views.sheng),
    url('^logout/$',views.logout),
    url('^order/$',views.order),
]