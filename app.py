import sys
from flask import Flask
from flask import make_response
from flask import request
import json

app = Flask(__name__)


@app.route('/')
def homepage():
    return "<h1>Meet ML chat bot </h1><p>Python: {ver}</p>".format(ver=sys.version)


@app.route('/webhook_chat_google', methods=['POST'])
def webhook_chat_google():

    req = request.get_json(silent=True, force=True)
    print('Request:\n{0}'.format(json.dumps(req, indent=4)))

    response = prepare_response("chat bot test speech")

    response = json.dumps(response, indent=4)
    print('Response:\n{0}'.format(response))

    r = make_response(response)
    r.headers['Content-Type'] = 'application/json'
    return r


def prepare_response(answer, context_out=None):
    response = dict()
    response["speech"] = answer
    response["displayText"] = answer
    if context_out:
        response["contextOut"] = context_out

    return response


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
