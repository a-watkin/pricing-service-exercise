from flask import Blueprint, session, request, url_for, render_template
from werkzeug.utils import redirect

from src.models.users.user import User, UserError
import src.models.users.decorators as user_decorators

# print( type( user_decorators) )


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # check login is valid
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                # gets the method user_alerts from the current location
                return redirect(url_for(".user_alerts"))
        except UserError.UserError as e:
            return e.message

    return render_template("users/login.html") # send an error if the login was invalid


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # check login is valid
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                # gets the method user_alerts from the current location
                return redirect(url_for(".user_alerts"))
        except UserError.UserError as e:
            # getting username does not exist here
            return e.message

    # changing this because i think it should be register
    return render_template("users/register.html") # send an error if the login was invalid


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()
    # the alert=alert passes the alert variable from above to the page so jinja can use it
    return render_template('users/alerts.html', alerts=alerts)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    # home here is the base template in the app.py file which is why you don't need
    # any prefix information
    return redirect(url_for('home'))


@user_blueprint.route('/check_alerts/')
def check_user_alerts(user_id):
    pass