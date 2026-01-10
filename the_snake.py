"""
Игра "Змейка" с использованием Pygame.

Реализация классики игр "Змейка" через библиотеку PyGame.
"""
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Класс-основа для объектов игры."""

    def __init__(self, position=(0, 0), body_color=None):
        """Инициализация класса игровых объектов."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта. Переопределяется в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None):
        """Инициализация класса яблока."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Установка рандомного положения яблока."""
        if occupied_positions is None:
            occupied_positions = []
        while True:
            pos = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if pos not in occupied_positions:
                self.position = pos
                break

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализация класса змейки."""
        super().__init__(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                         body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновление направления движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление позиции змеи."""
        self.update_direction()
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовка змеи."""
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            color = self.body_color if i != 0 else (0, 100, 0)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс позиции змеи в исходное."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(snake):
    """Обработка нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.move()

        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
