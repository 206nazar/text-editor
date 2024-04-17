import pygame
import sys
import random

# Ініціалізація Pygame
pygame.init()

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Розміри екрану
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300

# Шрифт для рахунку
font = pygame.font.Font(None, 36)

# Ініціалізація вікна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BaBeMo")

# Константи для гри
GRAVITY = 1
JUMP_HEIGHT = 15
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 80
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 40
GROUND_HEIGHT = 20
FPS = 60

# Клас для персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
        self.velocity_y = 0
        self.is_jumping = False

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.y >= SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -JUMP_HEIGHT
            self.is_jumping = True

# Клас для перешкод
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT

    def update(self):
        self.rect.x -= 7

# Функція для головного циклу гри
def main():
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    next_obstacle_time = 0
    score = 0
    score_increment = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        screen.fill(WHITE)

        # Генеруємо перешкоди
        if pygame.time.get_ticks() > next_obstacle_time:
            obstacle = Obstacle()
            obstacles.add(obstacle)
            all_sprites.add(obstacle)
            next_obstacle_time = pygame.time.get_ticks() + random.randint(1500, 3000)

        # Видаляємо перешкоди, які виходять за межі екрану
        for obstacle in obstacles:
            if obstacle.rect.right < 0:
                obstacle.kill()

        # Перевірка на зіткнення з перешкодами
        if pygame.sprite.spritecollide(player, obstacles, False):
            game_over()

        all_sprites.update()
        all_sprites.draw(screen)

        # Вивід рахунку
        if pygame.time.get_ticks() > score_increment:
            score += 1
            score_increment = pygame.time.get_ticks() + 1000

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

        clock.tick(FPS)

# Функція для закінчення гри та перегравання
def game_over():
    font_large = pygame.font.Font(None, 72)
    game_over_text = font_large.render("Game Over", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 36))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

if __name__ == "__main__":
    main()
