import RPi.GPIO as GPIO
from threading import Thread, Timer
import time
import sys

#all reqd for gui class
from tkinter import * #import GUI library
import tkinter.font #import tkinter font
from PIL import Image, ImageTk

import pygame #sound

GPIO.setmode(GPIO.BOARD) #use physical pin numbering
GPIO.setwarnings(False) #disable warnings

##Setup for input & output pins
GPIO.setup(3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #Left Flipper Input (EOS Switch In)
GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #Right Flipper Input (EOS Switch In)
GPIO.setup(7,GPIO.OUT)                              #Left Flipper Output (PWM)
GPIO.setup(8,GPIO.OUT)                              #Right Flipper Output (PWM)
GPIO.setup(10,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 1 (Points)
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 2 (Points)
GPIO.setup(12,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 3 (Points)
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Pop Bumper 4 (Points)

#Set PWM on pins 7 & 8 to 1,000 Hz. Start at 50% PWM
pwm1=GPIO.PWM(7, 1000)
pwm2=GPIO.PWM(8, 1000)
pwm1.start(50)
pwm2.start(50)

##input channels for playfield_parts
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Slingshot 1 Input (Points)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Slingshot 2 Input (Points)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 1 (Points)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 2 (Points)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 3 (Points)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Rollover Area 4 (Lives)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Target (Points)

score=0
life=3
class GPIO_pins():
    def Lives():
        while(True):
            if(GPIO.input(22)==GPIO.HIGH):  #If a ball is lost, tell display to remove a life
                global life  #Sleep to ignore extra bouncing
                life=life-1
                time.sleep(0.3)
                if(life==0):
                    global score
                    score=0;

    def Sound(soundfile):
        try:
            if(soundThread.is_alive()):
                soundThread.join()
        except:
            pass
        soundThread=Thread(target=GPIO_pins.PlaySound, args=(soundfile,))
        soundThread.start()
        time.sleep(0.15)

    def PlaySound(soundfile):
        soundObj=pygame.mixer.Sound(soundfile)
        soundObj.play()

    def flippers():
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

    def pop_bumpers():
        while (True):
            if ((GPIO.input(10)==GPIO.HIGH) or (GPIO.input(11)==GPIO.HIGH) or (GPIO.input(12)==GPIO.HIGH) or (GPIO.input(13)==GPIO.HIGH)): #if ball touches any pop bumper
                global score
                score=score+500
                GPIO_pins.Sound("bell_ding.wav")
                print(score)

    def areas():
        while (True):
            if ((GPIO.input(18)==GPIO.HIGH) or (GPIO.input(19)==GPIO.HIGH) or (GPIO.input(21)==GPIO.HIGH)):   #if ball rolls over area1
                global score
                score=score+400
                GPIO_pins.Sound("area_noise.wav")

class App():
    def __init__(self, master):
        self.master=master
        master.title("Pinball")
        scrwidth=master.winfo_screenwidth()
        scrheight = master.winfo_screenheight()

        #canvas large
        Canvas(master).pack()
        self.back_image=ImageTk.PhotoImage(Image.open('wall.jpg'))
        Label(master, image=self.back_image).place(relwidth=1,relheight=1)

        #label inside top right
        self.label1=Label(master, text='',bg='white', font=("Times",36,"bold"))
        self.label1.place(relx=0.0,rely=1.0,anchor="ne")

        #Frame inside canvas
        frame=Frame(master, height=scrheight/10, width=scrwidth/4, bg='white', bd=5)
        frame.place(relx=.5, rely=.5, anchor="center")
        self.label2=Label(frame, text= '', bg='white', font=("Times", 36, "bold"))
        self.label2.place(relheight=1, relwidth=1)

    def score_update(self):
        global score
        global life
        self.label['text']=str(score)
        root.after(1,self.score_update)

#Initialize Sounds
pygame.mixer.pre_init(44100, -16, 2, 4096) #frequency, size, channels, buffersize
pygame.init() #turn all of pygame on.

#Define GUI object
root = Tk()
app = App(root)
w,h=root.winfo_screenwidth(),root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.after(10,app.score_update)

lifeCount=Thread(target=GPIO_pins.Lives) #Keep track of lives
bats=Thread(target=GPIO_pins.flippers)   #Control Flippers
pop=Thread(target=GPIO_pins.pop_bumpers)   #Pop bumpers
rollArea=Thread(target=GPIO_pins.areas)   #Rollover Areas

#Start all threads
lifeCount.start()
bats.start()
pop.start()
rollArea.start()

while(True):
    pass
#Begin GUI Loop
#root.mainloop()
