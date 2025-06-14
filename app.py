# for development
# from flask_cors import CORS

from pprint import pprint
import json
import calendar
import time
from lara import parser, entities
from flask import Flask, render_template, jsonify, request, send_file
import processor
import os
import os.path
from datetime import datetime
from functools import wraps
from pymongo import MongoClient

import openai
from flask import Flask, redirect, render_template, request, url_for

import sys
from waitress import serve
sys.path.append(os.path.join(os.path.dirname(
    os.path.realpath(__file__)), os.pardir))


#####################################################################################################################
# Variables block
#####################################################################################################################

app = Flask(__name__)
# for development
# CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.config['SECRET_KEY'] = 'ez-a-kulcsom-3479373872943'
API_KEY = os.getenv("WEATHER_API_KEY", "supersecret123")

# Connect to MongoDB (default local Docker port)
client = MongoClient("mongodb://localhost:27017/")
# Select DB and collection
db = client["weather_db"]
collection = db["weather_data"]
#####################################################################################################################




#####################################################################################################################
# Functions block
#####################################################################################################################

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        key = request.headers.get("DD-API-KEY")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return view_function(*args, **kwargs)
    return decorated_function

def save_data(data):
    # Add timestamp to each record
    data["timestamp"] = datetime.utcnow()

    # Insert the document into the MongoDB collection
    result = collection.insert_one(data)
    return result.inserted_id
    #print(f"Inserted weather data with ID: {result.inserted_id}")

""" def save_data(data):
    # Get today's date as a string, e.g. '2025-06-14'
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Construct the filename with the date
    data_file = f"weather_data_{today_str}.json"

    existing_data = []

    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: JSON file {data_file} is empty or malformed. Overwriting.")
                existing_data = []

    existing_data.append(data)

    with open(data_file, 'w') as f:
        json.dump(existing_data, f, indent=2) """
#####################################################################################################################




#####################################################################################################################
# Routes block
#####################################################################################################################

""" @app.route("/api/v1/weather", methods=["POST"])
def receive_weather():
    try:
        data = request.get_json(force=True)
        print("Received weather data:", data)
        save_data(data)
        return jsonify({"status": "ok", "received": data}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 400 """

@app.route("/api/v1/weather", methods=["POST"])
def receive_weather():
    try:
        data = request.get_json(force=True)
        print("Received weather data:", data)

        # Save to DB
        inserted_id = save_data(data)

        # Make a copy WITHOUT the MongoDB _id (to prevent jsonify error)
        response_data = {k: v for k, v in data.items() if k != "_id"}

        return jsonify({
            "status": "ok",
            "inserted_id": str(inserted_id),
            "received": response_data
        }), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 400


# @app.route('/', methods=["GET", "POST"])
# def index():
#     return render_template('index.html', **locals())

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        try:
            with open('data.txt', 'r') as file:
                message = file.read()
                message = message.replace('\n', '<br>')
                file.close()
           #return jsonify({'message': message})
            return message
        except FileNotFoundError:
            return jsonify({'message': 'Data file not found'}), 404

    if request.method == 'POST':
        try:
            data = request.json
            message = data.get('message')

            if message:
                with open('data.txt', 'w') as file:
                    file.write(message)
                    file.close()

                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'error'})

        except Exception as e:
            return jsonify({'status': str(e)})

@app.route('/deletefiles', methods=['DELETE'])
def deletefiles():
    print("deletefiles route activated ")
    response = delete_files()
    return json.dumps({'msg': "ASDASDADSASD"})

@app.route('/weatherdog.jpg')
def serve_image():
    return send_from_directory('static', 'weatherdog.jpg')

#####################################################################################################################




def write_to_file(text, filename):
    f = open(filename, "a")
    f.write(text)
    f.close()

def delete_files():
    files = os.listdir('.')
    for file in files:
        if '.' not in file and not os.path.isdir(file):
                os.remove(file)
    return "deleted all files"

def write_to_resp(text):
    f = open("resp.txt", "a")
    f.write(text)
    f.close()

def generate_prompt(text, filename):
    if text:
        text = "\nHuman: " + text
    if not os.path.exists(filename):
        f = open("prompt.txt", "r")
        data = f.read()
        f.close()
        write_to_file(data, filename)
    write_to_file(text, filename)
    f = open(filename, "r")
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
