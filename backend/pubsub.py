import time

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback


pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-621045a8-98b3-4c06-99a4-15c81cb782d8"
pnconfig.subscribe_key = "sub-c-41462c63-86a5-41c4-9f8d-f1829ebbae27"
pnconfig.uuid = "someuuidblablablabaoier235digfj"
pubnub = PubNub(pnconfig)

TEST_CHANNEL = 'TEST_CHANNEL'

pubnub.subscribe().channels([TEST_CHANNEL]).execute()


class Listener(SubscribeCallback):
    def message(self, pubnub, message_object):
        print(f'\n--Incoming message object: {message_object}')


pubnub.add_listener(Listener())


def main():
    time.sleep(1)
    pubnub.publish().channel(TEST_CHANNEL).message({'foo': 'bar'}).sync()


if __name__ == '__main__':
    main()

