import RPi.GPIO as GPIO
import time
import json
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import subprocess



CHANNEL = "iot-demo"
subscribe_key = "sub-c-920d39c8-ea66-4650-9eca-a2e9fd8ffc78"
publish_key = "pub-c-5c55f43d-58e1-4070-97d2-a10bab46b15a"
pnconfig = PNConfiguration()
pnconfig.subscribe_key = subscribe_key
pnconfig.publish_key = publish_key
pnconfig.user_id = "IOT-Session"
pubnub = PubNub(pnconfig)


#Display config starts
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()
#Display config ends

#GPIO config starts
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_DHT = 23

GPIO_BUZZER = 25
GPIO_LIGHT = 24
GPIO_RELAY = 16
 
#set GPIO direction (IN / OUT)
# GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_BUZZER,GPIO.OUT)
GPIO.setup(GPIO_LIGHT,GPIO.OUT)
GPIO.setup(GPIO_RELAY,GPIO.OUT)
# GPIO.setup(GPIO_PUSH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(GPIO_ECHO, GPIO.IN)

#GPIO config ends
def initiatePush():
    flag = False
    while True: # Run forever            
        if GPIO.input(GPIO_PUSH) == GPIO.HIGH:
            if flag == True:
                flag = False
                GPIO.setup(GPIO_BUZZER, GPIO.HIGH)
                print("Button was pushed! True")
            else:
                flag = True
                GPIO.setup(GPIO_BUZZER, GPIO.LOW)
                print("Button was pushed! False")
        time.sleep(0.5)

def GpioToggle(GPIONumber, flag):
    print(GPIONumber)
    if (flag == True):
        GPIO.output(GPIONumber,GPIO.HIGH)
    else:
        GPIO.output(GPIONumber,GPIO.LOW)


def displayLine1(text):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), text,  font=font, fill=255)
    disp.image(image)
    disp.display()

def displayLine2(text):
    draw.text((x, top+10), text,  font=font, fill=255)
    disp.image(image)
    disp.display()

def clearText():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.image(image)
    disp.display()

def getTempHum():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO_DHT)
    pDict = dict();
    cDict = dict();
    pDict['event'] = "sensor"
    cDict['temp'] = temperature
    cDict['hum'] = humidity
    pDict['data'] = cDict
    json_object = json.dumps(pDict, indent = 4)
    return json_object

def publishMessage(message):
    envelope = pubnub.publish().channel(CHANNEL).message(message).sync()
    if envelope.status.is_error():
        print("[PUBLISH: fail]")
        print("error: %s" % envelope.status.error)
    else:
        print("[PUBLISH: sent]")
        print("timetoken: %s" % envelope.result.timetoken)

def subscribedMessages(message):
    print(message)
    if is_json(message):
        jsonData = json.loads(message)
        if jsonData["event"] == "buzzer":
            GpioToggle(GPIO_BUZZER, jsonData["data"])
        elif jsonData["event"] == "light":
            GpioToggle(GPIO_LIGHT, jsonData["data"])
        elif jsonData["event"] == "display":
            displayLine1(jsonData["data"])
        elif jsonData["event"] == "relay":
            GpioToggle(GPIO_RELAY, jsonData["data"])
        elif jsonData["event"] == "sensor-reload":
            data = getTempHum()
            publishMessage(data)

    else:
        print('Not a valid message data => """' + message + '"""')
    # displayLine2(message)

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError:
    return False
  return True


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

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        subscribedMessages(message.message)
#methods def ends
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(CHANNEL).execute()
#main loop starts

if __name__ == '__main__':
    try:
        displayLine1("Welcome Back!")
        # initiatePush()
        # GpioToggle(GPIO_RELAY, False)
        # GPIO.output(GPIO_RELAY,GPIO.LOW)
        # displayLine2("Raghul Selvam 2")
        # print("start")
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Keyboard interrupt by User")
        GPIO.cleanup()
        # clearText()