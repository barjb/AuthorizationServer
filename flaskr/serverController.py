from werkzeug.security import check_password_hash, generate_password_hash
from flask import request

from flaskr.db import get_db
from flaskr.auth import encode, JWT, isValid, decode, isValidButExpired


def temp():
    if request.method == 'GET':
        db = get_db()
        users = [
            {'username': 'jacob', 'password': 'password'},
            {'username': 'test1', 'password': 'test'},
            {'username': 'test2', 'password': 'test'},
            {'username': 'test3', 'password': 'test'}
        ]
        for user in users:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (user['username'], generate_password_hash(user['password'])),
            )
        db.commit()
    return 'ok'


def users():
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    response = [{'name': user['username'], 'password':user['password']}
                for user in users]
    return response


def tokens():
    db = get_db()
    tokens = db.execute('SELECT * FROM token').fetchall()
    response = [{'id': token['id'], 'tokenstr': token['tokenstr'], 'rootId':token['rootId'],
                 'refreshed':token['refreshed']} for token in tokens]
    return response


def cleartokens():
    db = get_db()
    db.execute('DELETE FROM token WHERE 1=1')
    db.commit()
    return 'ok'


def login():
    username = request.json['username']
    password = request.json['password']
    db = get_db()
    error = None
    user = None
    if not username or not password:
        error = 'Username and Password fields required'
        return {'message': error, 'status': 401, 'data': []}

    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'User not found'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'
    if error:
        return {'message': error, 'status': 401, 'data': []}
    access_token = encode(user['username'], JWT.ACCESS)
    refresh_token = encode(user['username'], JWT.REFRESH)
    db.execute('INSERT INTO token (tokenstr,rootId,refreshed) VALUES (?,?,?)',
               (refresh_token, None, False))
    db.commit()
    response = {'message': 'succesfully logged in',
                'status': 201, 'data': {'access-token': access_token, 'refresh-token': refresh_token}}
    return response


def refresh():
    access_token = request.json['access-token']
    refresh_token = request.json['refresh-token']

    if not isValidButExpired(access_token):
        return {'message': 'access token is not valid', 'status': 401, 'data': []}
    if not isValid(refresh_token, JWT.REFRESH):
        return {'message': 'refresh token is not valid', 'status': 401, 'data': []}

    decoded_refresh = decode(refresh_token, JWT.REFRESH)
    new_access_token = encode(decoded_refresh['user'], JWT.ACCESS)
    new_refresh_token = encode(decoded_refresh['user'], JWT.REFRESH)
    db = get_db()
    refresh_token_db = db.execute("SELECT id,refreshed FROM token WHERE tokenstr==?",
                                  (refresh_token,)).fetchone()
    if refresh_token_db == None:
        return {'message': 'Token deleted due to security breach', 'status': 401, 'data': []}

    if (refresh_token_db['refreshed']):
        db.execute('DELETE FROM token WHERE id=? or rootId=?',
                   (refresh_token_db['id'], refresh_token_db['id'],))
        db.commit()
        return {'message': 'Security breach', 'status': 401, 'data': []}
    db.execute('INSERT INTO token (tokenstr,rootId,refreshed) VALUES (?,?,?)',
               (new_refresh_token, refresh_token_db['id'], False))
    db.execute("UPDATE token SET refreshed=True WHERE id=?",
               (refresh_token_db['id'],))
    db.commit()
    resp = {'message': 'Refreshed access token succesfully', 'status': 201, 'data': {
            'access-token': new_access_token,
            'refresh-token': new_refresh_token
            }}
    return resp


def verify():
    access_token = request.json['access-token']
    if not isValid(access_token, JWT.ACCESS):
        return {'message': 'access token is not valid', 'status': 401, 'data': []}
    return {'message': 'access token is valid', 'status': 200, 'data': [access_token]}
