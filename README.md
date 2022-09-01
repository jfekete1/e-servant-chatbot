# e-servant-chatbot
A deep learning chatbot created with Python and Flask.
This is a customizable hungarian speaking chatbot based on the python-deep-learning-chatbot and the lara-hungarian-nlp.

To get started follow the steps below:

2. Install all the required libraries 
```
sudo apt install espeak
sudo apt install ffmpeg
pip install flask_cors
pip install flask
pip install google
pip install pyttsx3
pip install waitress
```

Run the chatbot.py file to create the model
```
python chatbot.py
```

Run the APP to create a Flask front end on port 8888 (or any port the app is pointing to)
```
python app.py
```

# IF YOU WANT HTTPS

https://dev.to/thetrebelcc/how-to-run-a-flask-app-over-https-using-waitress-and-nginx-2020-235c

http://esh-mqtt-0.esh.hu/ -> http://185.80.48.166
http://esh-mqtt-0.esh.hu:8080 -> http://185.80.48.166

#install certbot:
which snap
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx

#refresh cert:
sudo certbot renew --dry-run

https://esh-mqtt-0.esh.hu

sudo vi /etc/nginx/sites-available/default
location / {
    proxy_pass http://127.0.0.1:8080;
    add_header Access-Control-Allow-Origin *;
}
sudo systemctl restart nginx

