import random

from flask import Flask, request
from game import update_game as game_update, Apple, Snake, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH

app = Flask("PIPIDASTR")

SIZE = 20

all_snakes: list[Snake] = []
apple = Apple()

rome: list[dict] = []

@app.route("/create_rome", methods=["GET"])
def create_room():
    new_apple = Apple()
    new_all_snakes: list[Snake] = []

    rome.append({"apple": new_apple, "all_snakes": new_all_snakes})

    return str(len(rome) - 1)

@app.route("/connect", methods=["GET"])
def connect():
    global all_snakes

    snake = Snake((0, 0), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    all_snakes.append(snake)

    return str(len(all_snakes) - 1)

def get_host():
    for id, snake in enumerate(all_snakes):
        print(id, snake)
        if snake != 0:
            return id


@app.route("/get_board", methods=["POST"])
def get_board():
    snakes = []
    id = request.json["id"]

    if id == get_host():
        update_game()

    for snake in all_snakes:
        if snake == 0:
            snakes.append(0)
        else:
            snakes.append({"snake_pos": snake.positions, "snake_color": snake.color})
    return {
        "all_snakes": snakes,
        "apple": apple.position
    }


@app.route("/update_snake", methods=["POST"])
def update_snakes():
    data = request.json
    id = data["id"]

    all_snakes[id].events = data["events"]

    return "success"


@app.route("/update_game", methods=["GET"])
def update_game():
    game_update(all_snakes, apple)
    
    return "success"


@app.route("/disconnect", methods=["POST"])
def disconnect():
    global all_snakes

    data = request.json
    id = data["id"]

    if 0 <= id < len(all_snakes):
        all_snakes[id] = 0
        return "success"
    else:
        return "snake not found", 404


app.run(
    host='0.0.0.0',
    port=5000,
    debug=False,
    threaded=True,
    use_reloader=False
)
