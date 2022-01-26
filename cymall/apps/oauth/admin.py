from django.contrib import admin

# Register your models here.
from .models import OAuthQQUser


@admin.register(OAuthQQUser, )
class OAuthQQUserAdmin(admin.ModelAdmin):
    pass
