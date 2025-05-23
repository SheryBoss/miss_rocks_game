import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50

WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shery game')
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([OBSTACLE_WIDTH, OBSTACLE_HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        self.rect.y = -self.rect.height
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
            self.rect.y = -self.rect.height
            global score
            score += 1   # Increase score when obstacle passes the screen

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

score = 0
font = pygame.font.SysFont(None, 36)

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        if random.randrange(100) < 2:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            game_over = True

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)

        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(50)

    else:
        # Show final score on black screen
        screen.fill((0, 0, 0))
        final_text = font.render("Game Over! Final Score: " + str(score), True, WHITE)
        screen.blit(final_text, (SCREEN_WIDTH // 2 - final_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - final_text.get_height() // 2))
        pygame.display.flip()

        # Wait for player to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

pygame.quit()
sys.exit()
