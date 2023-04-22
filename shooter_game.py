from pygame import *
from random import *
from time import time as timer

font.init()
font2 = font.Font(None, 25)
font3 = font.Font(None, 100)

win = font3.render('You Win',True,(255,235,45))
lose = font3.render('You Lose',True,(245, 245, 245))

score = 0
lost = 0
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width,  player_hight):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_hight))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed       
    def fire(self):
        bullet = Bullet("224681.png", self.rect.centerx, self.rect.top, 3, 20,  40)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_hight:
            self.rect.x = randint(80, win_width - 80)              
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed    
        if self.rect.y < -5:
            self.kill()       



monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 700 - 80), -40, randint(1, 3), 50, 40)
    monsters.add(monster) 

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(0, 3):
    asteroid = Enemy('asteroid.png', randint(80, 700 - 80), -40, randint(1, 3), 60, 60)
    asteroids.add(asteroid) 

win_width = 700
win_hight = 500
window = display.set_mode((win_width, win_hight))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_hight))

player = Player('rocket.png', 50, 425, 15, 65, 65)

game = True
finish = False
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

rel_time = False
num_fire = 0
last_time = timer()
now_time = timer()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if finish != True:

        window.blit(background,(0, 0))

        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Идёт перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        if sprite.spritecollide(player, monsters, False) or life ==0:
            finish = True
            window.blit(lose, (200, 200))

        if sprite.spritecollide(player, monsters, False) or lost >=10:
            finish = True
            window.blit(lose, (200, 200))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 700 - 80), -40, randint(1, 3), 50, 45)
            monsters.add(monster) 
        
        collides = sprite.spritecollide(player, asteroids, True, False)
        for c in collides:
            life -= 1
            asteroid = Enemy('asteroid.png', randint(80, 700 - 80), -40, randint(1, 3), 60, 60)
            asteroids.add(asteroid) 

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_life = font2.render("Жизни: " + str(life), 1, (255, 255, 255))
        window.blit(text_life, (10, 80))
        
    display.update()
    clock.tick(FPS) 