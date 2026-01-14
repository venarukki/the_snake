"""
Игра "Змейка" с использованием Pygame.

Реализация классики игр "Змейка" через библиотеку PyGame.
"""
from random import choice, randint

import pygame as pg  # импорт pygame в сокращенном виде

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
KEY_UP = pg.K_UP
KEY_DOWN = pg.K_DOWN
KEY_LEFT = pg.K_LEFT
KEY_RIGHT = pg.K_RIGHT

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет головы змейки (добавлен)
SNAKE_HEAD_COLOR = (0, 100, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Класс-основа для объектов игры."""

    def __init__(self, position=(0, 0), body_color=None):
        """Инициализация класса игровых объектов."""
        self.position = position
        self.body_color = body_color

    def _draw_cell(self, surface, position=None, color=None, draw_border=True):
        """Отрисовка одной ячейки на поле."""
        position = position or self.position
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, color, rect)
        if draw_border:
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

    def draw(self):  # параметр surface был удалён
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
        self._draw_cell(surface)  # используем метод _draw_cell


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
        #  убран вызов update_direction
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        positions_list = list(self.positions)
        positions_list.insert(0, new_head)

        #  вместо большого кода сделан тернарный оператор
        self.last = positions_list.pop() if len(positions_list) > self.length else None

        self.positions = tuple(positions_list)

    def self_collided(self):
        """Проверка на столкновения змейки с собой."""
        #  убрана "одноразовая" переменная head
        return self.get_head_position() in self.positions[1:]

    def draw(self, surface):
        """Отрисовка змеи."""
        # добавляем _draw_cell в метод draw
        for position_index, position in enumerate(self.positions):
            # используем константу цвета головы вместо литерала
            color = SNAKE_HEAD_COLOR if position_index == 0 else self.body_color
            self._draw_cell(surface, position, color)

        if self.last:
            self._draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR,
                            draw_border=False)

    def reset(self):
        """Сброс позиции змеи в исходное."""
        self.length = 1
        self.positions = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),)
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None


def handle_keys(snake):
    """Обработка нажатия клавиш."""
    #  немножко сократил обработку
    direction_map = {
        KEY_UP: UP,
        KEY_DOWN: DOWN,
        KEY_LEFT: LEFT,
        KEY_RIGHT: RIGHT,
    }

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit('Окно игры было закрыто игроком.')
        if event.type == pg.KEYDOWN:
            new_direction = direction_map.get(event.key)
            # добавил вызов метода update_direction змейки
            # в обработку клавиш
            snake.update_direction(new_direction)


def game_reset(snake, apple):
    """Сброс игры."""
    snake.reset()
    apple.randomize_position(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    """Основной цикл игры."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        # 1. Ввод: обработка
        handle_keys(snake)

        # 2. Обработка: обновление состояния игры
        # 2.1 Обновление направления
        if snake.next_direction:
            snake.update_direction(snake.next_direction)
            snake.next_direction = None

        # 2.2 Движение змейки
        snake.move()

        # 2.3 Проверка на столкновения
        if snake.self_collided():
            game_reset(snake, apple)

        # 2.4 Проверка на съедение яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # 3. ВЫВОД: отрисовка
        apple.draw(screen)
        snake.draw(screen)
        pg.display.update()


if __name__ == '__main__':
    main()
