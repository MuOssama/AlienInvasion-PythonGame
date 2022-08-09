import pygame
import sys
import random
from pygame.sprite import Sprite
from pygame.sprite import Group
pygame.font.init()
clock=pygame.time.Clock()

screen = pygame.display.set_mode((750, 700))
font_type = pygame.font.SysFont('comicsans', 40)
font_typebig = pygame.font.SysFont('comicsans', 100)
infobg = pygame.image.load('images/temp_bg.png')
highscore_image = pygame.image.load('images/score.png')
ship_icon = pygame.image.load ('images/ship.png')

txt_file = open('highscore.txt','r')
highscore = 0
for line in txt_file:
    line = int(line)
    if line > highscore:
        highscore = int(line)
txt_file.close()





class Ship:
    def __init__(self,screen):
        self.screen = screen
        self.ship_image = pygame.image.load('images/ship.png')



        self.ship_rect          =    self.ship_image.get_rect()
        self.screen_rect        =    self.screen.get_rect()

        self.ship_rect.centerx  =    self.screen_rect.centerx
        self.ship_rect.bottom   =    self.screen_rect.bottom
        self.ship_rect.centery  =    self.ship_rect.centery



    def blitme(self):
        self.screen.blit(self.ship_image,self.ship_rect)



class Bullet(Sprite):

    def __init__(self,screen,ship):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/bullet.png')
        self.bullet_rect = self.image.get_rect()
        self.bullet_rect.centerx = ship.ship_rect.centerx
        self.bullet_rect.bottom = ship.ship_rect.top+60

    def update(self):
        self.bullet_rect.y -= 20

    def draw_bullet(self):
        screen.blit(self.image,self.bullet_rect)


class Enemy(Sprite):

    def __init__(self,screen,x,y):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/enemy.png')
        self.enemy_rect = self.image.get_rect()
        self.enemy_rect.centerx = x
        self.enemy_rect.centery = y

    def update(self):
        self.enemy_rect.centery += 1


    def draw_enemy(self):
        screen.blit(self.image,self.enemy_rect)

clock=pygame.time.Clock()


def run_game():
    pygame.init()
    # definitions
    velocity = 3
    current_time = 0
    lives = 3
    score = 0
    pygame.display.set_caption('Space Invasion')
    pygame.display.set_icon(ship_icon)
    bg = pygame.image.load('images/background.png')
    ship = Ship(screen)


    # bullet
    bullet_group = Group()

    # enemy
    enemy_group = Group()


    

    while True:
        current_time = pygame.time.get_ticks()
        screen.blit(bg,(0,0))
        keys=pygame.key.get_pressed()
        bullet = Bullet (screen, ship)
        enemy = Enemy (screen, x=random.randint (30, 700), y=random.randint (20, 60))
        score_label = font_type.render (f'Score: {str (score)}', 1, (255, 255, 255))
        score_labelbig = font_typebig.render (f'Score: {str (score)}', 1, (255, 255, 255))

        lives_label = font_type.render (f'Lives: {str (lives)}', 1, (255, 255, 255))
        gameover = font_typebig.render ("GAMEOVER", 1, (255, 255, 255))
        start = font_typebig.render (f"{4-int(current_time/1000)}", 1, (255, 255, 255))
        start_font = font_typebig.render('START!',1,(255,255,255))
        highscorer = font_typebig.render(f'HIGHSCORE: {highscore}',1,(255,100,100))

        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                  sys.exit ()
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                     bullet_group.add (bullet)


        if keys[pygame.K_LEFT] and  ship.ship_rect.centerx > 30:
                  ship.ship_rect.centerx -= velocity

        if keys[pygame.K_RIGHT] and  ship.ship_rect.centerx < 720:
                  ship.ship_rect.centerx += velocity

        if keys[pygame.K_UP] and ship.ship_rect.centery>30:
                  ship.ship_rect.centery-=velocity

        if keys[pygame.K_DOWN] and ship.ship_rect.centery<660:
            ship.ship_rect.centery+=velocity

        if current_time % 60== 0 :
            enemy_group.add (enemy)


        for bullet in bullet_group.sprites():
            bullet.draw_bullet()


            if bullet.bullet_rect.y < 20:
                bullet.kill()

        for enemy in enemy_group.sprites():
            enemy.draw_enemy()
            if enemy.enemy_rect.colliderect(bullet.bullet_rect):
                bullet.kill()
                enemy.kill()
                score = score+50
            if ship.ship_rect.colliderect (enemy.enemy_rect):
                lives -= 1
                enemy.kill ()

            if enemy.enemy_rect.y>700:
                enemy.kill()
                lives -= 1

        ship.blitme()
        enemy_group.update()
        bullet_group.update()

        if lives <= 0:
            screen.fill ((0, 0, 0))
            screen.blit (gameover, (180, 320))
            enemy.kill()
            if highscore < score:
               put_score = open('highscore.txt','w')
               put_score.write(str(score))
        screen.blit (lives_label, (10, 10))
        screen.blit (score_label, (580, 10))
        if current_time < 5000:
            enemy.kill()
            screen.blit (infobg, (0, 0))
            screen.blit (highscorer, (50, 200))
            if current_time < 5000 and int(current_time/1000) !=4:
                screen.blit (start, (350,300))

            if int(current_time/1000) ==4:
                screen.blit(start_font ,(260,300))
        if highscore < score and lives<=0:
            screen.blit (highscore_image, (0, 0))
            screen.blit (score_labelbig,(160,370))

        clock.tick(90)
        pygame.display.update()






run_game()