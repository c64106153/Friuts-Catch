import pygame  
import random
from pygame import *
import os

# 遊戲初始化 + 創建視窗
pygame.init()
pygame.mixer.init()
Width=1000
Height=750
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Friuts Catch")


clock = pygame.time.Clock()
FPS=60

lives=3

#新增水果
def new_fruit():
    r=Fruit()
    all_sprites.add(r)
    fruits.add(r) 


def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(None,size)
    text_surface = font.render(text,True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect)

def draw_init():
    draw_text(screen,'Click to start!',64, Width/2,Height*0.75)
    pygame.display.update()
    waiting=True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            play = pygame.mouse.get_pressed()
            if play[0]:
                waiting = False

score = 0

font = pygame.font.Font(None, 50)
pygame.mouse.set_visible(True)

# 載入圖片
background_img=pygame.image.load(os.path.join("pic","background.jpg")).convert()
player_img=pygame.image.load(os.path.join("pic","player.png")).convert()
fruits_imgs=[]
for i in range(1,9):
    fruits_imgs.append(pygame.image.load(os.path.join("pic",f"fruit{i}.png")).convert())

# 載入音樂、音效
catch=pygame.mixer.Sound(os.path.join("sound","catch.mp3"))
catch.set_volume(0.2)
pygame.mixer.music.load(os.path.join("sound","backsound1.mp3"))
pygame.mixer.music.set_volume(0.3)

#設定背景 遊戲圖標
pygame.display.set_icon(player_img)
screen.blit(background_img,(0,0))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives=3
        self.image = pygame.transform.scale(player_img,(170,150))
        self.image.set_colorkey((255,255,255))
        self.rect=self.image.get_rect()
        self.radius = 20
        self.rect.centerx = Width/2
        self.rect.bottom = Height
    def update(self):
        (mouse_x,mouse_y) =pygame.mouse.get_pos()
        self.rect.centerx =mouse_x
        if self.rect.right >Width:
            self.rect.right = Width
        if self.rect.left <0:
            self.rect.left = 0

class Fruit(pygame.sprite.Sprite):     
    def __init__(self):
        

        pygame.sprite.Sprite.__init__(self)
        self.image_ori =random.choice(fruits_imgs)
        self.image_ori.set_colorkey((255,255,255))
        self.image = pygame.transform.scale(self.image_ori,(75,75))
        self.rect=self.image.get_rect()
        self.lives=3

        self.rect.x = random.randrange(100,Width-100)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,5)
    
        
    
    
    def update(self):
        self.rect.y +=self.speedy
        if self.rect.top > Height :
            player.lives-=1
            self.rect.x = random.randrange(0,Width-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,5) 

all_sprites = pygame.sprite.Group()
fruits = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_fruit()

pygame.mixer.music.play(-1)
running = True
show_init=True


# 遊戲迴圈
while running:
    if show_init:
        draw_init()
        show_init = False
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    # 碰撞判定
    hits=pygame.sprite.spritecollide(player,fruits,True,pygame.sprite.collide_circle)
    for hit in hits:
        catch.play()
        new_fruit()
        score+=10

    #gameover後重新設定
    if player.lives== 0:
        show_init=True
        draw_text(screen,'Game Over!! ',100, Width/2,Height/2)
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
           new_fruit()
        score=0
        pygame.mixer.music.play(-1)
    
    #更新遊戲
    screen.fill((0, 0, 0))
    screen.blit(background_img,(0,0))
    draw_text(screen,'Score: '+str(score),50, Width/5,20)
    draw_text(screen,'Lives '+str(player.lives),50, Width-200,20)    
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.update()

pygame.quit()
