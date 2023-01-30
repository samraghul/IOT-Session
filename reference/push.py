import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)


if __name__ == '__main__':
    try:
        flag = True
        while True: # Run forever
            
            if GPIO.input(24) == GPIO.HIGH:
                
                if flag == True:
                    flag = False
                    GPIO.setup(25, GPIO.HIGH)
                    print("Button was pushed! True")
                else:
                    flag = True
                    GPIO.setup(25, GPIO.LOW)
                    print("Button was pushed! False")
            time.sleep(0.5)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Keyboard interrupt by User")
        GPIO.cleanup()
