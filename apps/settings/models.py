# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from django.db import models
from libs.mixins import ModelMixin
import json

class Setting(models.Model, ModelMixin):
    key = models.CharField(max_length=50, unique=True)
    value = models.TextField()
    desc = models.CharField(max_length=255, null=True,blank=True)

    def __repr__(self):
        return '<Setting %r>' % self.key


    class Meta:
        verbose_name = "系统配置"