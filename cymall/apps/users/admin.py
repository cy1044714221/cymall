from django.contrib import admin
from .models import User, Address
from django.contrib.auth.models import Group, Permission

admin.site.site_header = 'CyMall 商城'
admin.site.site_title = 'CyMall 商城-登录系统后台'
admin.site.index_title = 'CyMall 商城-后台管理'





@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'mobile', 'email', 'is_staff', 'last_login', 'is_active',
                    'date_joined', 'email_active', 'default_address']

    list_editable = ('is_active', 'email_active',)

    list_display_links = ['id', 'username']

    list_max_show_all = 200  # default

    list_per_page = 25

    list_filter = ['is_active', 'email_active', 'is_staff']

    search_fields = ['username', 'mobile']

    fieldsets = (
        ('基本', {'fields': ('username', 'mobile', 'email', 'password',)}),
        ('高级', {'fields': (('date_joined', 'last_login'), ('is_active', 'email_active'), 'default_address')}),
    )

    '''自定义actions'''
    actions = ['setup_staff']

    def setup_staff(self, request, queryset):
        queryset.update(is_staff=True)

    setup_staff.short_description = '设为工作人员'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'addressee', 'province', 'city', 'district', 'place', 'mobile', 'is_deleted',
                    'create_date', 'update_date']
    list_display_links = ['id', 'addressee']
    fields = ('user', 'addressee', ('province', 'city', 'district'), 'place', 'mobile', 'is_deleted')
    actions_on_top = False
    actions_on_bottom = False
    search_fields = ['addressee', 'mobile', 'place']
    autocomplete_fields = ['province', 'city', 'district', ]
    # list_filter = ['is_deleted']

    actions_selection_counter = True
