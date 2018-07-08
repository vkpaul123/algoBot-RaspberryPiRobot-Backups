import RPi.GPIO as GPIO
import time

class AlgoBotController:
    stopCount = 0
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.cleanup()
        
        # IR Sensors Pins setup
        self.irLeft = 2
        self.irRight = 3
        
        # Motor Driver pins setup 
        self.M11 = 16
        self.M12 = 12
        self.M21 = 21
        self.M22 = 20
        
        # set stopCount to 0
        AlgoBotController.stopCount = 0
        
        print('setup')
        GPIO.setup(self.irLeft, GPIO.IN)
        GPIO.setup(self.irRight, GPIO.IN)
        GPIO.setup(self.M11, GPIO.OUT)
        GPIO.setup(self.M12, GPIO.OUT)
        GPIO.setup(self.M21, GPIO.OUT)
        GPIO.setup(self.M22, GPIO.OUT)
        print('Ready!')
        
    def moveForward(self):
        print('moving forward...')
        GPIO.output(self.M11, 0)
        GPIO.output(self.M12, 1)
        GPIO.output(self.M21, 0)
        GPIO.output(self.M22, 1)
        print('movin forward done!')
        return

    def rotateRight(self):
        print('rotating right...')
        GPIO.output(self.M11, 1)
        GPIO.output(self.M12, 0)
        GPIO.output(self.M21, 0)
        GPIO.output(self.M22, 1)
        print('rotating right done!')
        return

    def rotateLeft(self):
        print('rotating left...')
        GPIO.output(self.M11, 0)
        GPIO.output(self.M12, 1)
        GPIO.output(self.M21, 1)
        GPIO.output(self.M22, 0)
        print('rotating left done!')
        return

    def stopMovement(self):
        print('stop movement...')
        GPIO.output(self.M11, 1)
        GPIO.output(self.M12, 1)
        GPIO.output(self.M21, 1)
        GPIO.output(self.M22, 1)
        print('stopped!')
        return

    # ==========================================
    #
    # 1 = white area detected
    # 0 = black area detected
    #
    # ==========================================
    
    def step_forward(self):
        print('STEP: F (Forward Step)...')
        try:
            while 1:
                if(GPIO.input(self.irLeft)==1 and GPIO.input(self.irRight)==1):
                    self.moveForward()
                elif(GPIO.input(self.irLeft)==0 and GPIO.input(self.irRight)==1):
                    self.rotateLeft()
                elif(GPIO.input(self.irLeft)==1 and GPIO.input(self.irRight)==0):
                    self.rotateRight()
                else:
                    if(AlgoBotController.stopCount <= 100):
                        self.stopMovement()
                        AlgoBotController.stopCount = 0
                        self.step_forward_correction()
                        break
                    else:
                        self.stopMovement()
                        AlgoBotController.stopCount = AlgoBotController.stopCount + 1
        except:
            GPIO.cleanup()
        
        print('STEP: F (Forward Step) COMPLETE!')
        return
    
    def step_forward_correction(self):
        print('STEP:    F_correct (Forward Step CORRECTION)...')
        try:
            afterTime = time.time() + 4.5
            currTime = time.time()
        
            while (currTime <= afterTime):
                currTime = time.time()
                
##                if (GPIO.input(self.irLeft)==0 or GPIO.input(self.irRight)==0):
##                    self.moveForward()
                
                if(GPIO.input(self.irLeft)==1 and GPIO.input(self.irRight)==1):
                    self.moveForward()
                elif(GPIO.input(self.irLeft)==0 and GPIO.input(self.irRight)==1):
                    self.rotateLeft()
                elif(GPIO.input(self.irLeft)==1 and GPIO.input(self.irRight)==0):
                    self.rotateRight()
                else:
                    self.moveForward()
        
            self.stopMovement()
        except:
            GPIO.cleanup()
            
        print('STEP:    F_correct (Forward Step CORRECTION) COMPLETE!')
        return
    
bot = AlgoBotController()
try:
    bot.step_forward()
except:
    GPIO.cleanup()
