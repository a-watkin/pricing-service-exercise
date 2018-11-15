from src.app import app
import sys

print('what?')
print('encoding is', sys.getdefaultencoding())
print(sys.version)

app.run(debug=app.config["DEBUG"], port=4990)
