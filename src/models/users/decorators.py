from functools import wraps
from flask import session, url_for, redirect, request
from src.app import app


# the whole thing checks to see if the user is logged in, if they are it just allows them to continue
# if not they have to login then they can continue
def requires_login(func):
    # wraps the above with the below
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # so if the user is not logged in then sent them to the login pag
        if 'email' not in session.keys() or session['email'] is None:
            # once user logs in the next=request.path sends them back to the page they were trying to access
            # but needed to be logged in to access
            # then once they're logged in allow them to continue where they left off
            return redirect(url_for('user.login_user', next=request.path))
        return func(*args, **kwargs)
    return decorated_function

def requires_admin_permission(func):
    # wraps the above with the below
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # so if the user is not logged in then sent them to the login pag
        if 'email' not in session.keys() or session['email'] is None:
            # once user logs in the next=request.path sends them back to the page they were trying to access
            # but needed to be logged in to access
            # then once they're logged in allow them to continue where they left off
            return redirect(url_for('user.login_user', next=request.path))

        # BE CAREFUL HERE the admins is a dict object you have to use square brackets
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('user.login_user'))

        return func(*args, **kwargs)

    return decorated_function


        # all decorators take the function they are decorating as an argument
# @requires_login
# def my_function(x, y):
#     return x + y
    # print('Hello world')
    # return "Hi"

# you can't call my_function outsite of the context of the requires_login(func) above it
# my_function() will give an error, NoneType object not callable

# my_function(5, 7)