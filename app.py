from flask import Flask, render_template, jsonify, request
import processor
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from lara import parser, entities


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ez-a-kulcsom-3479373872943'


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())



@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():

    if request.method == 'POST':
        the_question = request.form['question']

        response = processor.chatbot_response(the_question)

        if response == "Kérésed feldolgozás alatt.":
            print("Meg kell állapítani a kérés tartalma alapján a végrehajtandó feladatot.")
            response = "Kérésed feldolgozás alatt: "
            commands = entities.commands()
            commands_match = parser.Intents(commands).match_set(the_question)

            if commands_match:
                print('Az alábbi feladatokat adtad ki a számomra:')
                for command in commands_match:
                    print(command)
                    response += processor.do_job(command, the_question)

    return jsonify({"response": response })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
