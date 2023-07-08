from django.db import models

# Create your models here.
from django.db import models
from apps.projects.models import Project
from libs.ssh import SSH
from settings.utils import AppSetting


class Host(models.Model):
    # 主机名
    hostname = models.CharField(max_length=100, unique=True)
    # IP 地址
    ip_address = models.GenericIPAddressField(unique=True)
    # 操作系统
    operating_system = models.CharField(max_length=50)
    # CPU 核心数
    cpu_cores = models.PositiveIntegerField(null=True,blank=True,default=0)
    # 内存大小
    memory_size = models.PositiveIntegerField(null=True,blank=True,default=0)
    # 磁盘空间
    disk_space = models.PositiveIntegerField(null=True,blank=True,default=0)
    # 项目ID
    # project = models.CharField(max_length=100)
    project = models.ForeignKey(Project, verbose_name='Project', on_delete=models.SET_NULL, related_name='project',
                                null=True)
    # project_fk = models.ForeignKey(Project, verbose_name='Project', on_delete=models.SET_NULL, related_name='project',
    #                                null=True)
    # 主机描述
    description = models.TextField(blank=True, null=True)
    # 主机状态
    status = models.CharField(max_length=20, choices=[
        ('running', 'running'),
        ('stop', 'stop')
    ])
    app = models.CharField(max_length=100,default='app')
    os_version = models.CharField(null=True,blank=True,max_length=100,default='')
    env = models.CharField(max_length=20, choices=[
        ('test', 'test'),
        ('uat', 'uat'),
        ('dev', 'dev'),
        ('pprd', 'pprd'),
        ('prod', 'prod')
    ])
    deploy_username = models.CharField(max_length=50,verbose_name="发布用户",default='')
    pkey = models.TextField(null=True,verbose_name="私钥",default='')
    username = models.CharField(max_length=50,verbose_name="用户",default='')
    root_password = models.TextField(null=True,verbose_name="root加密密码",default='')
    monitor_port = models.CharField(max_length=100,blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.hostname

    @property
    def private_key(self):
        return self.pkey or AppSetting.get('private_key')

    def get_username(self):
        return self.username or 'root'

    def get_deploy_username(self):
        return self.deploy_username or 'root'

    def get_ssh(self, pkey=None):
        pkey = pkey or self.private_key
        return SSH(self.hostname, self.port, self.get_username, pkey)

    class Meta:
        verbose_name = "主机名称"
        verbose_name_plural = verbose_name

class HostUser(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=60, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=60, null=True, blank=True)
    host = models.ForeignKey(Host, verbose_name='Host', on_delete=models.CASCADE, related_name='users',
                                null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "主机用户"
        unique_together=("username","host")

class Config(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    env = models.CharField(max_length=20, choices=[
        ('test', 'test'),
        ('uat', 'uat'),
        ('dev', 'dev'),
        ('pprd', 'pprd'),
        ('prod', 'prod')
    ])

    project = models.ForeignKey(Project, verbose_name='Project', on_delete=models.SET_NULL, related_name='config',
                                null=True)

    # 主机描述
    description = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "配置管理"