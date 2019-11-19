import pygame
import time
from threading import Thread

pygame.mixer.init()
def pop_bumpers():
    soundObj=pygame.mixer.Sound("bell-ding.wav")
    soundObj.play()
    

def pop2():
    time.sleep(0.4)
    soundObj2=pygame.mixer.Sound("bell-ding.wav")
    soundObj2.play()

    


if __name__=='__main__': #start threads asynchronously
        Thread(target=pop_bumpers).start()
        Thread(target=pop2).start()
        