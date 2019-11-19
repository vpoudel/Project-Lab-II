import pygame #sound

pygame.mixer.pre_init(44100, -16, 2, 4096) #frequency, size, channels, buffersize
pygame.init() #turn all of pygame on.

soundObj=pygame.mixer.Sound("bell_ding.wav")
soundObj.play()