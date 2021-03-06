import RPi.GPIO as GPIO

class AlgoBotControllerFinalTest:
    stopCount = 0

    # orient ('orientation') can be 0:North; 1:East; 2:South; 3:West
    orient = 0
    gridLimitX = 0
    gridLimitY = 0
    botLocX = 0
    botLocY = 0

    def __init__(self):
    	# GPIO setup
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
        AlgoBotControllerFinalTest.stopCount = 0

        print('setup')
        GPIO.setup(self.irLeftFront, GPIO.IN)
        GPIO.setup(self.irRightFront, GPIO.IN)
        GPIO.setup(self.irLeftSide, GPIO.IN)
        GPIO.setup(self.irRightSide, GPIO.IN)

        GPIO.setup(self.M11, GPIO.OUT)
        GPIO.setup(self.M12, GPIO.OUT)
        GPIO.setup(self.M21, GPIO.OUT)
        GPIO.setup(self.M22, GPIO.OUT)
        print('Hardware Ready!')

    def setupInitValues(sizeX, sizeY, locX, locY, orientation):
    	# set dimention values
    	AlgoBotControllerFinalTest.gridLimitX = sizeX
    	AlgoBotControllerFinalTest.gridLimitY = sizeY
    	AlgoBotControllerFinalTest.botLocX = locX
    	AlgoBotControllerFinalTest.botLocY = locY
    	AlgoBotControllerFinalTest.orient = orientation
    	print('All initial Values Set. Ready to take Commands!')
    	return

    def moveForward(self):
        print('moving forward...')
        GPIO.output(self.M11, 0)
        GPIO.output(self.M12, 1)
        GPIO.output(self.M21, 0)
        GPIO.output(self.M22, 1)
       	# print('movin forward done!')
        return

    def rotateRight(self):
        print('rotating right...')
        GPIO.output(self.M11, 1)
        GPIO.output(self.M12, 0)
        GPIO.output(self.M21, 0)
        GPIO.output(self.M22, 1)
        # print('rotating right done!')
        return

    def rotateLeft(self):
        print('rotating left...')
        GPIO.output(self.M11, 0)
        GPIO.output(self.M12, 1)
        GPIO.output(self.M21, 1)
        GPIO.output(self.M22, 0)
        # print('rotating left done!')
        return

    def stopMovement(self):
        print('stop movement...')
        GPIO.output(self.M11, 1)
        GPIO.output(self.M12, 1)
        GPIO.output(self.M21, 1)
        GPIO.output(self.M22, 1)
        # print('stopped!')
        return

    # ==========================================
    #
    # 1 = white area detected
    # 0 = black area detected
    #
    # ==========================================

    def step_forward(self):
	if(AlgoBotControllerFinalTest.orient == 0 and AlgoBotControllerFinalTest.botLocY>=0 and AlgoBotControllerFinalTest.botLocY<AlgoBotControllerFinalTest.gridLimitY):
            self.step_move_forward()
            AlgoBotControllerFinalTest.botLocY = AlgoBotControllerFinalTest.botLocY + 1
	elif(AlgoBotControllerFinalTest.orient == 1 and AlgoBotControllerFinalTest.botLocX>=0 and AlgoBotControllerFinalTest.botLocX<AlgoBotControllerFinalTest.gridLimitX):
            self.step_move_forward()
            AlgoBotControllerFinalTest.botLocX = AlgoBotControllerFinalTest.botLocX + 1
	elif(AlgoBotControllerFinalTest.orient == 2 and AlgoBotControllerFinalTest.botLocY>0 and AlgoBotControllerFinalTest.botLocY<=AlgoBotControllerFinalTest.gridLimitY):
            self.step_move_forward()
            AlgoBotControllerFinalTest.botLocY = AlgoBotControllerFinalTest.botLocY - 1
	elif(AlgoBotControllerFinalTest.orient == 3 and AlgoBotControllerFinalTest.botLocX>0 and AlgoBotControllerFinalTest.botLocX<=AlgoBotControllerFinalTest.gridLimitX):
            self.step_move_forward()
            AlgoBotControllerFinalTest.botLocX = AlgoBotControllerFinalTest.botLocX - 1
	return

    def step_move_forward(self):
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
                    if(AlgoBotControllerFinalTest.stopCount >= 100):
                        self.stopMovement()
                        AlgoBotControllerFinalTest.stopCount = 0
                        self.step_forward_correction()
                        break
                    else:
                        self.stopMovement()
                        AlgoBotControllerFinalTest.stopCount = AlgoBotControllerFinalTest.stopCount + 1
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

        AlgoBotControllerFinalTest.orient = AlgoBotControllerFinalTest.orient + 1
        if(AlgoBotControllerFinalTest.orient > 3):
            AlgoBotControllerFinalTest.orient = 0

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

        AlgoBotControllerFinalTest.orient = AlgoBotControllerFinalTest.orient - 1
        if(AlgoBotControllerFinalTest.orient == 0):
            AlgoBotControllerFinalTest.orient = 3

        print('STEP: L (Left Step) COMPLETE!')
        return

sizeX = input('Enter Size of Grid (X-Axis)... ')
sizeY = input('Enter Size of Grid (Y-Axis)... ')
locX = input('Enter the X-Location of Robot... ')
locY = input('Enter the Y-Location of Robot... ')
orientation = input('Enter the orientation of Robot.\nOrientation can be 0:North; 1:East; 2:South; 3:West ... ')

bot = AlgoBotControllerFinalTest()
bot.setupInitValues(sizeX, sizeY, locX, locY, orientation)

try:
    while 1:
        print('W = Forward, A = Left, D = Right, Anything Else to exit')
        command = input('Enter Command... ')
        
        if(command == 'W' or command == 'w'):
            bot.step_forward()
        elif(command == 'A' or command == 'a'):
            bot.step_left()
        elif(command == 'D' or command == 'd'):
            bot.step_right()
        else:
            print('DONE!')
            break
except:
    GPIO.cleanup()
