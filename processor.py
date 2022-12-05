import pyttsx3
from googlesearch import search
import re
import os
import sys, base64
import time
import random
import requests
import json

telszamok = {
    "lacusnak": "36317000331",
    "danonak": "36309817729",
    "danónak": "36309817729",
    "apusnak": "36304742067",
	"ainak": "36303303527"
}

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

def greeting(id):
    msg = ""
    greeting_list = [" Szia! ", " Szervusz! ", " Szevasz! ", " Hello! ", " Üdvözöllek! "]
    if id == 'hi':
        msg = random.choice(greeting_list)
    return msg

def answer_common(id):
    msg = ""
    if id == 'profanity':
        msg += " Kérlek szépen kommunikálj velem! "
    elif id == 'thx':
        msg += " Egyébként szívesen máskor is! "
    elif id == 'sorry':
        msg += " Semmi baj, megbocsátok. "
    elif id == 'nvm':
        msg += " Szerintem is mindegy. "
    elif id == 'dontknow':
        msg += " Sajnos erről a témáról nincs elég információm. Beszéljünk másról. "
    elif id == 'whathelp':
        msg += " Több mindenben tudok segíteni. Fel tudok olvasni, illetve le tudok fordítani bármilyen szöveget. Rá is tudok keresni bármire, illetve tudok SMS-t küldeni a kontaktjaidnak!"
    return msg

def answer_command(jobname, question, num):
    msg = ""
    if jobname == 'tea':
        if num > 0:
            msg += " ŐŐŐ, Ja és a Tea készítés is folyamatban van. "
        else:
            msg += " Tea készítés folyamatban. "
    elif jobname == 'menu':
        if num > 0:
            msg += " ŐŐŐ, Ja és készítek neked egy menüt. "
        else:
            msg += " Készítek neked egy menüt. "
    elif jobname == 'something':
        if num > 0:
            msg += " ŐŐŐ, a valami részt nem értem. Pontosítsd mire gondolsz. "
        else:
            msg += " Nem tudom mit értesz a valami alatt, kérlek pontosítsd a kérésed. "
    elif jobname == 'install':
        if num > 0:
            msg += " ŐŐŐ, nem értem mit szeretnél telepítani. "
        else:
            msg += " Nem tudom mit szeretnél telepíteni. "
    elif jobname == 'sms':
        smsRecipient = "a senkinek"
        try:
            smsRecipient = re.search('(\w+nak)', question).group(0)
        except AttributeError:
            pass
        print("Neki küldök SMS-t: ", smsRecipient)
        msg += " SMS-t küldtem " + smsRecipient
        number='36703089523'
        for name, telszam in telszamok.items():
            if smsRecipient.lower() == name:
                number=telszam

        print("Erre a számra küldöm az SMS-t: ", number)

        smsText = ""
        try:
            smsText = re.search('hogy (.*?)$', question).group(1)
        except AttributeError:
            pass
        smsText = smsText.rstrip('\"')
        print("Ezt a szöveget küldöm el SMS-ben: ", smsText)
        msg += ", ezzel a szöveggel: " + smsText
        send_sms(smsText, number)



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
        msg += " Találat: " + google_search(found)
        msg = msg.rstrip('\/')
    else:
        msg += "Ismeretlen parancs. "
    return msg

def create_wav(txt, filename):
    parancs = "/usr/bin/espeak -w " + filename + " -v hu+f2" + " " + "\"" + txt + "\""
    os.system(parancs)

def create_mp3(txt, filename):
    engine = pyttsx3.init()
    engine.setProperty('voice','hungarian+f2')
    engine.save_to_file(txt, filename)
    engine.runAndWait()
    engine.stop()

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

def send_sms(message, number ='36703089523', key ='94qz15cnc0jvpoug7pcpghorhawvfjueff86'):
    if message == "":
        message = 'Teszt üzenet'
    url = "https://seeme.hu/gateway"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    params = {
        'key': key,
        'message': message,
        'number': number,
        'callback': '4,6,7',
        'format': 'json'
    }

    r=requests.get(url, headers=headers, params=params)
    print(r)



