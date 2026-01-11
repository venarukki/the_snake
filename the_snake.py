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

# Клавиши управления:
KEY_UP = pygame.K_UP
KEY_DOWN = pygame.K_DOWN
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT

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
        raise NotImplementedError('draw нужно переопределить в подклассе.')


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None):
        """Инициализация класса яблока."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Установка рандомного положения яблока."""
        occupied_positions = occupied_positions or []
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
        self.next_direction = None
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, next_direction):
        """Обновление направления движения змеи."""
        if next_direction:
            if next_direction == UP and self.direction != DOWN:
                self.direction = UP
            elif next_direction == DOWN and self.direction != UP:
                self.direction = DOWN
            elif next_direction == LEFT and self.direction != RIGHT:
                self.direction = LEFT
            elif next_direction == RIGHT and self.direction != LEFT:
                self.direction = RIGHT

    def move(self):
        """Обновление позиции змеи."""
        self.update_direction(self.next_direction)
        self.next_direction = None

        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        positions_list = list(self.positions)
        positions_list.insert(0, new_head)

        if len(positions_list) > self.length:
            self.last = positions_list.pop()
        else:
            self.last = None

        self.positions = tuple(positions_list)

    def self_collided(self):
        """Проверка на столкновения змейки с собой."""
        head = self.get_head_position()
        return head in self.positions[1:]

    def draw(self, surface):
        """Отрисовка змеи."""
        for position_index, position in enumerate(self.positions):
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            color = self.body_color if position_index != 0 else (0, 100, 0)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс позиции змеи в исходное."""
        self.length = 1
        self.positions = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),)
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None


def handle_keys(snake):
    """Обработка нажатия клавиш."""
    direction_map = {
        (KEY_UP, DOWN): DOWN,
        (KEY_UP, UP): UP,
        (KEY_UP, LEFT): UP,
        (KEY_UP, RIGHT): UP,

        (KEY_DOWN, UP): UP,
        (KEY_DOWN, DOWN): DOWN,
        (KEY_DOWN, LEFT): DOWN,
        (KEY_DOWN, RIGHT): DOWN,

        (KEY_LEFT, RIGHT): RIGHT,
        (KEY_LEFT, LEFT): LEFT,
        (KEY_LEFT, UP): LEFT,
        (KEY_LEFT, DOWN): LEFT,

        (KEY_RIGHT, LEFT): LEFT,
        (KEY_RIGHT, RIGHT): RIGHT,
        (KEY_RIGHT, UP): RIGHT,
        (KEY_RIGHT, DOWN): RIGHT,
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit('Окно игры было закрыто игроком.')
        if event.type == pygame.KEYDOWN:
            new_direction = direction_map.get((event.key, snake.direction),
                                              snake.direction)
            snake.next_direction = new_direction


def game_reset(snake, apple):
    """Сброс игры."""
    snake.reset()
    apple.randomize_position(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    """Основной цикл игры."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.move()

        if snake.self_collided():
            game_reset(snake, apple)

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
