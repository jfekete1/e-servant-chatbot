# for development
# from flask_cors import CORS

from pprint import pprint
import json
import calendar
import time
from lara import parser, entities
from flask import Flask, render_template, jsonify, request, send_file
import processor
import os.path

import openai
from flask import Flask, redirect, render_template, request, url_for

import sys
from waitress import serve
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))


app = Flask(__name__)
# for development
# CORS(app)
openai.api_key = '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'
app.config['SECRET_KEY'] = 'ez-a-kulcsom-3479373872943'

# @app.route('/', methods=["GET", "POST"])
# def index():
#     return render_template('index.html', **locals())

@app.route('/api', methods=["GET", "POST"])
def api():
    if request.method == 'GET':
        with open('trained_model.json') as f:
            data = json.load(f)
            return jsonify(data)
    if request.method == 'POST':
        # data = request.get_json(force=True)
        data = request.json
        print('icomming request: ')
        print(request.args)
        print(data)
        with open('trained_model.json', 'w') as json_file:
            json.dump(data, json_file)
        return jsonify(data)
    else:
        return "ERROR: Unknown method"

@app.route('/', methods=["GET", "POST"])
def index():
    txt = request.args.get('speech')
    lang = request.args.get('lang')
    if txt == "":
        txt = "szia"
    print("Ezt a stringet kaptam: ")
    print(txt)
    print("Ezt a nyelvet kaptam: ")
    print(lang)
    current_GMT = time.gmtime()
    ts = calendar.timegm(current_GMT)
    filename = str(ts) + ".mp3"
    response = ""

    common = entities.common()
    common_match = parser.Intents(common).match_set(txt)

    if common_match:
        print("Az alábbi általános üzenetet kaptam:")
        for com in common_match:
            print(com)
            response += processor.greeting(com)

    commands = entities.commands()
    commands_match = parser.Intents(commands).match_set(txt)

    if commands_match:
        print('Az alábbi feladatokat adtad ki a számomra:')
        i = 0
        for command in commands_match:
            print(command)
            response += processor.answer_command(command, txt, i)
            i = i + 1

    if common_match:
        print("Az alábbi általános üzenetet kaptam:")
        for com in common_match:
            print(com)
            response += processor.answer_common(com)

    if response != "":
        time.sleep(1)
        wav_str = processor.create_base64_wav(response, filename, lang)

        return json.dumps({'msg': response, 'wavstr': wav_str})
    else:
        resp = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(txt),
            temperature=0.9,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        response = resp.choices[0].text
        pprint(resp)
        write_to_file(response)
        response = response[5:]
        # response = "Ismeretlen utasítás, kérlek olyan utasítást adj, amit tudok teljesíteni !"
        wav_str = processor.create_base64_wav(response, filename, lang)
        return json.dumps({'msg': response, 'wavstr': wav_str})

def write_to_file(text):
    f = open("prompt.txt", "a")
    f.write(text)
    f.close()

def write_to_resp(text):
    f = open("resp.txt", "a")
    f.write(text)
    f.close()

def generate_prompt(text):
    text = "\nHuman: " + text
    write_to_file(text)
    f = open("prompt.txt", "r")
    data = f.read()
    f.close()
    return data

@app.route('/speech', methods=['GET'])
def get_speech():
    txt = request.args.get('speech')
    if txt == "":
        txt = "szia"
    print("Ezt a stringet kaptam: ")
    print(txt)
    current_GMT = time.gmtime()
    ts = calendar.timegm(current_GMT)
    filename = str(ts) + ".mp3"

    wav_str = processor.create_base64_wav(txt, filename, "hu")
    return json.dumps({'msg': txt, 'wavstr': wav_str})


@app.route('/file', methods=['GET'])
def get_file():
    filename = request.args.get('filename')
    # filename = "trained_model.json"
    return send_file(filename, as_attachment=True)

# @app.route('/sms', methods=['GET'])
# def get_sms():
#     key = request.args.get('key')
#     message = request.args.get('message')
#     number = request.args.get('number')
#     print("Sending SMS")
#     processor.send_sms(message, number, key)
#     return "asdasd"


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='8080', debug=True)

def main_prod():
    serve(app, host='0.0.0.0', port=8080, url_scheme='https')
    # serve(app, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main_prod()
