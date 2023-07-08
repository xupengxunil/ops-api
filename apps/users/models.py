from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.menu.models import Menu



# Create your models here.
from apps.menu.serializers import MenuSerializer


class Role(models.Model):
    """
    角色
    """

    name = models.CharField(max_length=30, null=False, verbose_name="角色名")
    isSupper = models.BooleanField(verbose_name="是否超级管理员", default=0)
    menulist = models.CharField(max_length=150, null=True, verbose_name="菜单列表")
    desc = models.CharField(max_length=30, null=False, verbose_name="角色描述")

    class Meta:
        verbose_name = "role"

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    """
    用户
    """

    GENDER = (
        ('male', u'男'),
        ('female', u'女'),
    )

    name = models.CharField(max_length=30, null=False, verbose_name="中文名")
    birthday = models.DateTimeField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER, null=True, blank=True, verbose_name="性别")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    role = models.ForeignKey(Role, verbose_name='用户Role',on_delete=models.SET_NULL,related_name='user_role',null=True)

    class Meta:
        verbose_name = "user"

    def __str__(self):
        return self.name

    def has_perms(self,codes):
        if self.is_superuser:
            return True
        menuId = self.role.menulist.split(',')
        menuList = Menu.objects.filter(id__in=menuId).all().order_by('sort')
        menuList = MenuSerializer(menuList, many=True).data

        for menu in menuList:
            if menu['url'] == codes[0]:
                return True
        return False


# class UserRole(models.Model):
#     """
#     用户角色映射
#     """
#     role = models.ForeignKey(Role, verbose_name='用户ID', on_delete=models.CASCADE, related_name='user_role')
