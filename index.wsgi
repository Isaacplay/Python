#def application(environ, start_response):
#    start_response('200 ok', [('content-type', 'text/plain')])
#   return ['Hello, SAE!']
# coding: UTF-8
import os
import sae
import web
import sys
from weixinInterface import WeixinInterface
app_root = os.path.dirname(__file__) 
sys.path.append(os.path.join(app_root, 'virtualenv.bundle.zip'))
sys.path.insert(0,os.path.join(app_root, 'xpinyin.zip')) 
sys.path.insert(0,os.path.join(app_root, 'requests.zip'))
sys.path.insert(0,os.path.join(app_root, 'urllib3.zip')) 

urls = (
'/weixin','WeixinInterface'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals()).wsgifunc()        
application = sae.create_wsgi_app(app)
