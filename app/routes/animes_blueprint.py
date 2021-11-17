from flask import Blueprint

from app.controllers.anime_controller import delete, get_create, filter, update


bp_animes = Blueprint('bp_animes', __name__, url_prefix='/animes')

bp_animes.post('')(get_create)
bp_animes.get('')(get_create)
bp_animes.get('/<int:anime_id>')(filter)
bp_animes.patch('/<int:anime_id>')(update)
bp_animes.delete('/<int:anime_id>')(delete)
