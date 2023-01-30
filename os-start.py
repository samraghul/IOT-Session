#Libraries
import RPi.GPIO as GPIO
from time import sleep
#Disable warnings (optional)
GPIO.setwarnings(False)
#Select GPIO mode
GPIO.setmode(GPIO.BCM)
#Set buzzer - pin 23 as output
buzzer=25
GPIO.setup(buzzer,GPIO.OUT)
loopCount = 2
count = 0
#Run forever loop
if __name__ == '__main__':
  try:
    while loopCount > count:
        GPIO.output(buzzer,GPIO.HIGH)
        # print ("Beep")
        sleep(0.1) # Delay in seconds
        GPIO.output(buzzer,GPIO.LOW)
        # print ("No Beep")
        sleep(0.1)
        count = count + 1
  except KeyboardInterrupt:
        print("Beep stopped by User")
        GPIO.cleanup()
