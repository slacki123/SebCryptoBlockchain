import os
import sys
from threading import Thread

from flask import Flask

from backend.pubsub import PubSub


class LocalTunnelAppRunner:

    def __init__(self, app: Flask, port: int, pubsub: PubSub):
        self.app = app
        self.port = port
        self.pubsub = pubsub

    def run_app(self):
        self.app.run(port=self.port)

    @staticmethod
    def run_lt(port):
        """
        This method runs the localtunnel command from within python
        """
        if os.path.isfile('/usr/local/bin/lt'):
            print("localtunnel is alreadty installed.")
        else:
            os.system('sudo npm install -g localtunnel')
        os.system(f'lt -p {port}')

    def run_local_tunnel_on_separate_thread(self):
        thread = Thread(target=self.run_lt, args=(self.port,))
        # thread.setDaemon(True)
        thread.start()

        # Try to get the logs here somehow
