import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1200, 400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balap Kelinci vs Kucing")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

rabbit_img = pygame.image.load("rabbit.png")
cat_img = pygame.image.load("cat.png")
boost_img = pygame.image.load("boost.png")

rabbit_img = pygame.transform.scale(rabbit_img, (60, 60))
cat_img = pygame.transform.scale(cat_img, (60, 60))
boost_img = pygame.transform.scale(boost_img, (40, 40))

#class
class Animal:
    def __init__(self, x, y, image, speed):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Player(Animal):
    def __init__(self, x, y, image, speed):
        super().__init__(x, y, image, speed)
        self.boost = False
        self.boost_timer = 0

    def move(self, keys):
        # gerak kanan
        if keys[pygame.K_RIGHT]:
            if self.boost:
                self.x += self.speed + 5
            else:
                self.x += self.speed

        # gerak atas bawah
        if keys[pygame.K_UP]:
            self.y -= 5
        if keys[pygame.K_DOWN]:
            self.y += 5

        # batas layar
        self.y = max(0, min(HEIGHT - 60, self.y))

        # durasi boost
        if self.boost:
            self.boost_timer -= 1
            if self.boost_timer <= 0:
                self.boost = False


class Enemy(Animal):
    def move(self):
        self.x += self.speed + random.randint(0, 2)


class Boost:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.x = random.randint(200, WIDTH - 100)
        self.y = random.choice([80, 150, 220])
        self.active = True

    def draw(self):
        if self.active:
            screen.blit(boost_img, (self.x, self.y))


# objectt nih
player = Player(50, 120, rabbit_img, 5)
enemy = Enemy(50, 250, cat_img, 4)
boost = Boost()

finish_line = WIDTH - 100

# ================= COUNTDOWN =================
def countdown():
    for i in ["3", "2", "1", "GO!"]:
        screen.fill((50, 80, 120))
        text = font.render(i, True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - 30, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(1000)

countdown()

# loop game nya
running = True
winner = None

while running:
    clock.tick(FPS)

    # background (hilangkan bayangan)
    screen.fill((50, 80, 120))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # gerak
    player.move(keys)
    enemy.move()

    # garis finish
    pygame.draw.line(screen, (255, 0, 0), (finish_line, 0), (finish_line, HEIGHT), 5)

    # boost
    boost.draw()

    player_rect = pygame.Rect(player.x, player.y, 60, 60)
    boost_rect = pygame.Rect(boost.x, boost.y, 40, 40)

    if boost.active and player_rect.colliderect(boost_rect):
        player.boost = True
        player.boost_timer = 120
        boost.active = False

    # gambar karakter
    player.draw()
    enemy.draw()

    # cek menang
    if player.x >= finish_line:
        winner = "Kelinci Menang!"
    elif enemy.x >= finish_line:
        winner = "Kucing Menang!"

    # tampilkan pemenang
    if winner:
        player.boost = False
        text = font.render(winner, True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()