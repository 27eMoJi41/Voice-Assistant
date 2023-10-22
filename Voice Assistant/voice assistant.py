# Voice Assistant by Emirhan ÖZKAYA

import sqlite3
import time
import webbrowser
import datetime
import speech_recognition as sr
import pyttsx3
import wikipedia
import pyautogui
import keyboard
from playsound import playsound
import pywhatkit

class voice_assistant:
    def __init__(self):
        super().__init__()
        self.i = 0
        self.first_date()

    def speak(self, say):
        engine = pyttsx3.init()
        engine.say(say)
        engine.runAndWait()

    def greeting(self):
        hour = datetime.datetime.now().hour
        playsound('Luna.mp3')
        time.sleep(3)
        if (hour >= 7 and hour < 12):
            self.speak("Good Morning " + self.name[0][0])
        elif (hour >= 12 and hour < 18):
            self.speak("Good Afternoon " + self.name[0][0])
        elif (hour >= 18 and hour < 21):
            self.speak("Good Evening " + self.name[0][0])
        else:
            self.speak("Good Night " + self.name[0][0])

        self.speak("How can i help you?")
        self.listen()

    def first_date(self):
        con = sqlite3.connect("user.db")
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS USER(Name TEXT,Surname TEXT)")
        con.commit()

        cursor.execute("select * from USER")
        self.name = cursor.fetchall()
        if (len(self.name) == 0):
            playsound('S_Harmonics.mp3')
            time.sleep(4.5)
            self.speak("Hi. My name is Friday. I will always be here for you. What is your name sir?")
            self.response = sr.Recognizer()
            mic = sr.Microphone(device_index=1)
            with mic as source:
                self.response.adjust_for_ambient_noise(source, duration=1)
                playsound('Crystal.mp3')
                time.sleep(1.5)
                print("Listening")
                audio = self.response.listen(source, timeout=1)

            try:
                self.phrase = self.response.recognize_google(audio, language="in-EN")
                self.phrase = self.phrase.lower()
                print(self.phrase)
            except sr.UnknownValueError:
                self.speak("Sorry,I did not get that.Please repeat")

            self.name_list = self.phrase.split(" ")

            cursor.execute("insert into USER VALUES(?,?)", (self.name_list[0], self.name_list[1]))
            con.commit()

            cursor.execute("select * from USER")
            self.name = cursor.fetchall()
            self.greeting()

        else:
            self.greeting()

    def re_listen(self):
        self.response = sr.Recognizer()
        mic = sr.Microphone(device_index=1)
        with mic as source:
            playsound('Crystal.mp3')
            time.sleep(1.5)
            print("Listening")
            self.response.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.response.listen(source, timeout=1)
        try:
            self.phrase = self.response.recognize_google(audio, language="in-EN")
            self.phrase = self.phrase.lower()
            print(self.phrase)
        except sr.UnknownValueError:
            self.speak("You don't say anything.")
            self.phrase = "repeat"
        return self.phrase

    def listen(self, lan='"in-EN"'):
        while (1):  # 4127
            if keyboard.is_pressed('tab'):
                self.response = sr.Recognizer()
                mic = sr.Microphone(device_index=1)
                with mic as source:
                    playsound('Crystal.mp3')
                    time.sleep(1.5)
                    print("Listening")
                    self.response.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.response.listen(source, timeout=5)

                if self.i == 3:
                    playsound('Ivory.mp3')
                    time.sleep(1.5)
                    self.speak(
                        "I close the program because you did not make any requests.Have a good day " + self.name[0][0])
                    break
                try:
                    self.phrase = self.response.recognize_google(audio, language=lan)
                    self.phrase = self.phrase.lower()
                    print(self.phrase)
                except sr.UnknownValueError:
                    self.speak("You don't say anything. I will close soon.")
                    self.i += 1
                    self.phrase = ""

                if (len(self.phrase) != 0):
                    self.i = 0

                if "open" in self.phrase:
                    list = self.phrase.split(" ")
                    a = list.index("open")
                    if ("." in list[a + 1]):
                        webbrowser.open_new_tab("https://www." + list[a + 1])
                    else:
                        webbrowser.open_new_tab("https://www." + list[a + 1] + ".com")
                    self.speak("I am opening " + list[a + 1])

                elif "don't listen" in self.phrase or "stop listening" in self.phrase or "stop listen" in self.phrase:
                    self.speak("for how much second you want")
                    try:
                        a = int(self.re_listen())
                        self.speak("Okay. I am not listen to " + str(a) + "second.")
                        time.sleep(a)
                        self.speak("I am back and ready for listen.")
                    except:
                        pass

                elif "youtube" in self.phrase:
                    list = self.phrase.split(" ")
                    a = list.index("youtube")
                    search = ""
                    for i in list[a + 1:]:
                        search += str(i + " ")  # 1402
                    webbrowser.open_new_tab("http://www.youtube.com/results?search_query=" + search)
                    self.speak("I am searching" + search + "in youtube")

                elif "play" in self.phrase:
                    list = self.phrase.split(" ")
                    a = list.index("play")
                    search = ""
                    for i in list[a + 1:]:
                        search += str(i + " ")
                    pywhatkit.playonyt(search)

                elif "search" in self.phrase:
                    list = self.phrase.split(" ")
                    a = list.index("search")
                    search = ""
                    for i in list[a + 1:]:
                        search += str(i + " ")
                    webbrowser.open_new_tab("https://www.google.com/search?q=+" + search)
                    if "on google" in self.phrase:
                        self.speak("I am searching " + search)
                    else:
                        self.speak("I am searching " + search + "on Google")

                elif "wikipedia" in self.phrase:
                    list = self.phrase.split(" ")
                    a = list.index("wikipedia")
                    search = ""
                    for i in list[a + 1:]:
                        search += str(i + " ")
                    try:
                        outcome = wikipedia.summary(search, sentences=2)
                        self.speak(outcome)
                    except:
                        self.speak("I could not find anything about it.")

                elif "screenshot" in self.phrase:
                    self.speak("I am taking screenshot.")
                    date_now = datetime.date.today()
                    time_now = datetime.datetime.now().strftime("%H-%M-%S")
                    pyautogui.screenshot('my_screenshot_' + str(date_now) + '_' + str(time_now) + '.png')

                elif "type" in self.phrase:
                    list = self.phrase.split(" ")
                    a = list.index("type")
                    v_type = ""
                    for i in list[a + 1:]:
                        v_type += str(i + " ")
                    self.speak("I am typing it.")
                    pyautogui.typewrite(v_type, interval=0.05)

                elif "where is" in self.phrase:
                    list = self.phrase.split(" ")
                    a = list.index("where")
                    search = ""
                    for i in list[a + 2:]:
                        search += str(i + " ")
                    webbrowser.open_new_tab("https://www.google.com/maps/place/" + search + "/&amp;")
                    self.speak("I am showing you " + search)

                elif "how are you" in self.phrase or "what about you" in self.phrase:
                    self.speak("Fine, thank you.")

                elif "who are you" in self.phrase:
                    self.speak("I am ," + self.name[0][0] + "'s self voice assistant.")

                elif "time" in self.phrase:
                    time_now = datetime.datetime.now().strftime("%H:%M:%S")
                    self.speak("The time is {}".format(time_now))

                elif "date" in self.phrase:
                    date_now = datetime.date.today()
                    self.speak("The date is" + str(date_now))

                elif "hello" == self.phrase:
                    self.speak("Yes I am here " + self.name[0][0] + ". I am listening you.")

                else:
                    self.speak("I couldn't understand what you said")

voice_assistant()