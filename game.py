from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.randomize_position([])

    def randomize_position(self, blocked_positions: list[tuple[int]]):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        
        if self.position in blocked_positions:
            self.randomize_position(blocked_positions)


class Snake(GameObject):
    def __init__(self, position, color):
        super().__init__()
        self.length = 2
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.color = color
        self.events = []

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x = (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH
        new_y = (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        if (new_x, new_y) in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, (new_x, new_y))
            self.last = self.positions[-1]
            if len(self.positions) > self.length:
                self.positions.pop()

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 2
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

def handle_keys(game_object, events):
    for key in events:
        if key == pygame.K_UP and game_object.direction != DOWN:
            game_object.next_direction = UP
        elif key == pygame.K_DOWN and game_object.direction != UP:
            game_object.next_direction = DOWN
        elif key == pygame.K_LEFT and game_object.direction != RIGHT:
            game_object.next_direction = LEFT
        elif key == pygame.K_RIGHT and game_object.direction != LEFT:
            game_object.next_direction = RIGHT

def snake_collision(snake1, snake2):
    head1 = snake1.get_head_position()
    head2 = snake2.get_head_position()

    if head1 == head2:
        snake1.reset()
        snake2.reset()

    for i in snake1.positions:
        if i == head2:
            snake2.reset()

    for i in snake2.positions:
        if i == head1:
            snake1.reset()

def update_snake(snake, keys, apple):
    handle_keys(snake, keys)
    snake.update_direction()
    snake.move()
    
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position(snake.positions)


def update_game(all_snakes, apple):
    for snake in all_snakes:
        if snake == 0:
            continue

        update_snake(snake, snake.events, apple)

    for i in range(0, len(all_snakes)):
        if all_snakes[i] == 0:
            continue
        for j in range(i + 1, len(all_snakes)):
            if all_snakes[j] == 0:
                continue
            snake_collision(all_snakes[i], all_snakes[j])