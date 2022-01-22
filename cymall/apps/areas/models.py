from django.db import models


# Create your models here.
class Area(models.Model):
    """行政区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上级行政区',
                               related_name='subs')

    class Meta:
        db_table = 'cy_areas'
        verbose_name = '行政区'
        verbose_name_plural = '行政区'

    def __str__(self):
        return self.name

    def parent_area(self):
        """返回父级区域名"""
        if self.parent is None:
            return ' - - '

        return self.parent.name

    # 指定方法列显示的名称
    parent_area.short_description = '父级区域'

    # 方法列默认不能排序，需要指定方法列按id进行排序
    # parent_area.admin_order_field = 'id'

