from django.db import models

Types = (
    (1, u'一级'),
    (2, u'二级'),
    (3, u'三级'),
)


# Create your models here.

class Menu(models.Model):
    name = models.CharField(verbose_name='菜单名称', max_length=30, null=False)
    url = models.CharField(verbose_name='菜单路径', max_length=30, null=True, blank=True)
    parentId = models.CharField(verbose_name='父ID', max_length=10, db_index=True)
    icon = models.CharField(verbose_name='图标', max_length=120, null=True, blank=True)
    type = models.IntegerField(verbose_name='菜单类别', choices=Types, null=False)
    sort = models.IntegerField(verbose_name='排序', null=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "菜单"
        verbose_name_plural = verbose_name
