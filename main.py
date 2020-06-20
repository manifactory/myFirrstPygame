import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *

#pygame 초기화
pygame.init()

#윈도우 스크린 초기화
pygame.display.set_caption('My Pygame Window')
WINDOW_SIZE = (400,400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

#이미지 리소스
player_image = pygame.image.load('Sprite-0002.png')


#변수 선언
move_right = False
move_left = False
move_up = False
move_down = False

player_location = [50,50]
player_momentum = [0,0.2]

player_rect = pygame.Rect(player_location[0],player_location[1],player_image.get_width(),player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

#main code
while True:
    screen.fill((255,255,255))

    screen.blit(player_image,player_location)

    #bouncing
    if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
        player_momentum[1] = -player_momentum[1]
    else:
        player_momentum[1] += 0.98
    player_location[1] += player_momentum[1]

    #moving
    if move_left:
        player_location[0] -= 4
    if move_right:
        player_location[0] += 4

    #moving rect
    player_rect.x=player_location[0]
    player_rect.y=player_location[1]

    #collider 테스트
    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen,(255,0,0),test_rect)
    else:
        pygame.draw.rect(screen,(0,0,0),test_rect)

    #event loop
    for event in pygame.event.get():

        if event.type==QUIT: #종료 이벤트
            pygame.quit()
            sys.exit()

        if event.type==KEYDOWN: #키 다운 이벤트
            if event.key == K_LEFT:
                move_left=True
            if event.key == K_RIGHT:
                move_right=True
            if event.key == K_UP:
                move_up=True
            if event.key == K_DOWN:
                move_down=True

        if event.type==KEYUP: #키 업 이벤트
            if event.key == K_LEFT:
                move_left=False
            if event.key == K_RIGHT:
                move_right=False
            if event.key == K_UP:
                move_up=False
            if event.key == K_DOWN:
                move_down=False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
