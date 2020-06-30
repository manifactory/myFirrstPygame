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
TILE_SIZE = 16

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
clicking = False

player_location = [50,50]
player_momentum = [0,0]
player_rect = pygame.Rect(player_location[0]-player_image.get_width()/4, player_location[1], player_image.get_width()/2, player_image.get_height())
print(player_rect)

canjump = True

camera = [0,0]
camera_center = [0,0]

fullscreen = False

framlate = 60
last_time = pygame.time.get_ticks()

font = pygame.font.SysFont(None, 20)
click = False

particles = []

mainClock = pygame.time.Clock()

#맵 데이터

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def load_map(path):
    f = open(path,'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    map_data = []
    for row in data:
        map_data.append(list(row))
    map_data = [list(map(int,line)) for line in map_data]
    print(map_data)
    return map_data

test_map = load_map('./data/map/test.txt')

def load_map_particle(map):
    map_data={}
    y=0
    for line in map:
        x=0
        for tile in line:
            if tile != 0:
                map_data[str(x) + ';' + str(y)] = [x,y,tile]
            x+=1
        y+=1
    return map_data

tile_map = load_map_particle(test_map)

def load_chunk(map_data):
    pass

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

#game loop
def GAME_SCENE():
    global last_time, screen,display, WINDOW_SIZE,DISPLAY_SIZE, fullscreen, player_rect, tile_map ,move_up,move_down,move_left,move_right

    last_time =  pygame.time.get_ticks()
    move_right = False
    move_left = False
    move_up = False
    move_down = False
    press_right = False
    press_left = False
    press_up = False
    press_down = False
    clicking = False

    running = True
    while running:

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
        for tile in tile_map:
            x,y,tile_form=tile_map[tile]
            if tile_form == 1:
                display.blit(grass_img,[x*16-camera[0],y*16-camera[1]])
            if tile_form == 2:
                display.blit(dirt_img,[x*16-camera[0],y*16-camera[1]])
            if tile_form == 3: #나중에 이미지 플렛폼으로 변환
                display.blit(grass_img,[x*16-camera[0],y*16-camera[1]])
            if tile_form != 0:
                tiles.append([pygame.Rect(x*16,y*16,16,2 if tile_form==3 else 16),'platform' if tile_form==3 else 'block'])

        """tiles=[]
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
            y+=1"""

        #paritcle
        # [[location],[momentum],timer]
        #particles.append([[100, 100], [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5], random.randint(4, 6), (255,0,0)])

        for particle in sorted(particles,reverse=True):
            particle[0][0] += particle[1][0]
            loc_str = str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE))
            if loc_str in tile_map:
                particle[1][0] = -0.7 * particle[1][0]
                particle[1][1] *= 0.95
                particle[0][0] += particle[1][0] * 2
            particle[0][1] += particle[1][1]
            loc_str = str(int(particle[0][0] / TILE_SIZE)) + ';' + str(int(particle[0][1] / TILE_SIZE))
            if loc_str in tile_map:
                particle[1][1] = -0.7 * particle[1][1]
                particle[1][0] *= 0.95
                particle[0][1] += particle[1][1] * 2
            particle[2] -= 0.035
            particle[1][1] += 0.15
            pygame.draw.circle(display, particle[3], [int(particle[0][0]-camera[0]),int(particle[0][1]-camera[1])], int(particle[2]))
            if particle[2] <= 0:
                particles.remove(particle)


        #bouncing
        """if player_location[1] > WINDOW_SIZE[1]-player_image.get_height():
            player_momentum[1] = -player_momentum[1]
        else:
            player_momentum[1] += 0.98"""

        #moving
        player_movement = [0,0]
        if move_right:
            player_movement[0] += 3 * dt
        if move_left:
            player_movement[0] -= 2 * dt
        player_momentum[1] += 1
        player_movement[1] += player_momentum[1] * dt #중력 흉내
        """if player_momentum[1] >= 3:
            player_momentum[1] = 3"""

        #moving rect
        player_rect, collisions = check_movement_collide(player_rect,[(player_movement[0]),(player_movement[1])],tiles)
        if collisions['bottom'] == True:
            canjump = True
            player_momentum[1]=0

        """player_rect_copy = pygame.Rect(player_rect)
        player_rect_copy.x-=camera[0]
        player_rect_copy.y-=camera[1]
        pygame.draw.rect(display,(250,50,0),player_rect_copy)"""
        display.blit(player_image,[player_rect.x-camera[0]-int(player_rect.width/2),player_rect.y-camera[1]])


        """for tile in tiles:
            pygame.draw.rect(display,(255,0,0),tile[0])"""

        #event loop
        for event in pygame.event.get():
            if event.type==VIDEORESIZE:
                if not fullscreen:
                    DISPLAY_SIZE = (event.w/2,event.h/2)
                    display = pygame.Surface(DISPLAY_SIZE)
                    WINDOW_SIZE=(event.w,event.h)
                    screen = pygame.display.set_mode((WINDOW_SIZE), pygame.RESIZABLE)
                last_time =  pygame.time.get_ticks()

            if event.type==QUIT: #종료 이벤트
                pygame.quit()
                sys.exit()

            if event.type==KEYDOWN: #키 다운 이벤트
                if event.key == K_ESCAPE:
                    running = False

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
                    last_time =  pygame.time.get_ticks()

                if event.key == K_LEFT:
                    move_left=True
                if event.key == K_RIGHT:
                    move_right=True
                if event.key == K_UP:
                    if canjump == True:
                        for i in range(20):
                            particles.append([[player_rect.centerx,player_rect.centery+player_rect.height/2], [random.randint(0, 20) / 20 - 0.5, random.randint(0, 40)/20], random.randint(2, 3), (155,118,83)])
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

def OPTION_SCENE():
    pass

#menu
def MAINMENU_SCENE():
    global screen, click
    while True:

        screen.fill((0,0,0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                GAME_SCENE()
        if button_2.collidepoint((mx, my)):
            if click:
                OPTION_SCENE()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

MAINMENU_SCENE()

input()
