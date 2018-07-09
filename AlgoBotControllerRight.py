import RPi.GPIO as GPIO

class AlgoBotControllerRight:
    stopCount = 0
    
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.cleanup()
        
        # IR Sensors Pins setup
        self.irLeftFront = 2
        self.irRightFront = 3
        self.irLeftSide = 27
        self.irRightSide = 17
        
        # Motor Driver pins setup 
        self.M11 = 16
        self.M12 = 12
        self.M21 = 21
        self.M22 = 20
        
        # set stopCount to 0
        AlgoBotControllerRight.stopCount = 0
        
        print('setup')
        GPIO.setup(self.irLeftFront, GPIO.IN)
        GPIO.setup(self.irRightFront, GPIO.IN)
        GPIO.setup(self.irLeftSide, GPIO.IN)
        GPIO.setup(self.irRightSide, GPIO.IN)
        
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
##        print('movin forward done!')
        return

    def rotateRight(self):
        print('rotating right...')
        GPIO.output(self.M11, 1)
        GPIO.output(self.M12, 0)
        GPIO.output(self.M21, 0)
        GPIO.output(self.M22, 1)
##        print('rotating right done!')
        return

    def rotateLeft(self):
        print('rotating left...')
        GPIO.output(self.M11, 0)
        GPIO.output(self.M12, 1)
        GPIO.output(self.M21, 1)
        GPIO.output(self.M22, 0)
##        print('rotating left done!')
        return

    def stopMovement(self):
        print('stop movement...')
        GPIO.output(self.M11, 1)
        GPIO.output(self.M12, 1)
        GPIO.output(self.M21, 1)
        GPIO.output(self.M22, 1)
##        print('stopped!')
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
                if(GPIO.input(self.irLeftFront)==1 and GPIO.input(self.irRightFront)==1):
                    self.moveForward()
                elif(GPIO.input(self.irLeftFront)==1 and GPIO.input(self.irRightFront)==0):
                    self.rotateLeft()
                elif(GPIO.input(self.irLeftFront)==0 and GPIO.input(self.irRightFront)==1):
                    self.rotateRight()
                else:
                    if(AlgoBotControllerRight.stopCount >= 100):
                        self.stopMovement()
                        AlgoBotControllerRight.stopCount = 0
                        self.step_forward_correction()
                        break
                    else:
                        self.stopMovement()
                        AlgoBotControllerRight.stopCount = AlgoBotControllerRight.stopCount + 1
        except:
            GPIO.cleanup()
        
        print('STEP: F (Forward Step) COMPLETE!')
        return
    
    def step_forward_correction(self):
        print('STEP:    F_correct (Forward Step CORRECTION)...')
        try:
            while (GPIO.input(self.irLeftSide)==1 or GPIO.input(self.irRightSide)==1):                
                if(GPIO.input(self.irLeftFront)==1 and GPIO.input(self.irRightFront)==1):
                    self.moveForward()
                elif(GPIO.input(self.irLeftFront)==1 and GPIO.input(self.irRightFront)==0):
                    self.rotateLeft()
                elif(GPIO.input(self.irLeftFront)==0 and GPIO.input(self.irRightFront)==1):
                    self.rotateRight()
                else:
                    self.moveForward()
        
            self.stopMovement()
        except:
            GPIO.cleanup()
            
        print('STEP:    F_correct (Forward Step CORRECTION) COMPLETE!')
        return
    
    # ==========================================
    def step_right(self):
        print('STEP: R (Right Step)...')
        
        try:
            while(GPIO.input(self.irLeftSide)==0 or GPIO.input(self.irRightSide)==0):
                self.rotateRight()
            
            while(GPIO.input(self.irLeftSide)==1 or GPIO.input(self.irRightSide)==1):
                self.rotateRight()
                
            self.stopMovement()
        except:
            GPIO.cleanup()
            
        print('STEP: R (Right Step) COMPLETE!')
        return
    
    # ==========================================
    def step_left(self):
        print('STEP: L (Left Step)...')
        
        try:
            while(GPIO.input(self.irLeftSide)==0 or GPIO.input(self.irRightSide)==0):
                self.rotateLeft()
            
            while(GPIO.input(self.irLeftSide)==1 or GPIO.input(self.irRightSide)==1):
                self.rotateLeft()
                
            self.stopMovement()
        except:
            GPIO.cleanup()
            
        print('STEP: L (Left Step) COMPLETE!')
        return
    
bot = AlgoBotControllerRight()
try:
    while 1:
        print('W = Forward, A = Left, D = Right, Anything Else to exit')
        command = input('Enter Command... ')
        
        if(command == 'W'):
            bot.step_forward()
        elif(command == 'A'):
            bot.step_left()
        elif(command == 'D'):
            bot.step_right
        else:
            print('DONE!')
            break
    
except:
    GPIO.cleanup()

