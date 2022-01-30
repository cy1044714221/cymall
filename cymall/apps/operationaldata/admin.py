from django.contrib import admin
from .models import State
from .views import stateboard


# Register your models here.

@admin.register(State, )
class StateAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_content=None):  # 改写方法 返回自定义的数据页面
        return stateboard(request)

