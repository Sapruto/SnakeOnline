import pygame
import requests

serverURL = "https://glacially-phlegmatic-chihuahua.cloudpub.ru:443"

ID = int(requests.get(f"{serverURL}/connect").text)

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

        self.head_img = pygame.image.load("resources/snake_head.png").convert_alpha()
        self.body_img = pygame.image.load("resources/snake_body.png").convert_alpha()

        self.head_img = pygame.transform.scale(self.head_img, (GRID_SIZE, GRID_SIZE))
        self.body_img = pygame.transform.scale(self.body_img, (GRID_SIZE, GRID_SIZE))

    def draw(self):
        if self.head_img is None or self.body_img is None:
            for position in self.positions[:-1]:
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, self.body_color, rect)
                pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        else:
            for position in self.positions[1:]:
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                screen.blit(self.body_img, rect)

            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            screen.blit(self.head_img, head_rect)

    def get_head_position(self):
        return self.positions[0]

class DrawStaticGameObject:
    def __init__(self, position, resource_name):
        self.position = position

        self.img = pygame.image.load(resource_name).convert_alpha()
        self.img = pygame.transform.scale(self.img, (GRID_SIZE, GRID_SIZE))

    def draw(self):
        head_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        screen.blit(self.img, head_rect)


def main():
    pygame.init()

    while True:
        clock.tick(SPEED)
        
        request = requests.post(f"{serverURL}/get_board", json={
            "id": ID
        })

        data = request.json()

        all_snakes = []

        apple = Apple(data["apple"])

        for snake_data in data["all_snakes"]:
            if snake_data == 0:
                all_snakes.append(0)
            else:
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

        screen.fill(BOARD_BACKGROUND_COLOR)

        for snake in all_snakes:
            if snake == 0:
                continue

            snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
    requests.post(f"{serverURL}/disconnect", json={
            "id": ID,
        })