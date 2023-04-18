import configparser
import time
import os
import RPi.GPIO as GPIO

# Find config file
dir = os.path.dirname(__file__)  # os.getcwd()
configFilePath = os.path.abspath(os.path.join(dir, "app.cfg"))
configParser = configparser.RawConfigParser()
configParser.read(configFilePath)

# Read in config variables
hopperGPIO = str(configParser.get('feederConfig', 'Hopper_GPIO_Pin'))
hopperTime = str(configParser.get('feederConfig', 'Hopper_Spin_Time'))

def spin_hopper(pin, duration):
    try:
        pin=int(pin)
        duration=float(duration)
        GPIO.setwarnings(False)
        GPIO.cleanup(pin)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        pwm=GPIO.PWM(pin,50)
        pwm.start(50)
        pwm.ChangeDutyCycle(12)
        time.sleep(0.5)
        pwm.ChangeDutyCycle(12)
        time.sleep(0.5)
        time.sleep(duration)
        pwm.start(0)
        GPIO.cleanup(pin)

        return 'ok'
    except Exception as e:
        return 'ok'  # e
