from flask import Flask, request
from game import update_game as game_update, Apple, Snake, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH

app = Flask("PIPIDASTR")

SIZE = 20

snake1 = Snake((0, SCREEN_HEIGHT // 2))
events1 = []

snake2 = Snake((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
events2 = []

SNAKE_COLOR1 = (52, 67, 69)
SNAKE_COLOR2 = (255, 52, 125)

apple = Apple()

@app.route("/get_board", methods=["GET"])
def get_board():
    return {
        "all_snakes": [
            {"snake_pos": snake1.positions, "snake_color": SNAKE_COLOR1},
            {"snake_pos": snake2.positions, "snake_color": SNAKE_COLOR2}
        ],
        "apple": apple.position
    }


@app.route("/update_snake", methods=["POST"])
def update_snakes():
    global events1, events2
    data = request.json

    if data["id"] == 1:
        events1 = data["events"]
    else:
        events2 = data["events"]

    return "success"


@app.route("/update_game", methods=["GET"])
def update_game():
    global snake1, events1, snake2, events2, apple
    game_update(snake1, events1, snake2, events2, apple)
    
    return "success"


app.run(port=5500, debug=True)
