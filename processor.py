import pyttsx3
from googlesearch import search
import re
import os
import sys, base64
import time



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

