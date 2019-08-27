from channels.generic.websocket import AsyncWebsocketConsumer
import asyncssh
import json
import sys
import asyncio
from django.conf import settings
from .common import decrypt_string


private_key_dir = settings.BASE_DIR + '/private_keys/'


class MySSHClientSession(asyncssh.SSHClientSession):
    def __init__(self, consumer):
        self.consumer = consumer

    def data_received(self, data, datatype):
        # async_to_sync(self.consumer.send)(data)
        asyncio.ensure_future(self.consumer.send(data))

    def connection_lost(self, exc):
        if exc:
            print('SSH session error: ' + str(exc), file=sys.stderr)


class MyWsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.host = None
        self.port = None
        self.username = None
        self.passwd = None
        self.private_key = None
        self.sshchannel = None
        self.sshconnection = None

    async def disconnect(self, close_code):
        self.sshchannel.close()
        self.sshconnection.close()
        self.sshchannel = None
        self.sshconnection = None

    async def receive(self, text_data=None, bytes_data=None):
        if self.sshchannel is None:

            hostinfo = json.loads(text_data)
            print(hostinfo)
            await self.send('checking login info...\r\n')
            self.host = hostinfo.get('host')
            try:
                self.port = int(hostinfo.get('port'))
            except Exception:
                await self.send('\rCheck Login Info Error, Please try it again\r\n')
            self.username = decrypt_string(hostinfo.get('username'))
            self.passwd = decrypt_string(hostinfo.get('passwd'))
            self.private_key = hostinfo.get('private_key') if hostinfo.get('private_key') else None

            await self.send('\rconnecting\r\n')
            if self.private_key:
                try:
                    self.sshconnection = await asyncssh.connect(self.host,
                                                                self.port,
                                                                username=self.username,
                                                                client_keys=[private_key_dir + self.private_key],
                                                                known_hosts=None)
                except Exception:
                    await self.send('\rLogging key Error. Please check your Private Key\r\n')
            else:
                try:
                    self.sshconnection = await asyncssh.connect(self.host, self.port,
                                                                username=self.username,
                                                                password=self.passwd,
                                                                known_hosts=None)
                except Exception:
                    await self.send('\rLogin Info Error\r\n')
            self.sshchannel, _ = await self.sshconnection.create_session(lambda: MySSHClientSession(self),
                                                                         term_type='xterm', term_size=(150, 40))
            # self.sshchannel, _ = await self.sshconnection.create_session(lambda:MySSHClientSession(self), term_type='xterm')
            await self.send('\rConnected....\r\n')
        else:
            self.sshchannel.write(text_data)

    async def reply(self, message):
        text_data = message.get('text_data')
        bytes_data = message.get('bytes_data')
        await self.send(text_data=text_data, bytes_data=bytes_data)
