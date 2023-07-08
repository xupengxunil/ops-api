# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.rsakey import RSAKey
from io import StringIO
import base64
import time
import re


class SSH:
    def __init__(self, hostname, port=22, username='root', pkey=None, password=None, connect_timeout=5):
        self.stdout = None
        self.client = None
        self.channel = None
        self.already_init = False
        self.eof = 'SHELL END 957321'
        self.regex = re.compile(r'SHELL END 957321 (-?\d+)[\r\n]?')
        self.arguments = {
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': password,
            'pkey': RSAKey.from_private_key(StringIO(pkey)) if isinstance(pkey, str) else pkey,
            'timeout': connect_timeout,
            'banner_timeout': 30
        }

    def run_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command,timeout=180)
        return stdout.readlines()

    def close(self):
        self.client.close()

    def get_client(self):
        if self.client is not None:
            return self.client
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy)
        self.client.connect(**self.arguments)
        return self.client

    def _handle_command(self, command):
        commands = ''
        commands += f'\necho {self.eof} $?\n'
        return commands

    def exec_command_raw(self, command):
        channel = self.client.get_transport().open_session()
        channel.set_combine_stderr(True)
        channel.settimeout(180)
        channel.exec_command(command)
        code, output = channel.recv_exit_status(), channel.recv(-1)
        return code, self._decode(output)

    def exec_command_with_stream(self, command):
        channel = self._get_channel()
        command = self._handle_command(command)
        channel.send(command,timeout=180)
        exit_code, line = -1, ''
        while True:
            line = self._decode(channel.recv(8196))
            if not line:
                break
            match = self.regex.search(line)
            if match:
                exit_code = int(match.group(1))
                line = line[:match.start()]
                break
            yield exit_code, line
        yield exit_code, line

    def _get_channel(self):
        if self.channel:
            return self.channel

        counter = 0
        self.channel = self.client.invoke_shell()
        command = 'set +o zle\nset -o no_nomatch\nexport PS1= && stty -echo\n'
        command += f'echo {self.eof} $?\n'
        self.channel.send(command.encode())
        while True:
            if self.channel.recv_ready():
                line = self._decode(self.channel.recv(8196))
                if self.regex.search(line):
                    self.stdout = self.channel.makefile('r')
                    break
            elif counter >= 100:
                self.client.close()
                raise Exception('Wait ssh response timeout')
            else:
                counter += 1
                time.sleep(0.1)
        return self.channel

    def _decode(self, content):
        try:
            content = content.decode()
        except UnicodeDecodeError:
            content = content.decode(encoding='GBK', errors='ignore')
        return content

    def get_transport(self):
        return self.client.get_transport()

    def __enter__(self):
        self.get_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.client = None
