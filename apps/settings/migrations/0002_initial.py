# Generated by Django 4.0.6 on 2023-07-08 07:25

from django.db import migrations, models
import libs.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, unique=True)),
                ('value', models.TextField()),
                ('desc', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': '系统配置',
            },
            bases=(models.Model, libs.mixins.ModelMixin),
        ),
    ]
