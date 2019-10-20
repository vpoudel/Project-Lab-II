
#all reqd for gui class
from tkinter import * #import GUI library
import tkinter.font #import tkinter font
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk


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
root.state('zoomed')
app=App(root)
root.mainloop()
