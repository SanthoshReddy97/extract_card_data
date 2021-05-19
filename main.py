import json
import logging

from flask import Flask, jsonify, request
from handler import CardHandler

# creating a Flask app
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        logging.debug("Request body:: {}".format(request.data))
        request_body = json.loads(request.data)

        if request_body.get('url'):
            handler = CardHandler(request_body=request_body)
        else:
            return "No image url found"
        card_data = handler.extract_card_data()
        return jsonify(card_data)


# By default flask runs on the port 5000
app.run()
