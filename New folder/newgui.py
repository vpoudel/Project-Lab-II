from tkinter import * #import GUI library
import tkinter.font #import tkinter font
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

def quitgame(): #define the function of Quit button
    exit();
def about(): #define the function of About button
    text="This is where we put our information and" \
             "also some about how to play"
    messagebox.showinfo("About",text)
def startgame():
    #label that says your score
    score=0
    Label1=Label(root, text="Your Score:   "+str(score), fg="red", font=('Helvetica', 44))
    Label1.grid(row=3,column=0)

    
root=Tk()

menu=Menu(root)
root.config(menu=menu)
#file menu
file=Menu(menu)
file.add_command(label='New Game') #command=self.client_new)
file.add_command(label='Quit', command=quitgame)
menu.add_cascade(label='File',menu=file)
#help menu
Help=Menu(menu)
Help.add_command(label='About', command=about)
menu.add_cascade(label='Help', menu=Help)

#start game button and its location
startButton=Button(root,text="Start Game", width=30, height=8, command=startgame)
startButton.grid(row=1, column=0)

#quit button and its location
quitButton=Button(root,text="Quit", width=30, height=8, command=quitgame)
quitButton.grid(row=1, column=1)


# insert image in the frame
load=Image.open("logo.jpg")
load=load.resize((250,250), Image.ANTIALIAS)
render=ImageTk.PhotoImage(load)
img=Label(root,image=render)
img.image=render
img.grid(row=0,column=0)


root.attributes("-fullscreen", True)
root.mainloop()