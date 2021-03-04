import speech_recognition as sr
from time import ctime
import time
import webbrowser
import os
import playsound
import random
from gtts import gTTS


Listen = False
Respond = False
r = sr.Recognizer()

def recordaudio(ask = False):
    with sr.Microphone() as source:
        if ask:
            BotSpeak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            #JarvisSpeak(voice_data)
            print(voice_data)
        except sr.UnknownValueError:
            if Listen:
                BotSpeak('Sorry, I did not get that.')
        except sr.RequestError:
            BotSpeak('Sorry, my speech service is down.')
        return voice_data

def BotSpeak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def respond(voice_data):
    if 'what is your name' in voice_data:
        BotSpeak("My name is Jarvis")
    if 'what time is it' in voice_data:
        BotSpeak(ctime())
    if 'search' in voice_data:
        search = recordaudio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        BotSpeak('Here is what I found for ' + search)
    if 'find location' in voice_data:
        location = recordaudio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        BotSpeak('Here is the location of ' + location)
    if 'open Google' in voice_data:
        BotSpeak('Opening Google Chrome')
        os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")
    global Listen
    Listen = False


#time.sleep(1)

#JarvisSpeak('How can i help you?')
while 1:
    #Listen = False
    time.sleep(0.2)
    voice_data = recordaudio()
    #print(Listen)
    if 'Siri' in voice_data:
        Listen = True
        BotSpeak('How can i help you?')
        continue
    if 'terminate' in voice_data:
        BotSpeak('Terminating')
        exit()
    if 'exit' in voice_data:
        Listen = False
        BotSpeak('i am going to sleep')
    if Listen:
        respond(voice_data)
