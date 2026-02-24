from game_objects import *

import pygame

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

def update_snake_with_game_object(snake, game_object):
    if snake.get_head_position() == game_object.position:
        game_object.event(snake)
        game_object.destroy()


def update_game(all_snakes, apple, game_objects):
    for snake in all_snakes:
        if snake == 0:
            continue

        update_snake(snake, snake.events, apple)

    for snake in all_snakes:
        if snake == 0:
            continue
        for game_object in game_objects:
            update_snake_with_game_object(snake, game_object)

    for i in range(0, len(all_snakes)):
        if all_snakes[i] == 0:
            continue
        for j in range(i + 1, len(all_snakes)):
            if all_snakes[j] == 0:
                continue
            snake_collision(all_snakes[i], all_snakes[j])