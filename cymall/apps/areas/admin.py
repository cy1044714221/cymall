from django.contrib import admin

# Register your models here.
from .models import Area


class AreaAdmin(admin.ModelAdmin):
    list_display = ["id", "name", 'parent_area']

    list_per_page = 10

    actions_on_top = False

    actions_on_bottom = False

    search_fields = ['id', 'name', ]

    # fieldsets = (
    #     ('基本', {'fields': ('name',)}),
    #     ('高级', {'fields': ('parent',)}),
    # )
    autocomplete_fields = ['parent']


# 注册Model类
admin.site.register(Area, AreaAdmin)
