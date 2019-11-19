#needed for gpio
import RPi.GPIO as GPIO # import RPi GPIO library
from threading import Thread
from threading import Timer
import time
import pygame

GPIO.setmode(GPIO.BOARD) #use physical pin numbering
GPIO.setwarnings(False) #disable warnings

##Setup for input & output pins
GPIO.setup(10,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 1 (Points)
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 2 (Points)
GPIO.setup(12,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 3 (Points)
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 4 (Points)
GPIO.setup(3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #Left Flipper Input (EOS Switch In)
GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #Right Flipper Input (EOS Switch In)
GPIO.setup(7,GPIO.OUT)                              #Left Flipper Output (PWM)
GPIO.setup(8,GPIO.OUT)                              #Right Flipper Output (PWM)

#Set PWM on pins 7 & 8 to 100,000 Hz. Start at 100% PWM


##input channels for playfield_parts
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Slingshot 1 Input (Points)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Slingshot 2 Input (Points)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 1 (Points)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 2 (Points)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 3 (Points)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Target (Points)

class GPIO_pins():

    def flippers(score):
        pwm1=GPIO.PWM(7, 1000)
        pwm2=GPIO.PWM(8, 1000)
        pwm1.start(50)
        pwm2.start(50)
        while (True):
            if (GPIO.input(3)==GPIO.LOW) or (GPIO.input(5)==GPIO.LOW):
                if(GPIO.input(3)==GPIO.LOW):
                    pwm1.ChangeDutyCycle(10)
                else:
                    pwm2.ChangeDutyCycle(10)
            if(GPIO.input(3)==GPIO.HIGH) or (GPIO.input(5)==GPIO.HIGH):
                if(GPIO.input(3)==GPIO.HIGH):
                    pwm1.ChangeDutyCycle(50)
                else:
                    pwm2.ChangeDutyCycle(50)
                    
        return score
                    

    def pop_bumpers():
        
        def boolTimer(timeUp):
            return not timeUp
        
        global score
        zeroCount = 0
        lowHigh = True  #Start by looking for a low to high transition (switch pressed)
        highLow = False #Use for after low to high transition detected
        timeUp=False
        alarm=Timer(0.1,boolTimer,timeUp)



        while (True):
            if ((GPIO.input(10) or GPIO.input(11) or GPIO.input(12) or GPIO.input(13))==GPIO.HIGH): #if ball touches any of the 4 pop bumpers
                #Nested ifs to track only the transitions we are looking for
                if(lowHigh):
                    if ((GPIO.input(10) or GPIO.input(11) or GPIO.input(12) or GPIO.input(13))==GPIO.HIGH):
                        lowHigh=False
                        highLow=True
                        if not(alarm.is_alive()):
                            alarm.cancel()
                            alarm.start()
                        else:
                            alarm.start()

                if(highLow):
                    if((GPIO.input(10) or GPIO.input(11) or GPIO.input(12) or GPIO.input(13))==GPIO.LOW):
                        lowHigh=True
                        highLow=False
                        zeroCount=zeroCount+1   #only count high to low transitions AFTER
                                                #a low to high transition has occured
                        if not(alarm.is_alive()):
                            alarm.cancel()
                            alarm.start()
                        else:
                            alarm.start()

                if(zeroCount>=3):   #Only increase score after a certain number of zeros
                    score=score+100
                    zeroCount=0     #Reset zeroCount
                    lowHigh=True    #Make sure Booleans are correctly reset
                    highLow=False
                    soundObj=pygame.mixer.Sound("bell-ding.wav")
                    soundObj.play()


                if(timeUp):
                    zeroCount=0     #Reset zeroCount
                    lowHigh=True    #Make sure Booleans are correctly reset
                    highLow=False
                    timeUp=False    #Reset Timer variable


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
        score=0
        #Thread(target=pop_bumpers,args=(score,)).start()
        Thread(target=flippers,args=(score,)).start()
        print(score)
        #Thread(target=targets).start()
        #Thread(target=area1).start()
        #Thread(target=area2).start()
        #Thread(target=area3).start()
