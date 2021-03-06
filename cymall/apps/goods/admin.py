from django.contrib import admin
from .models import SKU, SKUImage, Goods, Brand, GoodsCategory
from django.utils.html import format_html

class SKUInline(admin.TabularInline):
    model = SKU
    fk_name = 'goods'
    extra = 3


class SKUImageInline(admin.TabularInline):
    model = SKUImage
    fk_name = 'sku'
    extra = 3


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


@admin.register(Brand, )
class GoodsBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'logo_image', 'name', 'logo']
    list_display_links = ['id', 'name', 'logo']
    list_per_page = 5
    actions_on_top = False
    actions_on_bottom = False
    search_fields = ['id', 'name']


    def logo_image(self, obj):
        return format_html('<img src="%s" height="50" />' % obj.logo.url)

@admin.register(Goods, )
class GoodsSPUAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand', 'category1', 'category2', 'category3', 'sales', 'comments', ]
    list_display_links = ['id', 'name']
    list_editable = ['sales', 'comments']
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = False
    list_filter = ['brand', 'category1', ]
    search_fields = ['name', 'brand', 'category1', 'category2', 'category3', ]
    autocomplete_fields = ['brand', 'category1', 'category2', 'category3', ]

    inlines = [SKUInline]


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

    '''?????????actions'''
    actions = ['setup_is_launched']

    def setup_is_launched(self, request, queryset):
        queryset.update(is_launched=True)

    setup_is_launched.short_description = '??????????????? ??????SKU'
    inlines = [SKUImageInline]


@admin.register(SKUImage, )
class GoodsSKUImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_dispaly', 'sku', 'image', ]
    list_display_links = ['id', 'sku', ]

    actions_on_top = False
    actions_on_bottom = False

    # ??????????????????skuimage??????
    def image_dispaly(self, obj):
        return format_html('<img src="%s" height="80" />' % obj.image.url)