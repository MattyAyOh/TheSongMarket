from flask import Flask, request
from IPO import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def createIPO():
    uri = request.args.get('uri', '')
    createIPO(uri)

if __name__ == '__main__':
    app.run()