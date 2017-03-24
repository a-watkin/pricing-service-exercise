from src.app import app
import sys


print('encoding is', sys.getdefaultencoding())


app.run(debug=app.config["DEBUG"], port=4990)