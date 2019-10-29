
from threading import Thread
import time
#all reqd for gui class
from tkinter import * #import GUI library
import tkinter.font #import tkinter font
from PIL import Image
from PIL import ImageTk

score=0
class GPIO_pins():
    def pop_bumpers():
        while (True):
            time.sleep(5)
            global score
            score=score+50

    def slingshots():
        while (True):
            time.sleep(5)
            global score
            score=score+50
    if __name__=='__main__': #start threads asynchronously
        Thread(target=pop_bumpers).start()
        Thread(target=slingshots).start()

class App():
    def __init__(self, master):
        #initialization
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
        self.label['text']=str(score)
        root.after(1,self.score_update)
        root.update()

    def close(self):
        self.root.destroy()


root =Tk()
root.attributes("-fullscreen", True)
app=App(root)
root.bind("<Escape>", app.close)
root.after(1,app.score_update)
root.mainloop()
