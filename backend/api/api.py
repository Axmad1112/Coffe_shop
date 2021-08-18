import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
    return response

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    for_drinks = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': for_drinks
    }),200
    

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()

    if not drinks:
        abort(404)

    for_drink = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': for_drink
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(jwt):
    data = request.get_json()
    if 'title' and 'recipe' not in data:
        abort(400)

    title = data['title']
    recipe_json = json.dumps(data['recipe'])

    drink = Drink(title=title, recipe=recipe_json)
    drink.insert()

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(f, drink_id):
    body = request.get_json()

    if not body:
        abort(404)

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    try:
        drink = Drink.query.get(drink_id)
        if drink == None:
            abort(404)

        if title:
            drink.title = title

        if recipe:
            drink.recipe = recipe
    except Exception:
        abort(400)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.delete()
    except Exception:
        abort(400)

    return jsonify({'success': True, 'delete': id}), 200


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def Auth_Error_handling(index):
    res = jsonify(index.error)
    res.status_code = index.status_code
    return res


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500
