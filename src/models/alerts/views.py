from flask import Blueprint, render_template, request, session, redirect, url_for
from models.alerts.alert import Alert
from models.items.item import Item
import models.users.decorators as user_decorators

# store_blueprint = Blueprint('stores', __name__)
# print('why?')
alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
@user_decorators.requires_login
def index():
    pass
    # return "methods not method"

# so on a hunch i commented this out and now it works? what the actual fuck
# its methods, not method


@alert_blueprint.route('/new', methods=['GET', 'POST'])
# checks that the user is logged in
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        # def __init__(self, name, url, price=None, _id=None):
        item = Item(name, url)
        item.save_to_mongo()

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()  # Already saves to mongo

    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)

    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = request.form['price_limit']

        # so some of these are actually item properties
        alert.item.name = name
        alert.item.url = url
        alert.price_limit = price_limit

        # do i need to save the item?
        alert.save_to_mongo()
        # maybe?
        alert.item.save_to_mongo()

        return redirect(url_for('users.user_alerts'))

        # experimenting
        # return get_alert_page(alert_id)

    return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    # print('hello from get_alert_page the alert_id is: ', alert_id)
    alert = Alert.find_by_id(alert_id)
    return render_template('/alerts/alert.html', alert=alert)


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
