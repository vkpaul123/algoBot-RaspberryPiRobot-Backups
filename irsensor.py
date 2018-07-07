import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

irRight = 3
irLeft = 2

M11 = 16
M12 = 12
M21 = 21
M22 = 20

print('setup')
GPIO.setup(irLeft, GPIO.IN)
GPIO.setup(irRight, GPIO.IN)
GPIO.setup(M11, GPIO.OUT)
GPIO.setup(M12, GPIO.OUT)
GPIO.setup(M21, GPIO.OUT)
GPIO.setup(M22, GPIO.OUT)
print('Ready!')

def moveForward():
    print('moving forward...')
    GPIO.output(M11, 0)
    GPIO.output(M12, 1)
    GPIO.output(M21, 0)
    GPIO.output(M22, 1)
##    time.sleep(delay)
    print('movin forward done!')
    return

##def moveBackward():
##    print('moving Backward...')
##    GPIO.output(M11, 1)
##    GPIO.output(M12, 0)
##    GPIO.output(M21, 1)
##    GPIO.output(M22, 0)
##    time.sleep(delay)
##    print('movin backward done!')
##    return

def rotateRight():
    print('rotating right...')
    GPIO.output(M11, 1)
    GPIO.output(M12, 0)
    GPIO.output(M21, 0)
    GPIO.output(M22, 1)
##    time.sleep(delay)
    print('rotating right done!')
    return

def rotateLeft():
    print('rotating left...')
    GPIO.output(M11, 0)
    GPIO.output(M12, 1)
    GPIO.output(M21, 1)
    GPIO.output(M22, 0)
##    time.sleep(delay)
    print('rotating left done!')
    return

def stopMovement():
    print('stop movement...')
    GPIO.output(M11, 1)
    GPIO.output(M12, 1)
    GPIO.output(M21, 1)
    GPIO.output(M22, 1)
    print('stopped!')
    return

try:
    while(1):
        if(GPIO.input(irLeft)==1 and GPIO.input(irRight)==1):
            moveForward()
        elif(GPIO.input(irLeft)==0 and GPIO.input(irRight)==1):
            rotateLeft()
        elif(GPIO.input(irLeft)==1 and GPIO.input(irRight)==0):
            rotateRight()
        else:
            stopMovement()
except:
    GPIO.cleanup()

##print(GPIO.input(irLeft))
##print(GPIO.input(irRight))
##stopMovement()
print('done!')