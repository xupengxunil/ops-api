# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from common.customresponse import CustomResponse
from apps.resource.models import Host
from django.db.models import Sum

class DataView(APIView):

    def get(self, request, format=None):
        res = []
        host_all = Host.objects.count()
        host_prod = Host.objects.filter(env='prod').count()
        host_noprod = Host.objects.exclude(env='prod').count()
        cpu_all = Host.objects.aggregate(Sum('cpu_cores'))['cpu_cores__sum']
        cpu_prod = Host.objects.filter(env='prod').aggregate(Sum('cpu_cores'))['cpu_cores__sum']
        cpu_noprod = Host.objects.exclude(env='prod').aggregate(Sum('cpu_cores'))['cpu_cores__sum']
        mem_all = Host.objects.aggregate(Sum('memory_size'))['memory_size__sum']
        mem_prod = Host.objects.filter(env='prod').aggregate(Sum('memory_size'))['memory_size__sum']
        mem_noprod = Host.objects.exclude(env='prod').aggregate(Sum('memory_size'))['memory_size__sum']

        disk_all = Host.objects.aggregate(Sum('disk_space'))['disk_space__sum']
        disk_prod = Host.objects.filter(env='prod').aggregate(Sum('disk_space'))['disk_space__sum']
        disk_noprod = Host.objects.exclude(env='prod').aggregate(Sum('disk_space'))['disk_space__sum']


        host = {
            'title': '主机',
            'unit': '台',
            'color': 'success',
            'total': host_all,
            'prod': host_prod,
            'noprod': host_noprod
        }

        cpu = {
            'title': 'CPU',
            'unit': '核',
            'color': 'success',
            'total': cpu_all,
            'prod': cpu_prod,
            'noprod': cpu_noprod
        }

        mem = {
            'title': '内存',
            'unit': 'GB',
            'color': 'success',
            'total': mem_all,
            'prod': mem_prod,
            'noprod': mem_noprod
        }

        disk = {
            'title': '磁盘',
            'unit': 'GB',
            'color': 'success',
            'total': disk_all,
            'prod': disk_prod,
            'noprod': disk_noprod
        }

        res.append(host)
        res.append(cpu)
        res.append(mem)
        res.append(disk)


        return CustomResponse(data=res, code=200, msg="OK", status=status.HTTP_200_OK)