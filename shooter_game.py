from pygame import *
from random import randint

#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
#fire_sound = mixer.Sound('fire.ogg')



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
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
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1

class Ast(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0



display.set_caption("Shooter")
window = display.set_mode((700, 500))
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()


for i in range(5):
    monster = Enemy("ufo.png", randint(0,620), randint(0,15), 80, 50, randint(3,6))
    monsters.add(monster)

for i in range(3):
    asteroid = Ast("asteroid.png", randint(0,620), randint(0,15), 80, 50, randint(3,6))
    asteroids.add(asteroid)


lost = 0
score = 0
ship = Player("rocket.png", 5, 400, 80, 100, 10)

finish = False
run = True

hp = 3

lose_text = font2.render("Вы проиграли!", 1, (255, 30, 30))
win_text = font2.render("Вы выиграли!", 1, (1, 255, 1))


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if not finish:
        window.blit(background,(0,0))

        text = font1.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))



        if sprite.groupcollide(bullets, monsters, False, True):
            score += 1
            monster = Enemy("ufo.png", randint(0,620), randint(0,15), 80, 50, randint(3,6))
            monsters.add(monster)

        sprite.groupcollide(bullets, asteroids, True, False)
        
            

        if sprite.collide_rect(ship, asteroid):
            hp -= 1
        if sprite.collide_rect(ship, monster):
            hp -= 1


        if score >= 25:
            window.blit(win_text, (250, 240))
            finish = True

        if lost >= 10 or hp < 1:
            window.blit(lose_text, (250, 240))
            finish = True



        ship.update()
        ship.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        display.update()
    time.delay(30)