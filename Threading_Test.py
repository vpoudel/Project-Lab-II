from threading import Thread, Timer
import time
from queue import Queue

#all reqd for gui class
from tkinter import * #import GUI library
import tkinter.font #import tkinter font
from PIL import Image, ImageTk

score=0
class GPIO_pins():
    def pop_bumpers(app):
        while (True):
            time.sleep(1)
            app.pointsQ.put(50)

    def slingshots(app):
        while(True):
            time.sleep(2)
            app.pointsQ.put(3)

class App():
    def __init__(self, master):
        #initialization
        self.pointsQ = Queue(maxsize=0) #infinite size queue
        self.pointsQ.put(50)
        
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

    def score_update(self):
        global score
        temp = 0

        try:
            temp = self.pointsQ.get_nowait()
        except:
            pass    #Do nothing if an exception is raised 

        score = score + temp
        self.label['text']=str(score)
        root.after(1,self.score_update)
        root.update()

    def close(self,e):  #e is a variable placeholder that is passed in when using __.bind
        self.master.destroy()

root = Tk()
root.attributes("-fullscreen", True)
app = App(root)
root.bind("<Escape>", app.close)
root.after(1,app.score_update)

pop = Thread(target=GPIO_pins.pop_bumpers, args=(app,))
slingshot = Thread(target=GPIO_pins.slingshots, args=(app,))
pop.start()
slingshot.start()
root.mainloop()
