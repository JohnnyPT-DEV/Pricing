import json
from flask import Blueprint, render_template, request , url_for , redirect
from models.store import Store

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route("/")
def index() :
    stores = Store.all()
    return render_template('stores/index.html', stores=stores)


@store_blueprint.route("new", methods=['GET', 'POST'])
def new_store() :
    if request.method == 'POST' :
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store = Store(name, url_prefix, tag_name, query)
        store.save_to_mongo()

    return render_template('stores/new_store.html')


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
def edit_store(store_id):
    store = Store.get_by_id(store_id)

    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = request.form['query']

        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query

        store.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_mongo()
    return redirect(url_for('.index'))
