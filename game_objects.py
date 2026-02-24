from abc import ABC, abstractmethod
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
        self.speed_multiplier = 1

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        for i in range(self.speed_multiplier):
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


class StaticGameObject(ABC):
    def __init__(self, position, resource_name, data):
        self.position = position
        self.resource_name = resource_name
        self.data = data

        self.is_destroyed = False

    @abstractmethod
    def event(self, snake: Snake = None):
        pass

    @abstractmethod
    def destroy(self):
        self.is_destroyed = True

class Portal(StaticGameObject):
    def __init__(self, position, resource_name, data):
        super().__init__(position, resource_name, data)

    def event(self, snake: Snake = None):
        try:
            snake.positions[0] = self.data['to_pos']
        except Exception as e:
            print(f"{e}")


class Minus(StaticGameObject):
    def __init__(self, position, resource_name, data):
        super().__init__(position, resource_name, data)

    def event(self, snake: Snake = None):
        if snake.length <= 2:
            return

        for i in range(randint(1, snake.length - 1)):
            snake.positions.pop()
            snake.length -= 1

class CpeedPlusPlus(StaticGameObject):
    def __init__(self, position, resource_name, data):
        super().__init__(position, resource_name, data)

    def event(self, snake: Snake = None):
        if snake.speed_multiplier == 1:
            snake.speed_multiplier = snake.length
        else:
            snake.speed_multiplier = 1
