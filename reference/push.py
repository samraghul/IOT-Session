import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)


if __name__ == '__main__':
    try:
        while True: # Run forever
            if GPIO.input(22) == GPIO.HIGH:
                print("Button was pushed!")
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Keyboard interrupt by User")
        GPIO.cleanup()
