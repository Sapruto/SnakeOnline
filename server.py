import random
from typing import Type

from flask import Flask, request
from game import update_game as game_update, GRID_WIDTH, GRID_HEIGHT, GRID_SIZE
from game_objects import StaticGameObject, Snake, Apple, Portal, Minus, CpeedPlusPlus
app = Flask("PIPIDASTR")

SIZE = 20

all_snakes: list[Snake] = []
apple = Apple()
game_objects: list[StaticGameObject] = []

room: list[dict] = []
game_object_types: dict[str, Type[StaticGameObject]] = {
    "Portal": Portal,
    "Minus": Minus,
    "C++": CpeedPlusPlus
}

@app.route("/create_room", methods=["GET"])
def create_room():
    new_apple = Apple()
    new_all_snakes: list[Snake] = []

    room.append({"apple": new_apple, "all_snakes": new_all_snakes})

    return str(len(room) - 1)

@app.route("/connect", methods=["GET"])
def connect():
    global all_snakes

    snake = Snake((0, 0), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    # snake = Snake((0, 0), (0, 0, 0))

    all_snakes.append(snake)

    return str(len(all_snakes) - 1)

def get_host():
    for id, snake in enumerate(all_snakes):
        if snake != 0:
            return id


@app.route("/get_board", methods=["POST"])
def get_board():
    id = request.json["id"]

    if id == get_host():
        update_game()

    snakes = []

    for snake in all_snakes:
        if snake == 0:
            snakes.append(0)
        else:
            snakes.append({"snake_pos": snake.positions, "snake_color": snake.color})

    gameobjects_serialized = []

    for gameobject in game_objects:
        gameobjects_serialized.append({
            "position": gameobject.position,
            "resource_name": gameobject.resource_name
        })

    return {
        "all_snakes": snakes,
        "game_objects": gameobjects_serialized,
        "apple": apple.position
    }


@app.route("/create_gameobject", methods=["POST"])
def create_gameobject():
    data = request.json
    id = data["id"]
    gameobject_type = data["gameobject_type"]

    if id != get_host():
        return "not host"

    position = (random.randint(0, GRID_WIDTH) * GRID_SIZE, random.randint(0, GRID_HEIGHT) * GRID_SIZE)

    data = {}

    resource_name = ""
    if gameobject_type == "Portal":
        to_pos = (random.randint(0, GRID_WIDTH) * GRID_SIZE, random.randint(0, GRID_HEIGHT) * GRID_SIZE)
        data = {"to_pos": to_pos}
        resource_name = "resources/portal.png"
    elif gameobject_type == "Minus":
        resource_name = "resources/minus.png"
    elif gameobject_type == "C++":
        resource_name = "resources/kofee.png"

    gameobject = game_object_types[gameobject_type](position, resource_name, data)
    game_objects.append(gameobject)


@app.route("/update_snake", methods=["POST"])
def update_snakes():
    data = request.json
    id = data["id"]

    all_snakes[id].events = data["events"]

    return "success"


@app.route("/update_game", methods=["GET"])
def update_game():
    game_update(all_snakes, apple, game_objects)

    for obj in game_objects:
        if obj.is_destroyed:
            game_objects.remove(obj)
    
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
