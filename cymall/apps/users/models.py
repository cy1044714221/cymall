from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    email_active = models.BooleanField(default=False, verbose_name='邮箱是否激活')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        db_table = 'cy_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Address(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    addressee = models.CharField(max_length=20, verbose_name='收件人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='详细地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'cy_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_date']
