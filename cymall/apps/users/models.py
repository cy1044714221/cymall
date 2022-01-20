from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    email_active = models.BooleanField(default=False, verbose_name='邮箱是否激活')

    class Meta:
        db_table = 'cy_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
