import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() #pygame 초기화

pygame.display.set_caption('My Pygame Window')

WINDOW_SIZE = (400,400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) #윈도우 스크린 초기화

while True: #main code

    for event in pygame.event.get(): #이벤트 루프
        if event.type==QUIT: #종료 이벤트
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
