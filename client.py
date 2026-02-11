import pygame
import requests

serverURL = "http://127.0.0.1:5500"

ID = int(input("Enter ur id (1, 2): "))

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self, position):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = position

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self, positions, color):
        super().__init__()
        self.positions = positions
        self.body_color = color

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        return self.positions[0]




def main():
    pygame.init()

    while True:
        clock.tick(SPEED)
        
        request = requests.get(f"{serverURL}/get_board")

        data = request.json()

        all_snakes = []

        apple = Apple(data["apple"])

        for snake_data in data["all_snakes"]:
            new_snake = Snake(snake_data["snake_pos"], snake_data["snake_color"])
            all_snakes.append(new_snake)

        events = pygame.event.get()
        keys = []
        
        for event in events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                keys.append(event.key)

        requests.post(f"{serverURL}/update_snake", json={
            "id": ID,
            "events": keys
        })

        if ID == 1:
            requests.get(f"{serverURL}/update_game")

        screen.fill(BOARD_BACKGROUND_COLOR)

        for snake in all_snakes:
            snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()