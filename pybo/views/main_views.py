from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_world():
    return 'Hello Pybo!'

@bp.route('/')
def home_start():
    return 'Pybo Start'