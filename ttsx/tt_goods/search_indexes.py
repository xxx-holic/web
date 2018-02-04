#coding=utf-8
from haystack import indexes
from .models import GoodsInfo
#指定对于某个表的某些数据建立索引
class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    gclick = indexes.IntegerField(model_attr='gclick')
    gprice=indexes.FloatField(model_attr='gprice')
    #指定数据来源的表
    def get_model(self):
        return GoodsInfo
    #指定数据来源的行
    def index_queryset(self, using=None):
        return self.get_model().objects.all()