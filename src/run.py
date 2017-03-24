from src.app import app
import sys
import importlib


def set_defaultencoding_globally(encoding='utf-8'):
    assert sys.getdefaultencoding() in ('ascii', 'mbcs', encoding)
    import imp
    _sys_org = imp.load_dynamic('_sys_org', 'sys')
    _sys_org.setdefaultencoding(encoding)




set_defaultencoding_globally()

importlib.reload(sys)

app.run(debug=app.config["DEBUG"], port=4990)