# from pubnub.pubnub import PubNub

# pubnub = PubNub(
#     publish_key = "pub-c-5c55f43d-58e1-4070-97d2-a10bab46b15a",
#     subscribe_key = "sub-c-027e18e2-59d5-11ea-b226-5aef0d0da10f")
# channel = "iot-channel"

# def callback(message, channel):
#     print('[' + channel + ']: ' + str(message))


# pubnub.subscribe(
#     channel,
#     callback = callback)


from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-920d39c8-ea66-4650-9eca-a2e9fd8ffc78'
pnconfig.publish_key = 'pub-c-5c55f43d-58e1-4070-97d2-a10bab46b15a'
pnconfig.user_id = "Raghul-device"
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        print("success")
        pass  # Message successfully published to specified channel.
    else:
        print(status)
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        print("presence")
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            print("PNUnexpectedDisconnectCategory")
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            print("PNConnectedCategory")

            pubnub.publish().channel('iot-channel').message('Hello world!').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            print("PNReconnectedCategory")
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            print("PNDecryptionErrorCategory")
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('iot-channel').execute()