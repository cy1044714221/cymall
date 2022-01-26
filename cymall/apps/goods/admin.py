from django.contrib import admin

# Register your models here.
from .models import SKU, SKUImage, Goods, Brand, GoodsCategory


@admin.register(GoodsCategory, )
class GoodsCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    list_display_links = ['id', 'name']
    list_editable = ['parent']
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = False
    list_filter = ['parent']
    search_fields = ['id', 'name', 'parent']
    autocomplete_fields = ['parent']
    # raw_id_fields = ("parent",)


@admin.register(Brand, )
class GoodsBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'logo']
    list_display_links = ['id', 'name', 'logo']
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = False
    search_fields = ['id', 'name']
    # autocomplete_fields = ['parlogoent']
    # raw_id_fields = ("parent",)


@admin.register(Goods, )
class GoodsSPUAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand', 'category1', 'category2', 'category3', 'sales', 'comments']
    list_display_links = ['id', 'name']
    list_editable = ['sales', 'comments']
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = False
    list_filter = ['brand', 'category1', ]
    search_fields = ['name', 'brand', 'category1', 'category2', 'category3', ]
    autocomplete_fields = ['brand', 'category1', 'category2', 'category3', ]
    # raw_id_fields = ("parent",)


@admin.register(SKU, )
class GoodsSKUAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'caption', 'goods', 'category', 'price', 'stock', 'sales', 'comments', 'is_launched',
                    ]
    list_display_links = ['id', 'name', ]
    list_editable = ['stock', 'sales', 'comments', 'is_launched', ]
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = False
    list_filter = ['category', 'is_launched', ]
    search_fields = ['name', 'caption', ]
    autocomplete_fields = ['goods', 'category', ]

    '''自定义actions'''
    actions = ['setup_is_launched']

    def setup_is_launched(self, request, queryset):
        queryset.update(is_launched=True)

    setup_is_launched.short_description = '上架所选的 商品SKU'


@admin.register(SKUImage, )
class GoodsSKUImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sku', 'image']
    list_display_links = ['id', 'sku', ]
    actions_on_top = False
    actions_on_bottom = False
