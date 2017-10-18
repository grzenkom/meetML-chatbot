import sys
from flask import Flask
from flask import make_response
from flask import request
import json
from knowledge_base import KnowledgeBaseReader
app = Flask(__name__)


@app.route('/')
def homepage():
    return "<h1>Meet ML chat bot </h1><p>Python: {ver}</p>".format(ver=sys.version)


@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)
    print('Request:\n{0}'.format(json.dumps(req, indent=4)))

    result = req.get("result").get("parameters")
    property = result.get("property")
    element = result.get("element")

    answer = prepare_answer(element, property)
    response = prepare_response(answer)

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


def prepare_answer(element, property):
    kb = KnowledgeBaseReader.get_kb_extract()
    property_value = kb[kb["Element"] == element][property].tolist()[0]
    return "The {0} of {1} is {2}.".format(property, element, property_value)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
