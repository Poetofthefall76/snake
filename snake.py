import pygame
import random

# Инициализация Pygame
pygame.init()

# Размер окна и клетки
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Класс для представления змейки
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.new_direction = self.direction

    def move(self):
        self.direction = self.new_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        self.body.insert(0, new_head)

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.new_direction = (dx, dy)

    def draw(self, screen):
        for segment in self.body:
            x, y = segment
            pygame.draw.circle(screen, GREEN, ((x + 0.5) * GRID_SIZE, (y + 0.5) * GRID_SIZE), GRID_SIZE // 2)

# Класс для представления еды (фрукта)
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, screen):
        pygame.draw.rect(screen, RED, pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Функция для отображения текста на экране
def draw_text(screen, text, font_size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
snake = Snake()
food = Food()
game_over = False
in_menu = True

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    if in_menu:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            in_menu = False

    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            snake.change_direction(0, -1)
        elif keys[pygame.K_DOWN]:
            snake.change_direction(0, 1)
        elif keys[pygame.K_LEFT]:
            snake.change_direction(-1, 0)
        elif keys[pygame.K_RIGHT]:
            snake.change_direction(1, 0)

        # Обновление змейки и проверка на столкновение с едой
        snake.move()
        if snake.body[0] == food.position:
            food.spawn()
        else:
            snake.body.pop()

        # Проверка на столкновение себя
        if snake.body[0] in snake.body[1:]:
            in_menu = True
            snake = Snake()
            food = Food()

        # Отрисовка фона
        screen.fill(BLACK)

        # Отрисовка змейки и еды
        snake.draw(screen)
        food.draw(screen)

    # Отображение меню
    if in_menu:
        draw_text(screen, "Press SPACE to start", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Отрисовка экрана
    pygame.display.flip()
    clock.tick(10)  # Теперь игра работает с 60 фреймами в секунду

pygame.quit()