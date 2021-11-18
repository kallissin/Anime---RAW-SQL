from flask import request, jsonify
from psycopg2.errors import lookup
from app.models.anime_model import Anime
from app.models.exceptions import TypeKeyError


def formate_value_released_date(data):
    data['released_date'] = data['released_date'].strftime('%d/%m/%Y')
    return data


def get_create():
    if request.method == 'POST':
        data = request.get_json()
        try:
            Anime.validate_key(data)
            formated_data = Anime.format_key_anime(data)
            anime = Anime(formated_data)
            inserted_anime = anime.create_anime()
        except TypeKeyError as err:
            return jsonify(err.__dict__['message']), 422
        except lookup("42P01"):
            Anime.create_table()
            inserted_anime = anime.create_anime()
        except lookup("23505"):
            return {"error": "anime is already exists"}, 409
        return jsonify(formate_value_released_date(inserted_anime)), 201
    if request.method == 'GET':
        return {'message': 'agora é GET'}, 200


def filter(anime_id):
    return {'data': 'rota em andamento'}, 200


def update(anime_id):
    return {'data': 'rota em andamento'}, 200


def delete(anime_id):
    return {'data': 'rota em andamento'}, 200
