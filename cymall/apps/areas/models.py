from django.db import models


# Create your models here.
class Area(models.Model):
    """行政区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上级行政区', related_name='subs')

    class Meta:
        db_table = 'cy_areas'
        verbose_name = '行政区'
        verbose_name_plural = '行政区'

    def __str__(self):
        return self.name
