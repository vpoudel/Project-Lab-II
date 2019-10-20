from multiprocessing import Process
from threading import Thread
import time
import RPi.GPIO as GPIO # import RPi GPIO library
from playsound import playsound	#library for playing sound

#all reqd for gui class
from tkinter import * #import GUI library
import tkinter.font #import tkinter font
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk



channelA_inputs=[14,15,18,23,24,8,7,12,16,20,21]
channelB_outputs=[2,3,4,17,27,22,10,9,11,5,6,13,19,26]

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

##input channels for playfield_parts
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##input/output for PWM class
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(2, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(3, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

pwm1=GPIO.PWM(2, 65.8e+6)
pwm2=GPIO.PWM(3, 65.8e+6)
pwm1.start(100)
pwm2.start(100)


class PWM():

	def flipperleft():
		while True:
			if (GPIO.input(16)==GPIO.HIGH):
				time.sleep(0.25)
				if (GPIO.input(16)==GPIO.HIGH):
					pwm1.ChangeDutyCycle(50)

	def flipperright():
		while True:
			if (GPIO.input(20)==GPIO.HIGH):
				time.sleep(0.25)
				if (GPIO.input(20)==GPIO.HIGH):
					pwm2.ChangeDutyCycle(50)
	if __name__ == "__main__":
		Thread(target=flipperleft).start()
		Thread(target=flipperright).start()



class playfield_parts():
	def pop_bumpers():
		if (GPIO.input(14)==GPIO.HIGH):	#if ball touches pop bumper1,2,3,4 -->or gated pop bumpers
			score=score+100
			playsound('bumpers.mp3', block=False)

	def targets():
		if(GPIO.input(15)==GPIO.HIGH):	#if ball hits targets -->or gated targets
			score=score+1000
			playsound('target.mp3', block=False)

	def area1():
		if GPIO.input(18)==GPIO.HIGH:	#if ball rolls over area1
			score=score+200
			playsound('area.mp3', block=False)

	def area2():
		if GPIO.input(23)==GPIO.HIGH:	#if ball rolls over area3
			score=score+300
			playsound('area.mp3', block=False)

	def area3():
		if GPIO.input(24)==GPIO.HIGH:	#if ball rolls over area3
			score=score+500
			playsound('area.mp3', block=False)

	if __name__ == "__main__":
		Thread(target=pop_bumpers).start()
		Thread(target=targets).start()
		Thread(target=area1).start()
		Thread(target=area2).start()
		Thread(target=area3).start()



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




if __name__ == "__main__":
	Process(target=GUI).start()
	Process(target=playfield_parts).start()
	Process(target=PWM).start()









%In case I loose GUI
from tkinter import *
from PIL import Image,ImageTk



class App:
	def __init__(self, master):
		self.master=master
		width=master.winfo_screenwidth()
		height = master.winfo_screenheight()


		#Frame and Canvas
		frame=Frame(master).pack()
		Canvas(frame, height=height, width=width).pack(fill=BOTH, expand=1)
		self.back_image=ImageTk.PhotoImage(file="wallpin.jpg")
		Label(frame, image=self.back_image).place(relwidth=1,relheight=1)

		#another canvas
		Canvas(frame, height=height/4, width=width/4, bg = "blue").pack()
		#labels
		#self.scoreLabel=Label(frame, height=width)
#top.attributes("-fullscreen",True)
root =Tk()
root.state('zoomed')
app=App(root)
root.mainloop()




		def scorefunc():
			global score
			Label(frame, text="Your Score:   "+str(score), fg="red", font=('Helvetica', 44))
