#################################################
# Property of The Song Market
#
# Web Server listening on localhost:5000
# Takes get request with 'uri' key, publishes an IPO
#
# Created by: Matt Ao
# October 2nd, 2014
#################################################

from flask import Flask, request
from IPO import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def createIPO():
    uri = request.args.get('uri', '')
    createIPO(uri)

if __name__ == '__main__':
    app.run()