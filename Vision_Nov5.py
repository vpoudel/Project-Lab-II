import RPi._GPIO as GPIO
from threading import Thread
import time

#all reqd for gui class
import tkinter as tk  #import GUI library
from PIL import Image, ImageTk
from tkinter import messagebox
import pygame #sound

GPIO.setmode(GPIO.BOARD) #use physical pin numbering
GPIO.setwarnings(False) #disable warnings

chan_list1=[3,5,10,11,12,13]

##Setup for input & output pins
#3 Left Flipper Input (EOS Switch In) #5 Right Flipper Input (EOS Switch In)
 #7 Left Flipper Output (PWM)   #8 Right Flipper Output (PWM)
 #10,11,12,13 Pop Bumpers (Points)
GPIO.setup(chan_list1,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   
GPIO.setup([7,8],GPIO.OUT)
#Set PWM on pins 7 & 8 to 1,000 Hz. Start at 50% PWM
pwm1=GPIO.PWM(7, 1000)
pwm2=GPIO.PWM(8, 1000)
pwm1.start(50)
pwm2.start(50)

##input channels for playfield_parts
chan_list2=[15,16,18,19,21,22,23]
GPIO.setup(chan_list2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Slingshot 1 Input (Points)
#Initialize Sounds
pygame.mixer.pre_init(44100, -16, 2, 4096) #frequency, size, channels, buffersize
pygame.mixer.init() #turn all of pygame on.

score=0
life=3
class GPIO_():
    def Lives(self):
        while(True):
            if(GPIO.input(23)==GPIO.HIGH):  #If a ball is lost, tell display to remove a life
                global life,score
                if (life>0):
                    life=life-1
                else:
                    life=0
                    score=0
                time.sleep(0.5)
            if ((GPIO.input(3)==GPIO.HIGH) & life==0 & score==0):
                time.sleep(4)
                life=3
                

    def flippers(self):
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

    def pop_bumpers(self):
        while (True):
            if ((GPIO.input(10)==GPIO.HIGH) or (GPIO.input(11)==GPIO.HIGH)
                or (GPIO.input(12)==GPIO.HIGH) or (GPIO.input(13)==GPIO.HIGH)): #if ball touches the pop bumpers
                global score
                score=score+500
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.15)

    def area(self):
        while (True):
            global score
            if GPIO.input(18)==GPIO.HIGH:
                score=score+500
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.25)
            if GPIO.input(19)==GPIO.HIGH:
                score=score+300
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.25)
            if GPIO.input(21)==GPIO.HIGH:
                score=score+1000
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.25)

class App():
    def __init__(self, master):
        self.master=master
        master.title("Pinball")
        scrwidth=master.winfo_screenwidth()
        scrheight = master.winfo_screenheight()

        #canvas large
        tk.Canvas(master).pack()
        self.back_image=ImageTk.PhotoImage(Image.open('wall.jpg'))
        tk.Label(master, image=self.back_image).place(relwidth=1,relheight=1)

        #label for lives
        frame1=tk.Frame(master, height=scrheight/7, width=scrwidth/8, bg='white', bd=5)
        frame1.place(relx=1.0, rely=0.0, anchor="ne")
        self.label1=tk.Label(frame1, text='', bg='white', font=("Times", 36, "bold"))
        self.label1.place(relheight=1,relwidth=1)
        
        #Frame inside canvas
        frame2=tk.Frame(master, height=scrheight/10, width=scrwidth/4, bg='white', bd=5)
        frame2.place(relx=.5, rely=.5, anchor="center")
        self.label2=tk.Label(frame2, text= '', bg='white', font=("Times", 36, "bold"))
        self.label2.place(relheight=1, relwidth=1)

    def score_update(self):
        global life
        global score
        self.label1['text']=str(life)
        self.label2['text']=str(score)
        root.after(100,app.score_update)

        

root = tk.Tk()
app=App(root)
w,h=root.winfo_screenwidth(),root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
if __name__=="__main__":
    Thread(target=GPIO_().pop_bumpers).start()
    Thread(target=GPIO_().area).start()
    Thread(target=GPIO_().flippers).start()
    Thread(target=GPIO_().Lives).start()
app.score_update()
root.mainloop()


