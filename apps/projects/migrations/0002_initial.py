# Generated by Django 4.0.6 on 2023-07-08 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_nickname', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='公司简称')),
                ('company_name', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='公司全称')),
                ('company_code', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='代号')),
            ],
            options={
                'verbose_name': '子公司',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='组名')),
                ('group_code', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='组code')),
                ('group_cn', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='group', to='projects.company', verbose_name='子公司')),
            ],
            options={
                'verbose_name': '组名称',
                'verbose_name_plural': '组名称',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='项目名称')),
                ('project_code', models.CharField(db_index=True, max_length=30, unique=True, verbose_name='项目Code')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='project', to='projects.group', verbose_name='Group')),
            ],
            options={
                'verbose_name': '项目管理',
                'verbose_name_plural': '项目管理',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='角色名称')),
                ('role_code', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='角色Code')),
                ('description', models.CharField(db_index=True, max_length=100, verbose_name='描述')),
            ],
            options={
                'verbose_name': '项目角色',
                'verbose_name_plural': '项目角色',
            },
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='project_user', to='projects.project', verbose_name='项目')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='project_user', to='projects.role', verbose_name='角色')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='project_user', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '项目用户',
                'verbose_name_plural': '项目用户',
                'unique_together': {('project', 'user', 'role')},
            },
        ),
    ]