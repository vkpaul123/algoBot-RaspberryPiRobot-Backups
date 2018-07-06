import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

# set pins as output
GPIO.setup(20,GPIO.OUT)



GPIO.output(20,True)


