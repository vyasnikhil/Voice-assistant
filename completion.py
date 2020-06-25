import speech_recognition as sr
import os
import pyautogui as pt
import re
import json,requests
import webbrowser
import playsound
import subprocess
import time
import random
import datetime
from gtts import gTTS
from time import ctime
import smtplib

r = sr.Recognizer()

# https://myaccount.google.com/lesssecureapps?pli=1

def greet():
    time1=str(datetime.datetime.now())
    time1=time1.split(" ")[-1]
    time1=time1.split(".")[0]
    time1=time1.split(":")[0]
    if(int(time1) <= 10):
        speak("Good Morning sir")
        
    elif(int(time1) <17):
        speak("Good afternoon sir")
        
    else:
        speak("Good Evening sir")
        

def mouse_open(text):
    #pt.moveTo(28,767,duration=1)
    pt.moveTo(118,1056,duration=1)
    pt.click()
    pt.typewrite(text)
    pt.moveTo(222,361,duration=1)
    pt.click()

def note(text):
    date=datetime.datetime.now()
    filename=str(date).replace(":","-")+"-note.txt"
    with open(filename,"w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe",filename])

def record_audio():
    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, my speech service is down')
        return voice_data


def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 100000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(f"wlater: {audio_string}")
    os.remove(audio_file)





def respond(voice_data):
    if 'your name' in voice_data:
        speak("My name is Wlater")
        print('My name is Wlater')
        return

    elif 'search' in voice_data:
        if 'YouTube' in voice_data:
            search_term = voice_data.split("for")[-1]
            speak('Searching YouTube')
            url = f"https://www.youtube.com/results?search_query={search_term}"
        else:
            search_term = voice_data.split("for")[-1]
            speak('Searching Google')
            url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)

    
    # elif 'open' in voice_data:
    #     app = voice_data.split("open ")[-1]
    #     app = app.title()
    #     speak('Opening {}'.format(app))
    #     os.system("""cd.. """)
    #     os.system("""cd.. """)
    #     os.system(""" start "{}" """.format(app) )

    # elif 'close' in voice_data:
    #     app = voice_data.split("close ")[-1]
    #     app = app.title()
    #     speak('Closing {}'.format(app))
    #     os.system("pkill {}".format(app))


    elif 'time' in voice_data:
        date=str(datetime.datetime.now())
        date=date.split(" ")[-1]
        date=date.split(".")[0]
        date=date.split(":")[0:2]
        hours=date[0]
        minutes=date[1]
        ap="AM"
        if int(hours) > 12:
            ap="PM"

        time=f'{hours} {minutes}'
        speak(time+" "+ap)
        return
        # time = ctime().split(" ")[3].split(":")[0:2]
        # if time[0] == "00":
        #     hours = '12'
        # else:
        #     hours = time[0]
        # minutes = time[1]
        # time = f'{hours} {minutes}'
        # speak(time)   
    elif 'make a note' in voice_data:
        speak('making note')
        note(voice_data.split("of")[-1])

    elif 'email' in voice_data:
        text=voice_data.split("to")[-1]
        content=text.split("that")[-1]
        recepeint=text.split("that")[0]
        # speak(recepeint+",is that correct?")
        # response=record_audio()
        # if "no" in  response:
        #     speak("then please repeat the email address.")
        #     recepeint=record_audio()
        # else:
        # recepeint.strip()
        # recepeint.replace(" ","")
        recepeint=''.join(recepeint.split())
        recepeint=recepeint.lower()
        print(recepeint)
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("vyasnik30@gmail.com","voice3098")
        s.sendmail("vyasnik30@gmail.com",recepeint+"@gmail.com",content)
        s.quit()
        speak("message sent")
        return
    elif 'open' in voice_data:
        text=voice_data.split('open')[-1]
        speak('opening'+text)
        mouse_open(text)


    elif 'weather' in voice_data:
        city=voice_data.split("of")[-1]
        api_key="b4f5c93b041d8688df5ce112df3015df"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        url=base_url+"q="+city+"&appid="+api_key
        response=requests.get(url)
        x=response.json()

        if x["cod"]!=404:
            y=x["main"]
            temp=y["temp"]
            pressure=y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]

            speak("temperature in kelvin is :"+ str(temp))
            speak("current humidity is :"+str(current_humidiy))
            speak("current weather is :"+str(weather_description))
            return

        else:
            speak("city not found!")
            return




    elif 'exit' in voice_data:
        speak('Exiting')
        exit()


time.sleep(1)
greet()
speak('I am Wlater. How,can i help you ?')
while 1:
    voice_data = record_audio()
    print("You: "+voice_data)
    respond(voice_data)
    