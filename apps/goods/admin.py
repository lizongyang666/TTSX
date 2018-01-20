from django.contrib import admin
from .models import GoodsCategory, Goods, GoodsSKU, IndexCategoryGoodsBanner
from .models import IndexGoodsBanner, IndexPromotionBanner, GoodsImage


# Register your models here.

admin.site.register(GoodsCategory)
admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexCategoryGoodsBanner)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexPromotionBanner)
