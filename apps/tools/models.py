from django.db import models
from apps.users.models import UserProfile


# Create your models here.
class Todolist(models.Model):
    content = models.TextField(null=False)
    type = models.CharField(max_length=20, choices=[
        ('todo', 'todo'),
        ('idea', 'idea'),
        ('plan', 'plan')
    ])

    status = models.CharField(max_length=20, choices=[
        ('doing', 'doing'),
        ('done', 'done')
    ])

    user = models.ForeignKey(UserProfile, verbose_name='User', on_delete=models.PROTECT, related_name='todolist')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "备忘录"

