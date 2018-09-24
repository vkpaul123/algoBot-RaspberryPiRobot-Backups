import requests as req
import time
import RPi.GPIO as GPIO

class AlgoBotControllerFinalTest:
	stopCount = 0

    # orient ('orientation') can be 0:North; 1:East; 2:South; 3:West
    orient = 0
    gridLimitX = 8
    gridLimitY = 8
    botLocX = 0
    botLocY = 0

    def __init__(self):
    	# GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.cleanup()

        # IR Sensors Pins
        self.irLeftFront = 2
        self.irRightFront = 3
        self.irLeftSide = 27
        self.irRightSide = 17

        # Motor Driver pins
        self.M11 = 16
        self.M12 = 12
        self.M21 = 21
        self.M22 = 20

        # Ultrasonic sensor pins
        self.ultraEcho = 23
        self.ultraTrig = 24

        # set stopCount to 0
        AlgoBotControllerFinalTest.stopCount = 0

        # setup
        print('setup')
        GPIO.setup(self.irLeftFront, GPIO.IN)
        GPIO.setup(self.irRightFront, GPIO.IN)
        GPIO.setup(self.irLeftSide, GPIO.IN)
        GPIO.setup(self.irRightSide, GPIO.IN)

        GPIO.setup(self.M11, GPIO.OUT)
        GPIO.setup(self.M12, GPIO.OUT)
        GPIO.setup(self.M21, GPIO.OUT)
        GPIO.setup(self.M22, GPIO.OUT)

        GPIO.setup(self.ultraTrig, GPIO.OUT)
		GPIO.setup(self.ultraEcho, GPIO.IN)

		self.socketAddr = '';
		self.robotId = '';
        
        print('Hardware Ready!')

    # def setupInitValues(self, sizeX, sizeY, locX, locY, orientation):
    def setupInitValues(self, socketAddr, robotId, locX, locY, orientation):
    	# set dimention values
    	# AlgoBotControllerFinalTest.gridLimitX = sizeX
    	# AlgoBotControllerFinalTest.gridLimitY = sizeY
    	self.socketAddr = socketAddr
    	self.robotId = robotId
    	AlgoBotControllerFinalTest.botLocX = locX
    	AlgoBotControllerFinalTest.botLocY = locY
    	AlgoBotControllerFinalTest.orient = orientation
    	print(AlgoBotControllerFinalTest.gridLimitX, ' ', AlgoBotControllerFinalTest.gridLimitY, ' ', AlgoBotControllerFinalTest.botLocX, ' ', AlgoBotControllerFinalTest.botLocY , ' ', AlgoBotControllerFinalTest.orient)
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

    def calcDistance():
	    GPIO.output(self.ultraTrig, 1)
	    
	    time.sleep(0.00001)
	    GPIO.output(self.ultraTrig, 0)
	    
	    startTime = time.time()
	    stopTime = time.time()
	    
	    while(GPIO.input(self.ultraEcho) == 0):
	        startTime = time.time()
	        
	    while(GPIO.input(self.ultraEcho) == 1):
	        stopTime = time.time()
	    
	    timeElapsed = stopTime - startTime
	    
		# speed of sound in air
	    distance = (timeElapsed * 34300) / 2
	    
	    return distance


	def obstacleDetected(self, xLoc, yLoc):
		print('obstacle Detected at X=',xLoc, ' Y=',yLoc)
		reqUpdateObstacle = req.get(self.socketAddr + '/robot/updateObstacle/', self.robotId, '/', xLoc, '/', yLoc, '/node')
		return

    def step_forward(self):
    	print('looking for obstacle...')
    	if (self.calcDistance() <= 50):
    		if (AlgoBotControllerFinalTest.orient == 0):
    			print('obstacle at North')
    			self.obstacleDetected(AlgoBotControllerFinalTest.botLocX, AlgoBotControllerFinalTest.botLocY+1)
    		elif (AlgoBotControllerFinalTest.orient == 1):
    			print('obstacle at East')
    			self.obstacleDetected(AlgoBotControllerFinalTest.botLocX+1, AlgoBotControllerFinalTest.botLocY)
    		elif (AlgoBotControllerFinalTest.orient == 2):
    			print('obstacle at South')
    			self.obstacleDetected(AlgoBotControllerFinalTest.botLocX, AlgoBotControllerFinalTest.botLocY-1)
    		else:
	    		print('obstacle at West')
    			self.obstacleDetected(AlgoBotControllerFinalTest.botLocX-1, AlgoBotControllerFinalTest.botLocY)
    	else:
	        print('step_forward', AlgoBotControllerFinalTest.orient, ' ', AlgoBotControllerFinalTest.botLocY, ' ', AlgoBotControllerFinalTest.gridLimitY)
	        if(AlgoBotControllerFinalTest.orient == 0):
	            if(AlgoBotControllerFinalTest.botLocY>=0 and AlgoBotControllerFinalTest.botLocY<AlgoBotControllerFinalTest.gridLimitY):
	            	reqUpdateMove = req.get(self.socketAddr + '/robot/updateMove/', self.robotId, '/', AlgoBotControllerFinalTest.botLocX, '/', AlgoBotControllerFinalTest.botLocY+0.5, '/', AlgoBotControllerFinalTest.orient+1, '/F/sub-node')
    	        	if(reqUpdateMove.text == 'OK'):
    	        		print('Move Updated')

	                self.step_move_forward()
	                AlgoBotControllerFinalTest.botLocY = AlgoBotControllerFinalTest.botLocY + 1
	                print('north')
	            else:
	                print('Reached Bounds! Cannot Move Forward in North!')
	        elif(AlgoBotControllerFinalTest.orient == 1):
	            if(AlgoBotControllerFinalTest.botLocX>=0 and AlgoBotControllerFinalTest.botLocX<AlgoBotControllerFinalTest.gridLimitX):
	            	reqUpdateMove = req.get(self.socketAddr + '/robot/updateMove/', self.robotId, '/', AlgoBotControllerFinalTest.botLocX+0.5, '/', AlgoBotControllerFinalTest.botLocY, '/', AlgoBotControllerFinalTest.orient+1, '/F/sub-node')
    	        	if(reqUpdateMove.text == 'OK'):
    	        		print('Move Updated')

	                self.step_move_forward()
	                AlgoBotControllerFinalTest.botLocX = AlgoBotControllerFinalTest.botLocX + 1
	                print('east')
	            else:
	                print('Reached Bounds! Cannot Move Forward in East!')
	        elif(AlgoBotControllerFinalTest.orient == 2):
	            if(AlgoBotControllerFinalTest.botLocY>0 and AlgoBotControllerFinalTest.botLocY<=AlgoBotControllerFinalTest.gridLimitY):
	            	reqUpdateMove = req.get(self.socketAddr + '/robot/updateMove/', self.robotId, '/', AlgoBotControllerFinalTest.botLocX, '/', AlgoBotControllerFinalTest.botLocY-0.5, '/', AlgoBotControllerFinalTest.orient+1, '/F/sub-node')
    	        	if(reqUpdateMove.text == 'OK'):
    	        		print('Move Updated')

	                self.step_move_forward()
	                AlgoBotControllerFinalTest.botLocY = AlgoBotControllerFinalTest.botLocY - 1
	                print('south')
	            else:
	                print('Reached Bounds! Cannot Move Forward in South!')
	        elif(AlgoBotControllerFinalTest.orient == 3):
	            if(AlgoBotControllerFinalTest.botLocX>0 and AlgoBotControllerFinalTest.botLocX<=AlgoBotControllerFinalTest.gridLimitX):
	            	reqUpdateMove = req.get(self.socketAddr + '/robot/updateMove/', self.robotId, '/', AlgoBotControllerFinalTest.botLocX-0.5, '/', AlgoBotControllerFinalTest.botLocY, '/', AlgoBotControllerFinalTest.orient+1, '/F/sub-node')
    	        	if(reqUpdateMove.text == 'OK'):
    	        		print('Move Updated')

	                self.step_move_forward()
	                AlgoBotControllerFinalTest.botLocX = AlgoBotControllerFinalTest.botLocX - 1
	                print('west')
	            else:
	                print('Reached Bounds! Cannot Move Forward in West!')	        
        return

    def step_move_forward(self):
        print('STEP: F (Forward Step)...')
        print(GPIO.input(self.irLeftFront), ' ', GPIO.input(self.irRightFront))
        try:
        	while 1:
                if(GPIO.input(self.irLeftFront)==1 and GPIO.input(self.irRightFront)==1):
                    self.moveForward()
                elif(GPIO.input(self.irLeftFront)==1 and GPIO.input(self.irRightFront)==0):
                    self.rotateLeft()
                elif(GPIO.input(self.irLeftFront)==0 and GPIO.input(self.irRightFront)==1):
                    self.rotateRight()
                else:
                    if(AlgoBotControllerFinalTest.stopCount >= 200):
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
        reqUpdateMove = req.get(self.socketAddr + '/robot/updateMove/', self.robotId, '/', AlgoBotControllerFinalTest.botLocX, '/', AlgoBotControllerFinalTest.botLocY, '/', AlgoBotControllerFinalTest.orient+1, '/F/node')
    	if(reqUpdateMove.text == 'OK'):
    		print('Move Updated')
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
        reqUpdateMove = req.get(self.socketAddr + '/robot/updateMove/', self.robotId, '/', AlgoBotControllerFinalTest.botLocX, '/', AlgoBotControllerFinalTest.botLocY, '/', AlgoBotControllerFinalTest.orient+1, '/R/node')
        if(reqUpdateMove.text == 'OK'):
       		print('Move Updated')
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
        reqUpdateMove = req.get(self.socketAddr + '/robot/updateMove/', self.robotId, '/', AlgoBotControllerFinalTest.botLocX, '/', AlgoBotControllerFinalTest.botLocY, '/', AlgoBotControllerFinalTest.orient+1, '/L/node')
        if(reqUpdateMove.text == 'OK'):
       		print('Move Updated')
        return

ipAddr = input('Enter IP address of Server... ')
port = input('Enter port... ')
socketAddr = 'http://' + ipAddr + ':' + port

try:
	reqCheckConn = req.get(socketAddr + '/testConnection')
	repCheckConn = reqCheckConn.text

	if (resCheckConn == 'OK'): 	
		print('Connection OK!')
		robotId = input('Enter Robot ID... ')
		# sizeX = int(input('Enter Size of Grid (X-Axis)... '))
		# sizeY = int(input('Enter Size of Grid (Y-Axis)... '))
		locX = int(input('Enter the X-Location of Robot... '))
		locY = int(input('Enter the Y-Location of Robot... '))
		orientation = int(input('Enter the orientation of Robot.\nOrientation can be 0:North; 1:East; 2:South; 3:West ... '))

		bot = AlgoBotControllerFinalTest()
		# bot.setupInitValues(sizeX, sizeY, locX, locY, orientation)
		bot.setupInitValues(socketAddr, robotId, locX, locY, orientation)
		bot.stopMovement()

		reqPathSet = req.get(socketAddr + '/getPath/' + robotId + '/get')
		resPathStream = reqPathSet.text

		if(resPathStream != ''):
			pathStreamList = list(resPathStream)
			#try:

			for moveCommand in pathStreamList:
				if(command == 'F'):
			        print(command, ' F')
			        bot.step_forward()
			    elif(command == 'L'):
			        print(command,' L')
			        bot.step_left()
			    elif(command == 'R'):
			        print(command, 'R')
			        bot.step_right()
			    else:
			        print('DONE!')
			        break

			# while 1:
			#     print('W = Forward, A = Left, D = Right, Anything Else to exit')
			#     command = input('Enter Command... ')

			#     if(command == 'W' or command == 'w'):
			#         print(command, ' W')
			#         bot.step_forward()
			#     elif(command == 'A' or command == 'a'):
			#         print(command,' A')
			#         bot.step_left()
			#     elif(command == 'D' or command == 'd'):
			#         print(command, 'D')
			#         bot.step_right()
			#     else:
			#         print('DONE!')
			#         break
			#except:
			#    print('Error Occoured Somewhere')
			#    GPIO.cleanup()
			#finally:
			GPIO.cleanup()
except:
	print('Connection Failed. Host unreachable. Please check if the server is running')