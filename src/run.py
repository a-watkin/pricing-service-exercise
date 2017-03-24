from src.app import app
import sys
import importlib

print(sys.getdefaultencoding())

reload(sys)
sys.setdefaultencoding('UTF8')


print('encoding is', sys.getdefaultencoding())
print('so now it will not even print anything')



# importlib.reload(sys)

app.run(debug=app.config["DEBUG"], port=4990)