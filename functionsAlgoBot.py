import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

M11 = 16
M12 = 12
M21 = 21
M22 = 20

delay = 8.47

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
    time.sleep(delay)
    print('movin forward done!')
    return

def moveBackward():
    print('moving Backward...')
    GPIO.output(M11, 1)
    GPIO.output(M12, 0)
    GPIO.output(M21, 1)
    GPIO.output(M22, 0)
    time.sleep(delay)
    print('movin backward done!')
    return

def rotateRight():
    print('rotating right...')
    GPIO.output(M11, 1)
    GPIO.output(M12, 0)
    GPIO.output(M21, 0)
    GPIO.output(M22, 1)
    time.sleep(delay)
    print('rotating right done!')
    return

def rotateLeft():
    print('rotating left...')
    GPIO.output(M11, 0)
    GPIO.output(M12, 1)
    GPIO.output(M21, 1)
    GPIO.output(M22, 0)
    time.sleep(delay)
    print('rotating left done!')
    return

print('start')

moveForward()
moveBackward()
rotateLeft()
moveForward()
moveBackward()
rotateRight()
moveForward()
moveBackward()

GPIO.cleanup()
print('All Done!')