import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)



print('hi')

M11 = 16
M12 = 12
M21 = 21
M22 = 20

delay = 6

GPIO.setup(M11, GPIO.OUT)
GPIO.setup(M12, GPIO.OUT)
GPIO.setup(M21, GPIO.OUT)
GPIO.setup(M22, GPIO.OUT)
print('start')
##time.sleep(delay)



print('F')
GPIO.output(M11,1)
GPIO.output(M12,0)
GPIO.output(M21,1)
GPIO.output(M22,0)
print('F Done')
time.sleep(delay)
print('F Done Stop')

#print('L')
#GPIO.output(M11,0)
#GPIO.output(M12,1)
#GPIO.output(M21,1)
#GPIO.output(M22,0)
#print('L Done')
#time.sleep(delay)

#print('R')
#GPIO.output(M11,1)
#GPIO.output(M12,0)
#GPIO.output(M21,0)
#GPIO.output(M22,1)
#print('R Done')
#time.sleep(delay)

GPIO.cleanup()
print('All Done!')
