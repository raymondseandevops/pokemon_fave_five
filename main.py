
import asyncio
import requests
import json
import random
import statistics
from werkzeug.utils import escape
from flask import Flask, request
app = Flask(__name__)

FAVE_FIVE_POKEMONS: tuple = (
    "torchic",
    "numel",
    "bulbasaur",
    "floette",
    "mudkip"
)


def client_main():
    """
    Starts the Flask server app that listens to default address http://127.0.0.1:5000
    """
    app.run()


@app.route('/<pokemon>', methods=['GET'])
def find_pokemon(pokemon):
    """
    This is and endpoint that retrieves the attributes of individual pokemons from 2 external endpoints, combines, and returns the result. Input should be a name of the pokemon desired to be looked up.
    """
    my_pokemon = escape(pokemon)
    json_att_1 = json.loads(request_pokeapi(
        "https://pokeapi.co/api/v2/pokemon/" + my_pokemon))
    random_move_1 = random.choice(json_att_1["moves"])
    random_move_2 = random.choice(json_att_1["moves"])
    while (random_move_1 == random_move_2):
        random_move_2 = random.choice(json_att_1["moves"])
    json_att_2 = json.loads(request_pokeapi(
        "https://pokeapi.co/api/v2/pokemon-species/" + str(json_att_1["id"])))
    my_pokemon_attributes = {
        "name": json_att_1["name"],
        "height": json_att_1["height"],
        "weight": json_att_1["weight"],
        "color": json_att_2["color"]["name"],
        "moves": [random_move_1["move"]["name"], random_move_2["move"]["name"]],
        "base_happiness": json_att_2["base_happiness"]
    }
    return my_pokemon_attributes


@app.route('/favefivepokemons', methods=['GET'])
def find_fave_five_pokemons():
    """
    This function iterates through the FAVE_FIVE_POKEMONS list to retrieve attributes using the find_pokemon function. This function also calculates the mean, average and median of the respective pokemons' base_happiness attribute. All in all data after data is collected, results are returned.

    """
    pokemon_collection = []
    pokemon_base_happiness_collection = []
    for pokemon in FAVE_FIVE_POKEMONS:
        pokemon_att = json.loads(request_pokeapi(
            "http://127.0.0.1:5000/"+pokemon))
        pokemon_collection.append(pokemon_att)
        pokemon_base_happiness_collection.append(pokemon_att["base_happiness"])
    fave_five_pokemon_extended = {
        "my_fave_five_pokemons": pokemon_collection,
        "base_happiness_mean": statistics.mean(pokemon_base_happiness_collection),
        "base_happiness_average": sum(pokemon_base_happiness_collection)/len(pokemon_base_happiness_collection),
        "base_happiness_median": statistics.median(pokemon_base_happiness_collection),
    }
    return fave_five_pokemon_extended


def request_pokeapi(url):
    """
    Calls/requests API using passed url then returns the response text
    """
    header = {
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=header)
    return response.text


if __name__ == '__main__':
    asyncio.run(client_main())
