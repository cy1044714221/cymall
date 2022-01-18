from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    phone_num = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    email_active = models.BooleanField(default=False, verbose_name='邮箱是否激活')

    class Meta:
        db_table = 'cy_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
