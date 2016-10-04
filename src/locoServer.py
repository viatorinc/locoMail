__author__ = 'jmoriano'


from gevent.wsgi import WSGIServer
from locoMail import app

http_server = WSGIServer(('', 5000), app)
http_server.log
http_server.serve_forever()