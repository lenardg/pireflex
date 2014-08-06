import RPi.GPIO as GPIO
import time, random

leftLedPin = 7
rightLedPin = 11
leftButtonPin = 13
rightButtonPin = 15

debug = False
buttonstates = {}

def ledOn(pin):
	GPIO.output(pin,True)

def ledOff(pin):
	GPIO.output(pin,False)

def prepareButton(pin):
	buttonstates[pin] = 0

def isButton(pin):
	return True if GPIO.input(pin) else False

def wasButton(pin):
	state = GPIO.input(pin)
	if state != buttonstates[pin]:
		buttonstates[pin] = state
		if debug and state == 1: print "Pushed ", pin
		if state == 1: return True
	return False

def intro():
	print("Are you ready?")
	print("Press the left button to get started!")
	GPIO.wait_for_edge(leftButtonPin,GPIO.RISING)
	GPIO.wait_for_edge(leftButtonPin,GPIO.FALLING)
	print("And GO!")

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(leftLedPin, GPIO.OUT)
	GPIO.setup(rightLedPin, GPIO.OUT)
	GPIO.setup(leftButtonPin, GPIO.IN)
	GPIO.setup(rightButtonPin, GPIO.IN)
	ledOff(leftLedPin)
	ledOff(rightLedPin)


setup()
intro()

score = 0
pushqueue = []
pausetime = 1.5
pausechange = 0.05
lasttime = time.time() - pausetime * 2

prepareButton(leftButtonPin)
prepareButton(rightButtonPin)

while True:
	if time.time() - lasttime > pausetime * 0.75:
		ledOff(leftLedPin)
		ledOff(rightLedPin)
	if time.time() - lasttime > pausetime:
		lasttime = time.time()
		pausetime -= pausechange;
		if pausetime < 1.1 and pausechange > 0.025:
			pausechange = 0.025
		elif pausetime < 0.75 and pausechange > 0.015:
			pausechange = 0.015
		elif pausetime < 0.3 and pausechange > 0:
			pausechange = 0
		ledOff(leftLedPin)
		ledOff(rightLedPin)
		newValue = random.randint(0,1)
		pushqueue.append(newValue)
		if debug: print("Next value to push is ",newValue)
		ledOn(leftLedPin if newValue == 0 else rightLedPin)
	time.sleep(0.02)
	leftButton = wasButton(leftButtonPin) 
	rightButton = wasButton(rightButtonPin)
	if leftButton or rightButton:
		if len(pushqueue) == 0:
		#	continue
			print("BOOOOM! YOU PRESSED A BUTTON WHILE YOU DID NOT HAVE TO!! GAME OVER!")
			break;
		pushed = 0 if leftButton else 1
		if pushqueue[0] != pushed:
			print("BOOOOM! WRONG BUTTON! GAME OVER!")
			break;
		pushqueue.pop(0)
		score += 1

print("Your score: ", score)
GPIO.cleanup()



