from flask_cors import CORS
import json
import calendar
import time
from lara import parser, entities
from flask import Flask, render_template, jsonify, request, send_file
import processor
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'ez-a-kulcsom-3479373872943'


def create_wav(txt, filename):
    parancs = "/usr/bin/espeak -w " + filename + " -v hu+f2" + " " + txt
    os.system(parancs)

# @app.route('/', methods=["GET", "POST"])
# def index():
#     return render_template('index.html', **locals())


@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():

    if request.method == 'POST':
        the_question = request.form['question']

        response = processor.chatbot_response(the_question)

        if response == "Kérésed feldolgozás alatt.":
            print(
                "Meg kell állapítani a kérés tartalma alapján a végrehajtandó feladatot.")
            response = "Kérésed feldolgozás alatt: "
            commands = entities.commands()
            commands_match = parser.Intents(commands).match_set(the_question)

            if commands_match:
                print('Az alábbi feladatokat adtad ki a számomra:')
                for command in commands_match:
                    print(command)
                    response += processor.do_job(command, the_question)

    return jsonify({"response": response})


@app.route('/speech', methods=['GET'])
def get_speech():
    txt = request.args.get('speech')
    print("Ezt a stringet kaptam: ")
    print(txt)
    current_GMT = time.gmtime()
    ts = calendar.timegm(current_GMT)
    filename = str(ts) + ".mp3"
    filename2 = "feladatok.mp3"
    response = processor.chatbot_response(txt, filename)

    if response == "Kérésed feldolgozás alatt.":
        print("Meg kell állapítani a kérés tartalma alapján a végrehajtandó feladatot.")
        response = "Kérésed feldolgozás alatt: "
        commands = entities.commands()
        commands_match = parser.Intents(commands).match_set(txt)

        if commands_match:
            print('Az alábbi feladatokat adtad ki a számomra:')
            for command in commands_match:
                print(command)
                response += processor.do_job(command, txt)

    create_wav(response, filename2)
    
    url = "http://192.168.10.105:8080/file?filename=" + filename
    url2 = "http://192.168.10.105:8080/file?filename=" + filename2

    return json.dumps({'msg': response, 'file': url, 'file': url2})


@app.route('/file', methods=['GET'])
def get_file():
    filename = request.args.get('filename')
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
