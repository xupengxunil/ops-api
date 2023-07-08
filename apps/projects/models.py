from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from apps.users.models import UserProfile


class Company(models.Model):
    company_nickname = models.CharField(verbose_name='公司简称', max_length=30, db_index=True, unique=True)
    company_name = models.CharField(verbose_name='公司全称', max_length=30, db_index=True, unique=True)
    company_code = models.CharField(verbose_name='代号', max_length=30, db_index=True, unique=True)

    class Meta:
        verbose_name = "子公司"


class Group(models.Model):
    group_name = models.CharField(verbose_name='组名', max_length=30, db_index=True, unique=True)
    group_code = models.CharField(verbose_name='组code', max_length=30, db_index=True, unique=True)
    group_cn = models.ForeignKey(Company, verbose_name='子公司', on_delete=models.PROTECT, related_name='group')

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = "组名称"
        verbose_name_plural = verbose_name


class Project(models.Model):
    project_name = models.CharField(verbose_name='项目名称', max_length=30, db_index=True, unique=True)
    project_code = models.CharField(verbose_name='项目Code', max_length=30, db_index=True, null=False, unique=True)
    group = models.ForeignKey(Group, verbose_name='Group', on_delete=models.PROTECT, related_name='project')

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = "项目管理"
        verbose_name_plural = verbose_name


class Role(models.Model):
    role_name = models.CharField(verbose_name='角色名称', max_length=100, db_index=True, unique=True)
    role_code = models.CharField(verbose_name='角色Code', max_length=100, db_index=True, null=False, unique=True)
    description = models.CharField(verbose_name='描述', max_length=100, db_index=True, null=False)

    def __str__(self):
        return self.role_name

    class Meta:
        verbose_name = "项目角色"
        verbose_name_plural = verbose_name


class ProjectUser(models.Model):

    project = models.ForeignKey(Project, verbose_name='项目', on_delete=models.PROTECT, related_name='project_user')
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.PROTECT, related_name='project_user')
    role = models.ForeignKey(Role, verbose_name='角色', on_delete=models.PROTECT, related_name='project_user')

    def __str__(self):
        return self.project.project_name

    class Meta:
        verbose_name = "项目用户"
        verbose_name_plural = verbose_name
        unique_together = ('project', 'user', 'role')
