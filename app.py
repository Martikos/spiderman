from flask import Flask
from tornado.httpclient import AsyncHTTPClient

app = Flask(__name__)

@app.route('/results')
def results():
    result = requests.get('http://localhost:8888/results')
    return result.text


@app.route('/', methods=["GET"])
def query():
    print "queried"

    http_client = AsyncHTTPClient()
    http_client.fetch(request_url, callback=related_search)

    return "result"


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
