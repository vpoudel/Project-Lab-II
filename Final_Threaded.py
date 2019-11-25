import RPi._GPIO as GPIO
from threading import Thread
import time
#import sys

#all reqd for gui class
import tkinter as tk  #import GUI library
from PIL import Image, ImageTk
from tkinter import messagebox
import pygame #sound

GPIO.setmode(GPIO.BOARD) #use physical pin numbering
GPIO.setwarnings(False) #disable warnings

chan_list1=[3,11,29,31,32,33]

##Setup for input & output pins
#3 Left Flipper Input (EOS Switch In) #5 Right Flipper Input (EOS Switch In)
 #7 Left Flipper Output (PWM)   #8 Right Flipper Output (PWM)
 #10,11,12,13 Pop Bumpers (Points)
GPIO.setup(chan_list1,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   
GPIO.setup([7,13],GPIO.OUT)
#Set PWM on pins 7 & 8 to 1,000 Hz. Start at 50% PWM
pwm1=GPIO.PWM(7, 1000)
pwm2=GPIO.PWM(13, 1000)
pwm1.start(100)
pwm2.start(100)

##input channels for playfield_parts
chan_list2=[15,16,18,19,21,22,23]
GPIO.setup(chan_list2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)     #Slingshot 1 Input (Points)
#Initialize Sounds
pygame.mixer.pre_init(44100, -16, 2, 4096) #frequency, size, channels, buffersize
pygame.mixer.init() #turn all of pygame on.


#high score display
file=open("score.txt","r")
topscore=(file.readline())
topscore=int(topscore)
file.close()

score=0
life=3
curr_score=0
class GPIO_():
    def Lives(self):
        while(True):
            global life,score
            if(GPIO.input(23)==GPIO.HIGH):  #If a ball is lost, tell display to remove a life
                if (life>0):
                    life=life-1
                elif life==0:
                    curr_score=score
                    score=0
                    life=0
                time.sleep(0.5)
                

    def left_flipper(self):
        while (True):
                if(GPIO.input(15)==GPIO.LOW):
                    pwm1.ChangeDutyCycle(10)
                else:
                    pwm1.ChangeDutyCycle(100)
                    
    def right_flipper(self):
        while (True):
            if (GPIO.input(11)==GPIO.LOW):
                pwm2.ChangeDutyCycle(10)
            else:
                pwm2.ChangeDutyCycle(100)

    def pop_bumpers1(self):
        while (True):
            if (GPIO.input(29)==GPIO.HIGH): #if ball touches the pop bumpers
                global score
                score=score+500
                print('Pin 29 Pop bumper')
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.15)
                
    def pop_bumpers2(self):
        while (True):
            if (GPIO.input(31)==GPIO.HIGH): #if ball touches the pop bumpers
                global score
                score=score+500
                print('Pin 31 Pop bumper')
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.15)
        
    def pop_bumpers3(self):
        while (True):
            if (GPIO.input(32)==GPIO.HIGH): #if ball touches the pop bumpers
                global score
                score=score+500
                print('Pin 32 Pop bumper')
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.15)
                
    def pop_bumpers4(self):
        while (True):
            if (GPIO.input(33)==GPIO.HIGH): #if ball touches the pop bumpers
                global score
                score=score+500
                print('Pin 33 Pop bumper')
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.15)
    def area(self):
        while (True):
            global score
            if GPIO.input(18)==GPIO.HIGH:
                score=score+500
                print('Pin 18 Area')
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.25)
            if GPIO.input(19)==GPIO.HIGH:
                score=score+300
                print('Pin 19 Area')
                soundObj=pygame.mixer.Sound("bell_ding.wav")
                soundObj.play()
                time.sleep(0.25)
            if GPIO.input(21)==GPIO.HIGH:
                score=score+1000
                print('Pin 21 Area')
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
        #label for text Score
        scorelabel=tk.Label(master,text='Score',fg='white',bg='black',font=("Times", 45, "bold"))
        scorelabel.place(relx=0.46,rely=0.39)
        
        #label for top Score
        texta=tk.Label(master,text='Top Score: ',fg='white',bg='black',font=("Times", 45, "bold"))
        texta.place(relx=0.4,rely=0)
        self.top_score_label=tk.Label(master,text=topscore,fg='white',bg='black',font=("Times", 45, "bold"))
        self.top_score_label.place(relx=0.55,rely=0)
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
        global life,score,topscore
        self.label1['text']='Lives: '+str(life)
        self.label2['text']=str(score)
        if (life==0 & score==0):
            self.label1['text']='Lives: '+ str(life)
            self.label2['text']=str(score)
            popup = tk.Tk()
            popup.wm_title("Pinball")
            popup.geometry("%dx%d+0+0" % (w, h))
            label = tk.Label(popup, text="Game Over", font=("Times", 100, "bold"))
            label.pack(side="top", fill="x", pady=10)
            popup.after(3000,lambda:popup.destroy())
            life=3
            if curr_score>topscore:
                file1=open("score.txt","w")
                str_curr_score=str(curr_score)
                file1.write(str_curr_score)
                file1.close()
                topscore=curr_score
            self.top_score_label['text']=str(topscore)
            
        try:
            root.after(300,app.score_update)
        except:
            pass

    def close_app(self):
        root.destroy()
        exit()

root = tk.Tk()
app=App(root)
w,h=root.winfo_screenwidth(),root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
if __name__=="__main__":
    Thread(target=GPIO_().pop_bumpers1).start()
    Thread(target=GPIO_().pop_bumpers2).start()
    Thread(target=GPIO_().pop_bumpers3).start()
    Thread(target=GPIO_().pop_bumpers4).start()            
    Thread(target=GPIO_().area).start()
    Thread(target=GPIO_().left_flipper).start()
    Thread(target=GPIO_().right_flipper).start()
    Thread(target=GPIO_().Lives).start()
app.score_update()
root.protocol('WM_DELETE_WINDOW',app.close_app)
root.mainloop()



