import sae, pylibmc, sys
from mysite import wsgi

sys.modules['memcache'] = pylibmc
application = sae.create_wsgi_app(wsgi.application)

