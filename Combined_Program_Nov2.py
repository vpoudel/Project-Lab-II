import RPi.GPIO as GPIO
from threading import Thread, Timer
import time
from queue import Queue

#all reqd for gui class
from tkinter import * #import GUI library
import tkinter.font #import tkinter font
from PIL import Image, ImageTk

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
class RepeatingTimer(object):
    def __init__(self,interval,f,*params):
        self.interval = interval
        self.f = f
        self.args = params
        self.timer = Timer(self.interval,self.callback)

    def callback(self):
        self.f(*self.args)

    def cancel(self):
        self.timer.cancel()

    def start(self):
        self.timer.start()

    def is_alive(self):
        return self.timer.is_alive()

class GPIO_pins():
    def Lives(app):
        while(True):
            if(GPIO.input(22)==GPIO.HIGH):  #If a ball is lost, tell display to remove a life
                app.livesQ.put(-1)
                time.sleep(1.5)                 #Sleep to ignore extra bouncing

    def flippers():
            ##If there is a high to low transition, the flipper bat is up. Wait 200ms then lower PWM.
            ##  else the flipper bat is down, return pwm to 100%

            ##  Nested if statements to ensure that each individual pwm can change from 50% to 100%
            ##  independently from each other

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

    def boolTimer(*timeUp):
        timeUp = False

    def pop_bumpers(app):
        timeUp = False
        zeroCount = 0
        lowHigh = True  #Start by looking for a low to high transition (switch pressed)
        highLow = False #Use for after low to high transition detected
        alarm = RepeatingTimer(0.01,GPIO_pins.boolTimer,timeUp)

        while (True):
            if ((GPIO.input(10) or GPIO.input(11) or GPIO.input(12) or GPIO.input(13))==GPIO.HIGH): #if ball touches any of the 4 pop bumpers
                #Nested ifs to track only the transitions we are looking for
                print("High Detected")
                print(zeroCount)
                if(lowHigh):
                    if ((GPIO.input(10) or GPIO.input(11) or GPIO.input(12) or GPIO.input(13))==GPIO.HIGH):
                        lowHigh=False
                        highLow=True
                        if(alarm.is_alive()):
                            alarm.cancel()

                            alarm = RepeatingTimer(0.1,GPIO_pins.boolTimer,timeUp)
                            alarm.start()
                        else:
                            alarm = RepeatingTimer(0.1,GPIO_pins.boolTimer,timeUp)
                            alarm.start()

                if(highLow):
                    if((GPIO.input(10) or GPIO.input(11) or GPIO.input(12) or GPIO.input(13))==GPIO.LOW):
                        lowHigh=True
                        highLow=False
                        zeroCount=zeroCount+1   #only count high to low transitions AFTER
                                                #a low to high transition has occured
                        if not(alarm.is_alive()):
                            alarm.cancel()

                            alarm = RepeatingTimer(0.1,GPIO_pins.boolTimer,timeUp)
                            alarm.start()
                        else:
                            alarm = RepeatingTimer(0.1,GPIO_pins.boolTimer,timeUp)
                            alarm.start()

                if(zeroCount>=3):   #Only increase score after a certain number of zeros
                    app.pointsQ.put(500)
                    zeroCount=0     #Reset zeroCount
                    lowHigh=True    #Make sure Booleans are correctly reset
                    highLow=False

                if(timeUp):
                    zeroCount=0     #Reset zeroCount
                    lowHigh=True    #Make sure Booleans are correctly reset
                    highLow=False
                    timeUp=False    #Reset Timer variable

#    def slingshots():
#        while (True):
#            if ((GPIO.input(15) or GPIO.input(16))==GPIO.HIGH):
#                print("slingshots")
#                global score
#                score=score+200
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

class App():
    def __init__(self, master):
        #initialization
        self.pointsQ = Queue(maxsize=0) #infinite size queue
        self.livesQ = Queue(maxsize=0)
        self.lives = 3                  #Start with 3 lives
        self.lostBall = False           #Show that a ball is lost = false

        self.master=master
        scrwidth=master.winfo_screenwidth()
        scrheight = master.winfo_screenheight()
        master.title("Pinball")

        #canvas large
        Canvas(master).pack()
        self.back_image=ImageTk.PhotoImage(Image.open('wall.jpg'))
        Label(master, image=self.back_image).place(relwidth=1,relheight=1)

        #Frame inside canvas
        frame=Frame(master, height=scrheight/10, width=scrwidth/4, bg='white', bd=5)
        frame.place(relx=.5, rely=.5, anchor="center")
        self.label=Label(frame, text= '', bg='white', font=("Times", 36, "bold"))
        self.label.place(relheight=1, relwidth=1)

    def HideMessage(self):
        self.lostBall=False

    def score_update(self):
        global score
        tempScore = 0
        tempLives = 0

        try:
            tempScore = self.pointsQ.get_nowait()
        except:
            pass    #Do nothing if an exception is raised
        score = score + tempScore

        try:
            tempLives = self.livesQ.get_nowait()
        except:
            pass

        if(tempLives==-1):
            self.lives = self.lives + tempLives
            self.lostBall = True
            t = RepeatingTimer(3,self.HideMessage) #Create and run a timer
            t.start()

        if(self.lives==0):
            self.label['text']="YOU LOSE"
        elif(self.lostBall):
            self.label['text']="Ball Lost"
        else:
            self.label['text']=str(score)

            self.master.update()

    def close(self,e):  #e is a variable placeholder that is passed in when using __.bind
        self.master.destroy()


root = Tk()
root.attributes("-fullscreen", True)
app = App(root)
root.bind("<Escape>", app.close)
root.after(1,app.score_update)

pop = Thread(target=GPIO_pins.pop_bumpers, args=(app,))
lifeCount = Thread(target=GPIO_pins.Lives, args=(app,))
pop.start()
lifeCount.start()
root.mainloop()
