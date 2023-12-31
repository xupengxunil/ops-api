# Generated by Django 4.0.6 on 2023-07-08 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_initial'),
        ('resource', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=100, unique=True)),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('operating_system', models.CharField(max_length=50)),
                ('cpu_cores', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('memory_size', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('disk_space', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('running', 'running'), ('stop', 'stop')], max_length=20)),
                ('app', models.CharField(default='app', max_length=100)),
                ('os_version', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('env', models.CharField(choices=[('test', 'test'), ('uat', 'uat'), ('dev', 'dev'), ('pprd', 'pprd'), ('prod', 'prod')], max_length=20)),
                ('deploy_username', models.CharField(default='', max_length=50, verbose_name='发布用户')),
                ('pkey', models.TextField(default='', null=True, verbose_name='私钥')),
                ('username', models.CharField(default='', max_length=50, verbose_name='用户')),
                ('root_password', models.TextField(default='', null=True, verbose_name='root加密密码')),
                ('monitor_port', models.CharField(blank=True, max_length=100, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project', to='projects.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': '主机名称',
                'verbose_name_plural': '主机名称',
            },
        ),
        migrations.CreateModel(
            name='NetTestHost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=100, unique=True)),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('tag', models.CharField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('pkey', models.TextField(blank=True, default='', null=True, verbose_name='私钥')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '网络测试主机',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('env', models.CharField(choices=[('test', 'test'), ('uat', 'uat'), ('dev', 'dev'), ('pprd', 'pprd'), ('prod', 'prod')], max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='config', to='projects.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': '配置管理',
            },
        ),
        migrations.CreateModel(
            name='HostUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=60, null=True, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=60, null=True, verbose_name='密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='resource.host', verbose_name='Host')),
            ],
            options={
                'verbose_name': '主机用户',
                'unique_together': {('username', 'host')},
            },
        ),
    ]
