import pygame, sys, os

from math import sin, cos, radians

from pygame.locals import *

window = pygame.display.set_mode((600,600))
pygame.display.set_caption('Test')
screen = pygame.display.get_surface()
robot = "robot.png"
#robot_surf = pygame.image.load(robot)
#screen.blit(robot_surf,(0,0))

def drawArm(screen,startpoints,angle,lenght,width=1):
	x = lenght*cos(radians(angle))
	y = lenght*sin(radians(angle))
	white = (255,255,255)
	pygame.draw.line(screen,white,startpoints,(x,y),width)
	return (x,y)


def input(events):
	for event in events:
		if event.type == QUIT:
			sys.exit(0)
		else:
			print event
	arm1 = drawArm(screen,(0,0),25,100,2)
	RED=(255,0,0)
	#import pdb;pdb.set_trace()
	pygame.draw.circle(screen,RED,(int(arm1[0]),int(arm1[1])),2)
	drawArm(screen,arm1,45,100,2)
	pygame.display.flip()


while True:
	input(pygame.event.get())