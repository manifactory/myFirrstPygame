import pygame, sys, random

clock = pygame.time.Clock()

from pygame.locals import *
#pygame 초기화
pygame.init()

#윈도우 스크린 초기화
pygame.display.set_caption('My Pygame Window')
WINDOW_SIZE = (400,400)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)

DISPLAY_SIZE = (200,200)
display = pygame.Surface(DISPLAY_SIZE)

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

canjump = True

camera = [0,0]
camera_center = [0,0]

fullscreen = False

framlate = 60
last_time = pygame.time.get_ticks()

particles = []

#맵 데이터

def load_map(path):
    f = open(path,'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    map_data = []
    for row in data:
        map_data.append(list(row))
    return map_data

test_map = [list(map(int,line)) for line in load_map('./data/map/test.txt')]

print(test_map)

def load_chunk(map_data):
    pass

player_rect = pygame.Rect(player_location[0],player_location[1],player_image.get_width(),player_image.get_height())

def collision_test(rect,tiles):
    hit_list=[]
    for tile in tiles:
        if rect.colliderect(tile[0]):
            hit_list.append(tile)
    return hit_list

def check_movement_collide(rect,movement,tiles):
    collision_type = {'top':False,'bottom':False,'left':False,'right':False}
    rect.x += movement[0]
    for tile,tile_form in collision_test(rect,tiles):
        if movement[0] > 0:
            if tile_form =='block':
                rect.right = tile.left
                collision_type['right']=True
        elif movement[0] < 0:
            if tile_form =='block':
                rect.left = tile.right
                collision_type['left']=True
    rect.y += movement[1]
    for tile,tile_form in collision_test(rect,tiles):
        if movement[1] > 0:
            if tile_form =='block' or (tile_form =='platform' and rect.bottom-movement[1] <= tile.top):
                rect.bottom = tile.top
                collision_type['bottom']=True
        elif movement[1] < 0:
            if tile_form =='block':
                rect.top = tile.bottom
                collision_type['top']=True
    return rect, collision_type



#main code
while True:

    t = pygame.time.get_ticks()
    # deltaTime in framlate tick.
    dt = (t - last_time) / 1000.0 *60
    last_time = t


    display.fill((255,255,255))

    #camera move
    camera[0] += ((player_rect.x - camera[0] - (DISPLAY_SIZE[0]-player_image.get_width())/2)/20 * dt)
    camera[1] += ((player_rect.y - camera[1] - (DISPLAY_SIZE[1]-player_image.get_height())/2)/20 * dt)

    """camera_center = pygame.Vector2(camera[0]-(DISPLAY_SIZE[0]-player_image.get_width())/2, camera[1]-(DISPLAY_SIZE[1]-player_image.get_height())/2)
    camera=pygame.math.Vector2.lerp(pygame.Vector2(player_rect.x,player_rect.y),camera_center,dt)"""


    #draw tile
    tiles=[]
    y=0
    for line in test_map:
        x=0
        for tile in line:
            if tile == 1:
                display.blit(grass_img,[x*16-camera[0],y*16-camera[1]])
            if tile == 2:
                display.blit(dirt_img,[x*16-camera[0],y*16-camera[1]])
            if tile == 3: #나중에 이미지 플렛폼으로 변환
                display.blit(grass_img,[x*16-camera[0],y*16-camera[1]])
            if tile != 0:
                tiles.append([pygame.Rect(x*16,y*16,16,2 if tile==3 else 16),'platform' if tile==3 else 'block'])
            x+=1
        y+=1

    #paritcle
    # [[location],[momentum],timer]
    particles.append([[100, 100], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

    for particle in sorted(particles,reverse=True):
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        pygame.draw.circle(display, (155,118,83), [int(particle[0][0]-camera[0]),int(particle[0][1]-camera[1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)


    #bouncing
    """if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
        player_momentum[1] = -player_momentum[1]
    else:
        player_momentum[1] += 0.98"""

    #moving
    player_movement = [0,0]
    if move_left:
        player_movement[0] -= 2 * dt
    if move_right:
        player_movement[0] += 2 * dt
    player_momentum[1] += 1
    player_movement[1] += player_momentum[1] * dt #중력 흉내
    """if player_momentum[1] >= 3:
        player_momentum[1] = 3"""

    #moving rect
    player_rect, collisions = check_movement_collide(player_rect,[(player_movement[0]),(player_movement[1])],tiles)
    if collisions['bottom'] == True:
        canjump = True
        player_momentum[1]=0

    display.blit(player_image,[player_rect.x-camera[0],player_rect.y-camera[1]])


    """for tile in tiles:
        pygame.draw.rect(display,(255,0,0),tile[0])"""

    #event loop
    for event in pygame.event.get():
        """if event.type==VIDEORESIZE:
            if not fullscreen:
                DISPLAY_SIZE = (event.w/2,event.h/2)
                display = pygame.Surface(DISPLAY_SIZE)
                WINDOW_SIZE=(event.w,event.h)
                screen = pygame.display.set_mode((WINDOW_SIZE), pygame.RESIZABLE)"""

        if event.type==QUIT: #종료 이벤트
            pygame.quit()
            sys.exit()

        if event.type==KEYDOWN: #키 다운 이벤트
            if event.key == K_F4:
                fullscreen = not fullscreen
                if fullscreen == True:
                    DISPLAY_SIZE = (200,200)
                    display = pygame.Surface(DISPLAY_SIZE)
                    WINDOW_SIZE=(screen.get_width(),screen.get_height())
                    screen = pygame.display.set_mode((WINDOW_SIZE), pygame.FULLSCREEN)
                else:
                    DISPLAY_SIZE = (200,200)
                    display = pygame.Surface(DISPLAY_SIZE)
                    WINDOW_SIZE=(screen.get_width(),screen.get_height())
                    screen = pygame.display.set_mode((WINDOW_SIZE), pygame.FULLSCREEN)
                    WINDOW_SIZE=(screen.get_width(),screen.get_height())
                    screen = pygame.display.set_mode((WINDOW_SIZE), pygame.RESIZABLE)

            if event.key == K_LEFT:
                move_left=True
            if event.key == K_RIGHT:
                move_right=True
            if event.key == K_UP:
                if canjump == True:
                    for i in range(20):
                        particles.append([[player_rect.centerx,player_rect.centery+player_rect.height/2], [random.randint(0, 20) / 20 - 0.5, 0.1], random.randint(4, 7)])
                    player_momentum[1] = -10
                    canjump = False
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
input()
