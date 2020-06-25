import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
#pygame 초기화
pygame.init()

#윈도우 스크린 초기화
pygame.display.set_caption('My Pygame Window')
WINDOW_SIZE = (400,400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

display = pygame.Surface((200,200))

#이미지 리소스
player_image = pygame.image.load('Sprite-0001.png')

grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
rock_img = pygame.image.load('rock.png')

#변수 선언
move_right = False
move_left = False
move_up = False
move_down = False
press_right = False
press_left = False
press_up = False
press_down = False

player_location = [50,50]
player_momentum = [0,0]


#맵 데이터
test_map = [[0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1],
            [2,2,2,2,2,2,2,2,2,2,2,2],
            [0,0,0,0,0,0,0,0,0,0,0,0]]

player_rect = pygame.Rect(player_location[0],player_location[1],player_image.get_width(),player_image.get_height())

def collision_test(rect,tiles):
    hit_list=[]
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def check_movement_collide(rect,movement,tiles):
    collision_type = {'top':False,'bottom':False,'left':False,'right':False}
    rect.x += movement[0]
    for tile in collision_test(rect,tiles):
        if movement[0] < 0:
            rect.left = tile.left
            collision_type['left']=True
        elif movement[0] > 0:
            rect.left = tile.right
            collision_type['right']=True
    rect.y += movement[1]
    for tile in collision_test(rect,tiles):
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_type['top']=True
        elif movement[1] > 0:
            rect.bottom = tile.top
            collision_type['bottom']=True
    return rect, collision_type


#main code
while True:
    display.fill((255,255,255))

    #draw tile
    tile_rect=[]
    y=0
    for line in test_map:
        x=0
        for tile in line:
            if tile == 1:
                display.blit(grass_img,[x*16,y*16])
            if tile == 2:
                display.blit(dirt_img,[x*16,y*16])
            if tile != 0:
                tile_rect.append(pygame.Rect(x*16,y*16,16,16))
            x+=1
        y+=1


    #bouncing
    """if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
        player_momentum[1] = -player_momentum[1]
    else:
        player_momentum[1] += 0.98"""

    #moving
    player_movement = [0,0]
    if move_left:
        player_movement[0] -= 4
    if move_right:
        player_movement[0] += 4
    player_movement[1] += player_momentum[1] #중력 흉내
    player_momentum[1] += 0.98
    """if player_momentum[1] >= 3:
        player_momentum[1] = 3"""
    #moving rect
    player_rect, collisions = check_movement_collide(player_rect,player_movement,tile_rect)
    if collisions['bottom'] == True:
        player_momentum[1]=0

    for tile in tile_rect:
        pygame.draw.rect(display,(255,0,0),tile)
    display.blit(player_image,[player_rect.x,player_rect.y])

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
                player_momentum[1] = -10
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

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),[0,0])
    pygame.display.update()
    clock.tick(60)
