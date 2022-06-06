import os
import time
from threading import Thread
from requests import get

from flask import Flask


class LocalTunnelAppRunner:

    def __init__(self, app: Flask, port: int):
        self.app = app
        self.port = port
        self.ip_address = get('https://api.ipify.org').content.decode('utf8')
        print(f'My ip: {self.ip_address}')
        self.tunnel_subdomain = f"{self.ip_address.replace('.', '-')}-{port}"
        self.tunnel_url = f'https://{self.tunnel_subdomain}.loca.lt'

    def run_app(self):
        self.app.run(port=self.port)

    def run_lt(self, port):
        """
        This method runs the localtunnel command from within python
        """
        if os.path.isfile('/usr/local/bin/lt'):
            print("localtunnel is alreadty installed.")
        else:
            os.system('sudo npm install -g localtunnel')

        # Get the IP address and port to be used as subdomain, horrendous hack
        os.system(f'lt -p {port} -s {self.tunnel_subdomain}')

    def run_local_tunnel_on_separate_thread(self):
        thread = Thread(target=self.run_lt, args=(self.port,))
        # thread.setDaemon(True)
        thread.start()
        time.sleep(3)

