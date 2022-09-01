from flask_cors import CORS
import json
import calendar
import time
from lara import parser, entities
from flask import Flask, render_template, jsonify, request, send_file
import processor
import os.path
import sys
from waitress import serve
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'ez-a-kulcsom-3479373872943'

# @app.route('/', methods=["GET", "POST"])
# def index():
#     return render_template('index.html', **locals())

# @app.route('/', methods=["GET", "POST"])
# def index():
#     return "asdasd"

@app.route('/', methods=["GET", "POST"])
def index():
    txt = request.args.get('speech')
    if txt == "":
        txt = "szia"
    print("Ezt a stringet kaptam: ")
    print(txt)
    current_GMT = time.gmtime()
    ts = calendar.timegm(current_GMT)
    filename = str(ts) + ".mp3"

    print("Meg kell állapítani a kérés tartalma alapján a végrehajtandó feladatot.")
    response = ""
    commands = entities.commands()
    commands_match = parser.Intents(commands).match_set(txt)

    if commands_match:
        print('Az alábbi feladatokat adtad ki a számomra:')
        i = 0
        for command in commands_match:
            print(command)
            response += processor.do_job(command, txt, i)
            i = i + 1

        time.sleep(1)
        wav_str = processor.create_base64_wav(response, filename)

        return json.dumps({'msg': response, 'wavstr': wav_str})
    else:
        response = "Ismeretlen utasítás, kérlek olyan utasítást adj, amit tudok teljesíteni !"
        wav_str = processor.create_base64_wav(response, filename)
        return json.dumps({'msg': response, 'wavstr': wav_str})

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

    print("Meg kell állapítani a kérés tartalma alapján a végrehajtandó feladatot.")
    response = ""
    commands = entities.commands()
    commands_match = parser.Intents(commands).match_set(txt)

    if commands_match:
        print('Az alábbi feladatokat adtad ki a számomra:')
        i = 0
        for command in commands_match:
            print(command)
            response += processor.do_job(command, txt, i)
            i = i + 1

        time.sleep(1)
        wav_str = processor.create_base64_wav(response, filename)

        return json.dumps({'msg': response, 'wavstr': wav_str})
    else:
        response = "Ismeretlen utasítás, kérlek olyan utasítást adj, amit tudok teljesíteni !"
        wav_str = processor.create_base64_wav(response, filename)
        return json.dumps({'msg': response, 'wavstr': wav_str})


@app.route('/file', methods=['GET'])
def get_file():
    filename = request.args.get('filename')
    return send_file(filename, as_attachment=True)


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='8080', debug=True)

def main_prod():
    serve(app, host='0.0.0.0', port=8080, url_scheme='https')


if __name__ == '__main__':
    main_prod()
