# Generated by Django 4.0.6 on 2023-07-08 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='菜单名称')),
                ('url', models.CharField(blank=True, max_length=30, null=True, verbose_name='菜单路径')),
                ('parentId', models.CharField(db_index=True, max_length=10, verbose_name='父ID')),
                ('icon', models.CharField(blank=True, max_length=120, null=True, verbose_name='图标')),
                ('type', models.IntegerField(choices=[(1, '一级'), (2, '二级'), (3, '三级')], verbose_name='菜单类别')),
                ('sort', models.IntegerField(null=True, verbose_name='排序')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '菜单',
                'verbose_name_plural': '菜单',
            },
        ),
    ]
