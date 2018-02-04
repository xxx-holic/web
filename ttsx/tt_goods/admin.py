from django.contrib import admin
from .models import *
# Register your models here.
class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id','gtitle','gprice','gkucun','gtype']
    list_filter = ['gtype']
    search_fields = ['gtitle','gjianjie','gcontent']


admin.site.register(TypeInfo)
admin.site.register(GoodsInfo,GoodsInfoAdmin)
