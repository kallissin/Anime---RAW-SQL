from flask import request, jsonify
from psycopg2.errors import lookup
from app.models.anime_model import Anime
from app.exc.exceptions import TypeKeyError


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
        try:
            list_animes = Anime.get_all()
            new_list_animes = [formate_value_released_date(anime) for anime in list_animes]
        except lookup("42P01"):
            Anime.create_table()
            return jsonify({"data": []}), 200
        return jsonify({"data": new_list_animes}), 200


def filter(anime_id):
    try:
        anime = Anime.get_by_id(anime_id)
        formated_anime = formate_value_released_date(anime)
        if formated_anime:
            return jsonify({"data": [formated_anime]}), 200
        return jsonify({"error": "Not Found"}), 404
    except (lookup("42P01"), KeyError):
        return jsonify({"error": "Not Found"}), 404


def update(anime_id):
    data = request.get_json()
    try:
        Anime.validate_key(data)
        if 'anime' in data.keys():
            data = Anime.format_key_anime(data)
        anime = Anime.update_anime(anime_id, data)
        formated_anime = formate_value_released_date(anime)
    except TypeKeyError as err:
        return jsonify(err.__dict__['message']), 422
    except (lookup("42P01"), KeyError):
        return jsonify({"error": "Not Found"}), 404
    return jsonify(formated_anime), 200


def delete(anime_id):
    try:
        result_verification = Anime.verify_id_exists(anime_id)
        if result_verification:    
            anime = Anime.delete_anime(anime_id)
            formated_anime = formate_value_released_date(anime)
            return jsonify(formated_anime), 200
        return jsonify({"error": "Not Found"}), 404
    except (lookup("42P01"), KeyError):
        return jsonify({"error": "Not Found"}), 404
