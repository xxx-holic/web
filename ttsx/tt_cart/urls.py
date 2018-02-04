from django.conf.urls import url
from . import views
urlpatterns=[
    url('^add/$',views.add),
    url('^$',views.index),
    url('^del/$',views.delete),
    url('^set/$',views.set),
    url('^get_count/$',views.get_count),
]