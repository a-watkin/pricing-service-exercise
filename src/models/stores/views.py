from flask import Blueprint, render_template, request, redirect, url_for
from src.models.stores.store import Store
import json

import src.models.users.decorators as user_decorators

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    # print('should be getting here?')
    stores = Store.all()
    # return 'hello'
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.html', store=Store.get_by_id(store_id))


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_permission
def edit_store(store_id):
    store = Store.get_by_id(store_id)

    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        # beautiful soup expects a python dict, so you get the {"id": "price-now"}
        # as a json object, this converts is to a dict, it's actually already in that format anyway right? i think so
        query = json.loads(request.form['query'])

        # because you're working on an object that already exists
        # store = Store.get_by_id(store_id)

        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query

        store.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>', methods=['GET'])
@user_decorators.requires_admin_permission
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.index'))


@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin_permission
def create_store():
    if request.method == 'POST':
        # print('create_store here, am post data now?')
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        # beautiful soup expects a python dict, so you get the {"id": "price-now"}
        # as a json object, this converts is to a dict, it's actually already in that format anyway right? i think so
        query = json.loads(request.form['query'])

        # signature of the store class
        # def __init__(self, name, url_prefix, tag_name, query, _id=None):
        Store(name, url_prefix, tag_name, query).save_to_mongo()


    return render_template('stores/new_store.html')