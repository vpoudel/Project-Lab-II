#needed for gpio
import RPi.GPIO as GPIO # import RPi GPIO library
from threading import Thread
from playsound import playsound	#library for playing sound


GPIO.setmode(GPIO.BOARD) #use physical pin numbering
GPIO.setwarnings(False) #disable warnings

##Flippers input output pins
GPIO.setup(3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
pwm1=GPIO.PWM(7,65.8e+6)
pwm2=GPIO.PWM(8, 65.8e+6)
pwm1.start(100)
pwm2.start(100)

##input channels for playfield_parts
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class GPIO_pins():

	def __init__(self):
		global score
		score=0

	def flippers():
		while (True):
			if (GPIO.input(3)==GPIO.LOW):
				pwm1.ChangeDutyCycle(50)
			elif (GPIO.input(5)==GPIO.LOW):
				pwm2.ChangeDutyCycle(50)
			else
				pwm1.ChangeDutyCycle(100)
				pwm2.ChangeDutyCycle(100)

	def pop_bumpers():
		while (True):
			if ((GPIO.input(10) or GPIO.input(11) or GPIO.input(12) or GPIO.input(13))==GPIO.HIGH):	#if ball touches pop bumper1,2,3,4
				print("Pop Bumper")
				score=score+100
				#playsound('bumpers.mp3', block=False)

	def slingshots():
		while (True):
			if ((GPIO.input(15) or GPIO.input(16))==GPIO.HIGH):
				print("slingshots")
				score=score+200
				#playsound('slingshots.mp3', block=False)


	def area1():
		while (True):
			if GPIO.input(18)==GPIO.HIGH:	#if ball rolls over area1
				print("area1")
				score=score+200
				#playsound('area.mp3', block=False)

	def area2():
		while (True):
			if (GPIO.input(19)==GPIO.HIGH):	#if ball rolls over area3
				print("area2")
				score=score+300
				#playsound('area.mp3', block=False)

	def area3():
		while (True):
			if (GPIO.input(21)==GPIO.HIGH):	#if ball rolls over area3
				print("area3")
				score=score+500
				#playsound('area.mp3', block=False)

	def targets():
		while (True):
			if(GPIO.input(22)==GPIO.HIGH):	#if ball hits targets
				print("targets")
				score=score+2000
				#playsound('target.mp3', block=False)



	if __name__=='__main__': #start threads asynchronously
		Thread(target=pop_bumpers).start()
		Thread(target=targets).start()
		Thread(target=area1).start()
		Thread(target=area2).start()
		Thread(target=area3).start()
		Thread(target=flippers).start()
