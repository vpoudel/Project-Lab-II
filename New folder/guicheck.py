from tkinter import *
from PIL import Image,ImageTk
from threading import Thread
import RPi.GPIO as GPIO # import RPi GPIO library
from playsound import playsound #library for playing sound
import time


class App():
    def __init__(self, master):
        #initialization
        global score
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
        my_score=StringVar(value=score)
        label=Label(frame, textvariable= my_score, bg='white', font=("Times", 36, "bold"))
        label.place(relheight=1, relwidth=1)

root =Tk()
score=10000
time.sleep(5)
score=2000
root.state('zoomed')
app=App(root)
root.mainloop()


class playfield_parts():

    def pop_bumpers():
        if (GPIO.input(14)==GPIO.HIGH): #if ball touches pop bumper1,2,3,4 -->or gated pop bumpers
            score=score+100
            playsound('bumpers.mp3', block=False)

    def targets():
        if(GPIO.input(15)==GPIO.HIGH):  #if ball hits targets -->or gated targets
            score=score+1000
            playsound('target.mp3', block=False)

    def area1():
        if GPIO.input(18)==GPIO.HIGH:   #if ball rolls over area1
            score=score+200
            playsound('area.mp3', block=False)

    def area2():
        if GPIO.input(23)==GPIO.HIGH:   #if ball rolls over area3
            score=score+300
            playsound('area.mp3', block=False)

    def area3():
        if GPIO.input(24)==GPIO.HIGH:   #if ball rolls over area3
            score=score+500
            playsound('area.mp3', block=False)

    if __name__ == "__main__":
        Thread(target=pop_bumpers).start()
        Thread(target=targets).start()
        Thread(target=area1).start()
        Thread(target=area2).start()
        Thread(target=area3).start()
