# from pubnub import Pubnub

# pubnub = Pubnub(
#     publish_key = "pub-c-a4f70ce4-33a4-4d97-b2d7-49e039342f0e",
#     subscribe_key = "sub-c-4269c980-54a6-11ea-80a4-42690e175160")

# channel = "my_channel"
# message = "A message"

# pubnub.publish(
#     channel = channel,
#     message = "A message")


from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


ENTRY = "Earth"
CHANNEL = "iot-channel"
the_update = None

        pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-920d39c8-ea66-4650-9eca-a2e9fd8ffc78'
pnconfig.publish_key = 'pub-c-5c55f43d-58e1-4070-97d2-a10bab46b15a'
pnconfig.user_id = "Raghul-device"
pubnub = PubNub(pnconfig)

print("*****************************************")
print("* Submit updates to The Guide for Earth *")
print("*     Enter 42 to exit this process     *")
print("*****************************************")

while the_update != "42":
    the_update = input("Enter an update for Earth: ")
    the_message = {"entry": ENTRY, "update": the_update}
    envelope = pubnub.publish().channel(CHANNEL).message(the_message).sync()

    if envelope.status.is_error():
        print("[PUBLISH: fail]")
        print("error: %s" % envelope.status.error)
    else:
        print("[PUBLISH: sent]")
        print("timetoken: %s" % envelope.result.timetoken)