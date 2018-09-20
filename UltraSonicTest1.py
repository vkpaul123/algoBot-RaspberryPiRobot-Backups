import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

echoPin = 23
trigPin = 24

GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

def calcDistance():
    GPIO.output(trigPin, 1)
    
    time.sleep(0.00001)
    GPIO.output(trigPin, 0)
    
    startTime = time.time()
    stopTime = time.time()
    
    while(GPIO.input(echoPin) == 0):
        startTime = time.time()
        
    while(GPIO.input(echoPin) == 1):
        stopTime = time.time()
    
    timeElapsed = stopTime - startTime
    
##    speed of sound in air
    distance = (timeElapsed * 34300) / 2
    
    return distance


try:
    while 1:
        time.sleep(1)
        print('Distance = ', calcDistance(), ' cm')
except:
    GPIO.cleanup()
