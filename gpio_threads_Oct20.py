#needed for gpio
import RPi.GPIO as GPIO # import RPi GPIO library
from threading import Thread
#from playsound import playsound #library for playing sound
import time

GPIO.setmode(GPIO.BOARD) #use physical pin numbering
GPIO.setwarnings(False) #disable warnings

##Flippers input output pins
GPIO.setup(3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #Left Flipper Input (EOS Switch In)
GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #Right Flipper Input (EOS Switch In)
GPIO.setup(7,GPIO.OUT)                              #Left Flipper Output (PWM)
GPIO.setup(8,GPIO.OUT)                              #Right Flipper Output (PWM)
GPIO.setup(10,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 1 (Points)
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 2 (Points)
GPIO.setup(12,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 3 (Points)
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 4 (Points)

#Set PWM on pins 7 & 8 to 65,800,000 Hz. Start at 100% PWM
pwm1=GPIO.PWM(7,65.8e+6)
pwm2=GPIO.PWM(8, 65.8e+6)
pwm1.start(100)
pwm2.start(100)

##input channels for playfield_parts
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Slingshot 1 Input (Points)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Slingshot 2 Input (Points)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 1 (Points)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 2 (Points)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 3 (Points)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Target (Points)

class GPIO_pins():

    def flippers():
            ##If there is a high to low transition, the flipper bat is up. Wait 200ms then lower PWM.
            ##  else the flipper bat is down, return pwm to 100%

            ##  Nested if statements to ensure that each individual pwm can change from 50% to 100%
            ##  independently from each other
        while (True):
            if (GPIO.input(3)==GPIO.LOW) or (GPIO.input(5)==GPIO.LOW):
                if(GPIO.input(3)==GPIO.LOW):
                    time.sleep(0.2)
                    pwm1.ChangeDutyCycle(50)
                else:
                    time.sleep(0.2)
                    pwm2.ChangeDutyCycle(50)
            if(GPIO.input(3)==GPIO.HIGH) or (GPIO.input(5)==GPIO.HIGH):
                if(GPIO.input(3)==GPIO.HIGH):
                    pwm1.ChangeDutyCycle(100)
                else:
                    pwm2.ChangeDutyCycle(100)

    def pop_bumpers():
        while (True):
            if ((GPIO.input(10) or GPIO.input(11) or GPIO.input(12) or GPIO.input(13))==GPIO.HIGH): #if ball touches any of the 4 pop bumpers
                print("Pop Bumper")
                global score
                score=score+100
                #playsound('C:\Users\codys\Desktop\Project_Lab_2\Code\three20.mp3', block=False)

    def slingshots():
        while (True):
            if ((GPIO.input(15) or GPIO.input(16))==GPIO.HIGH):
                print("slingshots")
                global score
                score=score+200
                #playsound('C:\Users\codys\Desktop\Project_Lab_2\Code\three20.mp3', block=False)


    def area1():
        while (True):
            if GPIO.input(18)==GPIO.HIGH:   #if ball rolls over area1
                print("area1")
                global score
                score=score+200
                #playsound('area.mp3', block=False)

    def area2():
        while (True):
            if (GPIO.input(19)==GPIO.HIGH): #if ball rolls over area2
                print("area2")
                global score
                score=score+300
                #playsound('area.mp3', block=False)

    def area3():
        while (True):
            if (GPIO.input(21)==GPIO.HIGH): #if ball rolls over area3
                print("area3")
                global score
                score=score+500
                #playsound('area.mp3', block=False)

    def targets():
        while (True):
            if(GPIO.input(22)==GPIO.HIGH):  #if ball hits targets
                print("targets")
                global score
                score=score+2000
                #playsound('target.mp3', block=False)



    if __name__=='__main__': #start threads asynchronously
        Thread(target=pop_bumpers).start()
        Thread(target=targets).start()
        Thread(target=area1).start()
        Thread(target=area2).start()
        Thread(target=area3).start()
        Thread(target=flippers).start()
