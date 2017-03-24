from flask import Flask, render_template
from src.common.database import Database


app = Flask(__name__)


app.config.from_object('src.config')
# appconfig = app.from_object('src.config')

app_admins = app.config['ADMINS']

app.config.encoding = "utf-8"


# print("atomicpenguines@gmail.com" in app.config['ADMINS'])

app.secret_key = "123"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')


# print('getting here')
# import the blueprints
#
# it says it can't find this blueprint, seems to link to it ok though?
from src.models.users.views import user_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint


# register the blueprints
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")