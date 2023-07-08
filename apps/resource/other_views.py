import math

from rest_framework.views import APIView
from rest_framework import status
from common.customresponse import CustomResponse
from apps.resource.models import Host
from apps.projects.models import Project
from libs.ssh import SSH


def fetch_host_extend(ssh):
    response = {'disk': []}
    with ssh:
        code, out = ssh.exec_command_raw('nproc')
        if code != 0:
            code, out = ssh.exec_command_raw("grep -c 'model name' /proc/cpuinfo")
        if code == 0:
            response['cpu'] = int(out.strip())

        code, out = ssh.exec_command_raw("cat /etc/os-release | grep PRETTY_NAME | awk -F \\\" '{print $2}'")
        if '/etc/os-release' in out:
            code, out = ssh.exec_command_raw("cat /etc/issue | head -1 | awk '{print $1,$2,$3}'")
        if code == 0:
            response['os_name'] = out.strip()[:50]

        code, out = ssh.exec_command_raw('lsblk -dbn -o SIZE -e 11 2> /dev/null')
        if code == 0:
            disks = []
            disk_size = 0
            for item in out.strip().splitlines():
                item = item.strip()
                size = math.ceil(int(item) / 1024 / 1024 / 1024)
                if size > 10:
                    disks.append(size)
            for i in disks:
                disk_size += i
            response['disk'] = disk_size

        code, out = ssh.exec_command_raw("dmidecode -t 17 | grep -E 'Size: [0-9]+' | awk '{s+=$2} END {print s,$3}'")
        if code == 0:
            fields = out.strip().split()
            if len(fields) == 2 and fields[1] in ('GB', 'MB'):
                size, unit = out.strip().split()
                if unit == 'GB':
                    response['memory'] = size
                else:
                    response['memory'] = round(int(size) / 1024, 0)
        if 'memory' not in response:
            code, out = ssh.exec_command_raw("free -m | awk 'NR==2{print $2}'")
            if code == 0:
                response['memory'] = math.ceil(int(out) / 1024)
        return response


class OsInfoView(APIView):

    def get(self, request):
        if request.query_params['id']:
            host_id = int(request.query_params['id'])
            host = Host.objects.filter(pk=host_id).first()
            host_ip = host.ip_address
            host_pkey = host.private_key
            host_username = host.get_username()
        else:
            return CustomResponse(data={}, code=200, msg="No id request.", status=status.HTTP_200_OK)

        ssh = SSH(host_ip, '22', host_username, host_pkey)
        form = fetch_host_extend(ssh)

        host = Host.objects.filter(pk=host_id).first()
        host.os_version = form['os_name']
        host.disk_space = form['disk']
        host.cpu_cores = form['cpu']
        host.memory_size = int(form['memory'])
        host.save()

        return CustomResponse(data={}, code=200, msg="OK", status=status.HTTP_200_OK)


class DeployHostView(APIView):

    def get(self, request):
        if 'project' in request.query_params and 'env' in request.query_params:
            env = request.query_params['env']
            project_id = int(request.query_params['project'])
            project_host = Host.objects.filter(project=project_id, env=env)
            ops_project_id = Project.objects.filter(project_code='ops-deploy').first().id
            ops_deploy_host = Host.objects.filter(project=ops_project_id,env=env)
        else:
            return CustomResponse(data={}, code=200, msg="No id request.", status=status.HTTP_200_OK)

        deploy_host = []

        for host in project_host:
            host_dict = {}
            host_dict['ip'] = host.ip_address
            host_dict['name'] = host.hostname
            host_dict['id'] = host.id
            deploy_host.append(host_dict)

        for host in ops_deploy_host:
            host_dict = {}
            host_dict['ip'] = host.ip_address
            host_dict['name'] = host.hostname
            host_dict['id'] = host.id
            deploy_host.append(host_dict)

        return CustomResponse(data=deploy_host, code=200, msg="OK", status=status.HTTP_200_OK)
