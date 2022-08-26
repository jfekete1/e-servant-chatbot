import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pyttsx3
from googlesearch import search
import re
import os
import sys, base64
import time

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('job_intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
        else:
            result = "You must ask the right questions"
    return result

def say_locally(txt):
    engine = pyttsx3.init()
    engine.setProperty('voice','hungarian+f2')
    engine.setProperty('rate', 150)
    engine.say(txt)
    engine.runAndWait()
    engine.stop()

def google_search(query):
    for j in search(query, tld="com", num=1, stop=1, pause=2):
        print(j)
        return j

def do_job(jobname, question, num):
    msg = ""
    if jobname == 'tea':
        if num > 0:
            msg += " ŐŐŐ, Ja és a Tea készítés is folyamatban van. "
        else:
            msg += " Tea készítés folyamatban. "
        # say_locally(msg)
    elif jobname == 'menu':
        if num > 0:
            msg += " ŐŐŐ, Ja és készítek neked egy menüt. "
        else:
            msg += " Készítek neked egy menüt. "
        # say_locally(msg)
    elif jobname == 'something':
        if num > 0:
            msg += " ŐŐŐ, a valami részt nem értem. Pontosítsd mire gondolsz. "
        else:
            msg += " Nem tudom mit értesz a valami alatt, kérlek pontosítsd a kérésed. "
    elif jobname == 'search':
        if num > 0:
            msg += " Ja és erre a szövegre indítok google keresést: "
        else:
            msg += " Erre a szövegre indítok google keresést: "
        found = "e-servant"
        try:
            found = re.search('hogy (.*?)$', question).group(1)
        except AttributeError:
            pass
        print("Ezt a keresési feltételt találtam: ", found)
        msg += found
        # say_locally(msg)
        msg += " Találat: " + google_search(found)
        msg = msg.rstrip('\/')
    else:
        msg += "Ismeretlen parancs. "
        # say_locally(msg)
    return msg

def create_wav(txt, filename):
    parancs = "/usr/bin/espeak -w " + filename + " -v hu+f2" + " " + "\"" + txt + "\""
    os.system(parancs)

def create_base64_wav(txt, filename):
    engine = pyttsx3.init()
    engine.setProperty('voice','hungarian+f2')
    engine.save_to_file(txt, filename)
    engine.runAndWait()
    engine.stop()
    time.sleep(1)
    f = open(filename, 'rb')
    b = base64.b64encode(f.read())
    b_str = b.decode()
    f.close()
    time.sleep(1)
    parancs = "/usr/bin/rm -f ./" + filename
    os.system(parancs)
    return b_str


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    # wav_str = create_base64_wav(res, filename)
    # tuple_return = (res, wav_str)
    # return tuple_return
    return res
