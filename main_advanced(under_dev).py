import speech_recognition as sr
from time import ctime
from tkinter import *  # for keypress
from pynput.keyboard import Key, Listener

import time
import webbrowser
import os
import playsound
import random
import psutil
import signal
from gtts import gTTS
import pyaudio

# r.energy_threshold = 100
Check = True
Listen = False
Respond = False
r = sr.Recognizer()
r.energy_threshold = 10000000
#r.dynamic_energy_threshold = False
##############################################
'''def KeyuP(e):
    if e.char == 'm' or e.char == 'M':
        r.energy_threshold = 10000000
        print(r.energy_threshold)
'''

'''def KeydowN(e):
    global Check
    if e.char == 'm' or e.char == 'M':
        if Check==True:
            r.energy_threshold = 0
            Check = False
        elif Check==False:
            r.energy_threshold = 10000000
            Check = True
        print(r.energy_threshold)
root = Tk()
frame = Frame(root)
frame.bind("<KeyPress>", KeydowN)
frame.pack()
frame.focus_set()
root.mainloop()
'''
'''def Activate():
    with Listener(on_press=KeydowN, on_release = KeyuP) as listener:
        listener.join()
'''
##############################################
##############################################
def EndProc(ProcessName):
    closed = False
    for proc in psutil.process_iter():
        try:
            procinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            if ProcessName.lower() in procinfo['name'].lower():
                os.kill(procinfo['pid'], signal.SIGTERM)
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            BotSpeak('No Such Process Exists sir')
        # print(closed)
    if closed:
        BotSpeak('closed ' + ProcessName)


###############################################
def recordaudio(ask=False):
    #Activate()
    with sr.Microphone() as source:
        if ask:
            BotSpeak(ask)
        # r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            # BotSpeak(voice_data)
            print(voice_data)

        except sr.UnknownValueError:
            if Listen:
                BotSpeak('Sorry, I did not get that.')
        except sr.RequestError:
            BotSpeak('Sorry, my speech service is down.')
        return voice_data


#################################################
def BotSpeak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


##################################################
def respond(voice_data):
    if 'what is your name' in voice_data:
        BotSpeak("My name is Siri")
    elif 'what time is it' in voice_data:
        BotSpeak(ctime())
    elif 'search' in voice_data:
        search = voice_data[7:300]
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        BotSpeak('Here is what I found for ' + search)
    elif 'find location' in voice_data:
        location = recordaudio('What is the location?')
        url = 'https://google.com/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        BotSpeak('Here is the location of ' + location)
    elif 'open ' in voice_data:
        app = voice_data[5:300]
        BotSpeak('Opening ' + app)
        if ('Google Chrome' in app) or 'Chrome' in app:
            os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")
        elif 'discord' in app:
            os.startfile("C:\shortcuts\Discord")
    elif 'close' in voice_data:
        proc = voice_data[6:300]
        if ('Google Chrome' in proc) or 'Chrome' in proc:
            proc = 'chrome'
        elif 'spotify' in proc:
            proc = 'spotify'
        EndProc(proc)
    global Listen
    Listen = False


# time.sleep(1)

# JarvisSpeak('How can i help you?')
while 1:

    '''if keyboard.on_press('M'):
        r.energy_threshold = 0
    if keyboard.on_release_key('M'):
        r.energy_threshold = 1000000
    '''
    # Listen = False
    time.sleep(0.2)
    voice_data = recordaudio()
    # print(Listen)
    print(r.energy_threshold)
    if 'Siri' in voice_data:
        Listen = True
        voice_data = voice_data[5:100]
        # BotSpeak('How can i help you?')
        # continue
    if 'terminate' in voice_data:
        BotSpeak('Terminating')
        exit()
    if 'exit' in voice_data:
        Listen = False
        BotSpeak('i am going to sleep')
    if Listen:
        respond(voice_data)