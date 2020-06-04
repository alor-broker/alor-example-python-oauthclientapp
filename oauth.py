from requests_oauthlib import OAuth2Session
import webbrowser
import io
import http.server
import socketserver
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Эти параметры заполняются значениями из https://alor.dev/myapps
client_id = "d8d4cbfc66d649f18ce7"
client_secret = "4s79AP4NkG6AMMRsoiPCO/XG1PGXI7pAS+UDu69xn40="

authorization_base_url = 'https://oauth.alor.ru/authorize'
token_url = 'https://oauth.alor.ru/token'
redirect_uri = 'http://localhost:3002/callback'


scope = [
    'ordersread', 'trades', 'personal'
]

alor = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

authorization_url, state = alor.authorization_url(authorization_base_url)

webbrowser.open(authorization_url)

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        o = urllib.parse.urlparse(self.path)
        data = urllib.parse.parse_qs(o.query)
        code = data['code'][0]
        tokens = alor.fetch_token(token_url, code=code, client_secret=client_secret, include_client_id=True)
        print(tokens)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(tokens).encode('utf-8'))

PORT = 3002
httpd = HTTPServer(('localhost', PORT), CallbackHandler)    
httpd.serve_forever()
