

#Juggling Dog
import random
import pygame

#initialize pygame
pygame.init()

#GAME CONSTANTS
GAME_FOLDER = 'D:/python project/game dev/art_of_game_development/game_4/'
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 700
FPS = 60
DOG_VELOCITY = 10
BALL_VELOCITY = 5
BUFFER_DISTANCE = -200

GOLDEN = pygame.Color(255,201,14)
RED = pygame.Color(255,0,0)
BLUE = pygame.Color(0,0,255)

MAX_LIVES = 5

#create a window
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Juggling Dog')

#background
background_image = pygame.transform.scale( pygame.image.load(GAME_FOLDER + 'background.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.mixer.music.load(GAME_FOLDER + 'background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#game assets
dog_left = pygame.image.load(GAME_FOLDER+ 'dog_left.png')
dog_right = pygame.image.load(GAME_FOLDER+ 'dog_right.png')
dog = dog_right
dog_rect = dog.get_rect()
dog_rect.bottom = WINDOW_HEIGHT
dog_rect.centerx = WINDOW_WIDTH//2

ball = pygame.image.load(GAME_FOLDER + 'ball.png')
ball_rect = ball.get_rect()
ball_rect.top = BUFFER_DISTANCE
ball_rect.left = random.randint(0, WINDOW_WIDTH- ball_rect.width)

#sounds
loss = pygame.mixer.Sound(GAME_FOLDER + 'loss.wav')
loss.set_volume(0.5)
bounce = pygame.mixer.Sound(GAME_FOLDER + 'bounce.mp3')

#game values
change_x = 0
change_y = BALL_VELOCITY
cnt =0
y_multiples = [-1,-1/2,-1/4, 1/4,1/2, 1]
y_interval = FPS//6
multiple_index = 0
score = 0
lives = MAX_LIVES
game_status = 1

bounce_ball = False
running = True
clock = pygame.time.Clock()

#game_texts
game_font_big = pygame.font.Font(GAME_FOLDER +'SunnyspellsRegular.otf',60)
game_font = pygame.font.Font(GAME_FOLDER +'SunnyspellsRegular.otf', 40)

game_title = game_font_big.render('Juggling Dog', True, GOLDEN)
game_title_rect = game_title.get_rect()
game_title_rect.centerx = WINDOW_WIDTH//2
game_title_rect.top = 10

player_lives = game_font.render('Lives: ' + str(lives), True, GOLDEN)
player_lives_rect = player_lives.get_rect()
player_lives_rect.left = 10
player_lives_rect.top = 10

player_score = game_font.render('Score: ' + str(score), True, GOLDEN)
player_score_rect = player_score.get_rect()
player_score_rect.right = WINDOW_WIDTH -10
player_score_rect.top = 10

game_ends = game_font_big.render('GAME ENDS!!!', True, RED)
game_ends_rect = game_ends.get_rect()
game_ends_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

game_restart = game_font.render('Press r to Restart, q to Quit', True, BLUE)
game_restart_rect = game_restart.get_rect()
game_restart_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 +60)

made_by = game_font.render('#NITINYADAVAHIR',True,RED)
made_by_react = made_by.get_rect()
made_by_react.left = 1050
made_by_react.top =657

#main game loop (defines the life of the game)
while running:
    #blit the background
    display_surface.blit(background_image, (0,0))
    display_surface.blit(made_by,made_by_react)

    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            running = False

    if game_status == 1:
        if bounce_ball:
            if cnt < FPS:
                ball_rect.left += change_x #x_path
                ball_rect.top += change_y * y_multiples[multiple_index] #y_path
                cnt+=1
                if cnt % y_interval == 0:
                    multiple_index+=1
            else:
                bounce_ball = False
        else:
            ball_rect.top+= change_y
            ball_rect.left += change_x

        #continuous key movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            dog = dog_left
            if dog_rect.left >=0:
                dog_rect.left-= DOG_VELOCITY
        if keys[pygame.K_RIGHT]:
            dog = dog_right

            if dog_rect.right <= WINDOW_WIDTH:
                dog_rect.left += DOG_VELOCITY

        if dog_rect.colliderect(ball_rect):
            change_x = random.randint(3,6)
            change_y = change_x * 3
            cnt = 0
            multiple_index = 0
            bounce_ball = True
            bounce.play()
            score+=1
            player_score = game_font.render('Score: ' + str(score), True, GOLDEN)

            if dog == dog_left:
                change_x = -change_x
            else:
                change_x = +change_x


        if ball_rect.bottom > WINDOW_HEIGHT:
            loss.play()
            #a new ball should be presented
            ball_rect.top = BUFFER_DISTANCE
            ball_rect.left = random.randint(0, WINDOW_WIDTH- ball_rect.width)
            change_x = 0
            change_y = BALL_VELOCITY
            multiple_index = 0
            lives-=1
            player_lives = game_font.render('Lives: ' + str(lives), True, GOLDEN)

            if lives == 0:
                #game ends
                game_status = 2
                pygame.mixer.music.stop()


        # blit the assets
        display_surface.blit(dog, dog_rect)
        display_surface.blit(ball, ball_rect)

    elif game_status == 2:
        display_surface.blit(game_ends, game_ends_rect)
        display_surface.blit(game_restart, game_restart_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            change_x = 0
            change_y = BALL_VELOCITY
            cnt = 0
            multiple_index = 0
            score = 0
            player_score = game_font.render('Score: ' + str(score), True, GOLDEN)
            lives = MAX_LIVES
            player_lives = game_font.render('Lives: ' + str(lives), True, GOLDEN)
            game_status = 1
            bounce_ball = False
            pygame.mixer.music.play(-1)
        elif keys[pygame.K_q]:
            running = False

    #blit the hud
    display_surface.blit(game_title, game_title_rect)
    display_surface.blit(player_lives, player_lives_rect)
    display_surface.blit(player_score, player_score_rect)


    #update the display
    pygame.display.update()

    #Moderate the loop's iteration rate (cooperative multitasking)
    #Game runs at the same speed over different CPU's
    clock.tick(FPS)

#quit pygame
pygame.quit()