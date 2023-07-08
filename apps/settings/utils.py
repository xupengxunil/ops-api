from functools import lru_cache
from apps.settings.models import Setting
from libs.ssh import SSH
import json


class AppSetting:

    @classmethod
    def get(cls, key):
        set = Setting.objects.filter(key=key).first()
        if not set:
            raise KeyError(f'no such key for {key!r}')
        return json.loads(set.value)

    @classmethod
    def set(cls, key, value, desc=None):
        value = json.dumps(value)
        Setting.objects.update_or_create(key=key, value=value)

    @classmethod
    def get_ssh_key(cls):
        return cls.get('private_key')
