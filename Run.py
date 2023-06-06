import pyttsx3
import webbrowser
import smtplib
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
import re
from pygame import mixer  # Load the required library
import time
import datetime
import json
import Load_Data
import Commands
import Actions
import Statements
import re
import Natural_bot
import cv2
import numpy as np
import threading
from mutagen.mp3 import MP3


wolframalpha_keys = ["J462Q4-TY6PAG6UWP", "LJH5J5-KPLT7J3A6J", "4J4WE4-URJWP68LW4", "68TPE2-TV4XJT5R28",
                     "V4APGW-7TTXX2249J", "WXJ7W4-UHU8P9J2RP", "39LPG8-T4WGLTHQEU", "3RQKWG-4H36WRT7V5",
                     "U3YH8R-QRK7JY4H5P", "3HALW9-9T9KHG2UQP","YE7JT2-UWR6QGPHEA"]

engine = pyttsx3.init()

en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"  # female
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"  # male

engine.setProperty('voice', en_voice_id)

rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)

robotFailedNumbers = 0
RobotDeactivation = False

Routing_Status = False
Where_to_Route = ""

Face_Detect_Status_By_Robot_eye = False


def Database_Loader():
    Load_Data.CommandsDataLoader()
    Load_Data.ActionsDataLoader()
    Load_Data.StatementsDataLoader()
    Load_Data.loadDataset_set1()


def talk_function(audio):
    print('Computer: ' + audio)
    engine.say(audio)
    engine.runAndWait()


def greeting_function():
    currentHour = int(datetime.datetime.now().hour)
    basicGreeting = ""

    if currentHour >= 0 and currentHour < 12:
        basicGreeting = "Good Morning!"

    if currentHour >= 12 and currentHour < 18:
        basicGreeting = "Good Afternoon!"

    if currentHour >= 18 and currentHour != 0:
        basicGreeting = "Good Evening!"

    return basicGreeting


def getCurrentDate():
    from datetime import datetime, date  # depandancy

    weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    currentDate = datetime.date(datetime.now())
    dayNumber = currentDate.weekday()
    DayAsString = weekDays[dayNumber]
    today = date.today()

    date_and_day = [DayAsString, today]

    return date_and_day


def getCurrenTime():
    from time import gmtime, strftime  # depandancy
    from datetime import datetime, date  # depandancy

    currentTime = strftime("%H:%M:%S")
    d = datetime.strptime(str(currentTime), "%H:%M:%S")

    currentTime = d.strftime("%I %M %p")

    return currentTime


def RobotEye():
    global Face_Detect_Status_By_Robot_eye

    faceDetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    while (True):

        Face_Detect_Satus_Local_Variable = False

        ret, img = cam.read()
        font = cv2.FONT_HERSHEY_SIMPLEX
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, 'Face ', (x + w, y + h), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            Face_Detect_Satus_Local_Variable = True

        if Face_Detect_Satus_Local_Variable == False:
            Face_Detect_Status_By_Robot_eye = False

        elif Face_Detect_Satus_Local_Variable == True:
            Face_Detect_Status_By_Robot_eye = True

        cv2.imshow("Eye Monitor", img)
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.relese()
    cv2.destoryAllWindows();


def TurningOn():
    print("Model Loading...")

    engine.setProperty('voice', en_voice_id)

    mixer.init()
    mixer.music.load('Sound_Effects/sound1.mp3')
    mixer.music.play()
    time.sleep(2)

    mixer.init()
    mixer.music.load('Sound_Effects/sound2.mp3')
    mixer.music.play()
    time.sleep(3)

    talk_function("""Hello, {}. My name is alpha humanoid robot. My operating system version is 1.0.
    I am working at SLIATE Sammanthurai Advanced Technological Institute as a virtual assistant. My primary functions is to provide administrative services to the employees. 
    I have been programmed to do so many tasks. I can see human faces.
    I can even understand human voices and I have the ability to speak English Language.
    Not only that, but also, I can talk with people.. 
	Further I have been trained to do more works in future.
    """.format(
        greeting_function()))

    currentDateObj1 = getCurrentDate()

    print(currentDateObj1)

    talk_function(
        "Today is {},. The date is {}. and the time is {}. I wish that everyone in the SLIATE should have a nice day.".format(
            currentDateObj1[0], currentDateObj1[1], getCurrenTime()))

    talk_function("My database has been loaded. I think I am online. Now, I am ready to do my work. Bye..")

    engine.runAndWait()

    Eye = threading.Thread(target=RobotEye)
    Eye.start()

    robotActivationListening()


def robotActivationListening():
    while True:

        whilebreak = False

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1

            # r.dynamic_energy_threshold
            # r.energy_threshold = 4000

            print("Waiting to Activate...")
            audio = r.listen(source, phrase_time_limit=10)

        try:

            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            query = query.lower()
            print(query)  # Testing

            for command in Commands.Robot_Activation_Commands_List:

                if command in query:
                    whilebreak = True
                    break

            if whilebreak == True:
                print("alpha is activating...")
                robotActivating()
                break

        except sr.UnknownValueError:

            if Face_Detect_Status_By_Robot_eye == True:
                talk_function(random.choice(Statements.Robot_Activation_Greeting))

            elif Face_Detect_Status_By_Robot_eye == False:
                status = ["1","2","3"]

                if random.choice(status) == "1" or random.choice(status) == "3":
                    
                    sounds = ["sound0","sound1","sound2","sound3","sound4","sound5","sound6","sound7","sound8","sound9","sound10","sound11","sound12"]
                    
                    sound_to_play = random.choice(sounds)
                    audioDetails = MP3('Sound_Effects/Waiting_sounds/{}.mp3'.format(sound_to_play))
                    
                    audioDuration = audioDetails.info.length

                    mixer.music.load('Sound_Effects/Waiting_sounds/{}.mp3'.format(sound_to_play))
                    mixer.music.play()

                    time.sleep(audioDuration)






        except sr.RequestError:

            TheResponse = random.choice(Statements.Robot_Activation_Statements_network_problem)
            talk_function(TheResponse)


def DeactivateMoodGreeting():
    answers = ["yes", "no"]
    decision = random.choice(answers)

    if decision == "yes":
        talk_function(random.choice(Statements.Robot_Activation_Greeting))


def myCommand():
    global robotFailedNumbers, RobotDeactivation

    r = sr.Recognizer()
    with sr.Microphone() as source:
        mixer.music.load('Sound_Effects/sound3.mp3')
        mixer.music.play()
        time.sleep(0)

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=10)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')

    except sr.UnknownValueError:

        query = ""

        TheResponse = random.choice(Statements.Robot_Activation_Statements_cant_hear)
        talk_function(TheResponse)

        robotFailedNumbers = robotFailedNumbers + 1

        if robotFailedNumbers == 10:
            RobotDeactivation = True

    if query != "":
        robotFailedNumbers = 0

    return query


def robotActivating():
    print("I am Activated!.")
    mixer.init()
    mixer.music.load('Sound_Effects/sound0.mp3')
    mixer.music.play()
    time.sleep(3)

    TheResponse = random.choice(Actions.Robot_Activation_Actions_List)

    matchesGreeting = re.search(r"[{}]", TheResponse)

    if matchesGreeting:

        TheResponse = TheResponse.format(greeting_function())

    else:
        TheResponse = TheResponse

    talk_function(TheResponse)

    Router()


def selfDeactivationMood():
    global RobotDeactivation, robotFailedNumbers

    RobotDeactivation = False
    robotFailedNumbers = 0

    TheResponse = random.choice(Statements.Robot_Deactivation_Statements)

    time.sleep(1)
    talk_function(TheResponse)

    robotActivationListening()


def command1_funtion():
    TheResponse = random.choice(Actions.How_are_you_Actions_List)
    talk_function(TheResponse)

    if 'what about you' in TheResponse or 'how about you' in TheResponse or 'are you fine' in TheResponse:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for health..")
            r.pause_threshold = 1
            audio = r.listen(source, phrase_time_limit=10)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print('User: ' + query + '\n')

            query = query.lower()

            if "am fine" in query or "am also fine" in query or "ok" in query or "okey" in query or "yes" in query or "good" in query:
                response_list_1 = ["It is good to hear that", "Good", "WoW, you are happy, so i am happy",
                                   "humans are always fine", "Good, keep it up. you should always happy like this",
                                   "I know that you are happy because, I analysed your facial expressions",
                                   "Good, keep this smile always"]
                talk_function(random.choice(response_list_1))

            if "not happy" in query or "sad" in query or "problem" in query or "mood out" in query or "not fine" in query or "no" in query:
                response_list_2 = ["I pary for you to get well soon",
                                   "god bless you. don't worry, you will be recovered",
                                   "you will be fine soon, don't worry",
                                   "God will heal you, don't worry, you will be happy soon",
                                   "humans are emotional animals. that is the reason they are frequently. Kill your heart, and use your brain"]
                talk_function(random.choice(response_list_2))

        except sr.UnknownValueError:
            pass
            print("Pass")


def command2_funtion():
    TheResponse = random.choice(Actions.Robot_Name_List)
    talk_function(TheResponse)

    talk_function(random.choice(Commands.AskingTheNamesofRobotCommands))

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for name...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=10)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')

        if query != "":
            response_list = ["Nice Name", "beautiful name", "wonderful name", "Good Name", "Amazing name", "smart name",
                             "best name", "perfect name"]
            talk_function(random.choice(response_list))

            with open("UserData/Names.txt", "a") as myfile:
                myfile.write("{}\n".format(query))

    except sr.UnknownValueError:
        pass
        print("Pass")


def command4_funtion(question):
    namer = ["who named you", "who gave you this name", "who gave this name", "who named you like this"]

    namerStatus = ""

    for name in namer:
        if question == name:
            namerStatus = name

    if namerStatus != "":
        list_of_response = ["I was named by mister Infas. He is the creator of my operating system",
                            "This name was given by mister Infas.", "This beautiful name was given by mister Infas."]
        talk_function(random.choice(list_of_response))
    else:
        talk_function(random.choice(Actions.talking_about_name))


def command5_funtion(question):
    global Routing_Status, Where_to_Route

    type_of_question = ""

    exitStatus = ""

    for command5 in Commands.talking_about_work:

        if question == command5:
            exitStatus = "yes"

    if exitStatus == "yes":

        for ques in Commands.talking_about_work_place_2:

            if question == ques:
                type_of_question = "work_place"

        for ques2 in Commands.talking_about_work_duration_3:

            if question == ques2:
                type_of_question = "work_duration"

        for ques3 in Commands.talking_about_work_salary_4:

            if question == ques3:
                type_of_question = "work_salary"

        if type_of_question == "work_place":
            talk_function(random.choice(Actions.talking_about_work_place_2))

        elif type_of_question == "work_duration":
            talk_function(random.choice(Actions.talking_about_work_duration_3))

        elif type_of_question == "work_salary":
            talk_function(random.choice(Actions.talking_about_work_salary_4))

        else:
            talk_function(random.choice(Actions.talking_about_work_1))

        Routing_Status = True
        Where_to_Route = "command5_funtion"

    elif exitStatus == "":

        for questionExit in Commands.talking_about_work_salary_Extra:

            if question == questionExit:

                if question == "tell me more about your work" or question == "tell me more" or question == "explain your work" or question == "describe your work" or question == "describe your job":
                    with open("Data/Actions/Action-4_Extra.json") as d:
                        data = json.load(d)

                        TheResponse = ""

                        for x in data["more"]:
                            x = x.lower()
                            x = x.strip()
                            TheResponse = x
                            talk_function(TheResponse)

                elif question == "why don't you need money" or question == "don't you need money":

                    with open("Data/Actions/Action-4_Extra.json") as s:
                        data = json.load(s)

                        theAnswers = []

                        for s in data["reason_for_not_needed_money"]:
                            s = s.lower()
                            s = s.strip()

                            theAnswers.append(s)
                        talk_function(random.choice(theAnswers))

                else:
                    talk_function(random.choice(Actions.talking_about_work_salary_Extra))

                break

    extraQuestionStatus = "exit"

    for extraQuestion in Commands.talking_about_work_salary_Extra:
        if extraQuestion != question:
            extraQuestionStatus = ""

    if extraQuestionStatus == "" and exitStatus == "":
        Routing_Status = False
        Where_to_Route = ""
        AllFunctionalities(question)


email_spell_mistake = 0

def email_spell():

    global email_spell_mistake

    query = ""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        mixer.music.load('Sound_Effects/sound3.mp3')
        mixer.music.play()
        time.sleep(0)

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=60)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')

    except sr.UnknownValueError:
        email_mis = ["Sorry, I can't hear you. Spell the email address properly." ,"Spell the email address properly.","Sorry, Spell your email address correctly"]
        talk_function(random.choice(email_mis))
        email_spell_mistake = email_spell_mistake + 1

        if email_spell_mistake == 3:
            res = ["Sorry, I can't send you email for you. You are spelling the email address incorrectly.","I can't send you email for you. try again later. Because,  you are spelling incorrectly"]
            talk_function(random.choice(res))
        else:
            email_spell()

    return query


email_content_mistake = 0 

def email_content():

    global email_content_mistake

    query = ""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        mixer.music.load('Sound_Effects/sound3.mp3')
        mixer.music.play()
        time.sleep(0)

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=60)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')

    except sr.UnknownValueError:
        talk_function(random.choice(Statements.Robot_Activation_Statements_cant_hear))
        email_content_mistake = email_content_mistake + 1

        if email_content_mistake == 3:
            res = ["Sorry, I can't send you email for you. You are not telling the content of the email.","I can't send you email for you. try again later. Because,  you are telling incorrectly"]
            talk_function(random.choice(res))
        else:
            email_content()

    return query



def send_mail_function():
    questions = ["Okay!. Can you please, spell me the recipient's email address. Spell me, do not tell me the address at once.","Sure, Spell me the recipient's email address. Spell me"]
    talk_function(random.choice(questions))
    recipientEmail =  email_spell()

    recipientEmail = "".join(recipientEmail.split())
    recipientEmail = recipientEmail.lower()

    try:
        message_res = ["What should I say? ","Tell me the message"]
        talk_function(random.choice(message_res))
        content = email_content()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("machinealpha9@gmail.com", 'machinealpha123456789')
        server.sendmail('machinealpha9@gmail.com', recipientEmail , content)
        print("sent to {}".format(recipientEmail))

        server.close()
        talk_message = ["Email was sent!","The email was sent successfully."] 
        talk_function(random.choice(talk_message))

    except:
        res = ['Sorry!, I am unable to send your message at this moment!',"Something went wrong. I can't send the email right now"]
        talk_function(random.choice(res))

    



def command6_funtion(question):
    routePath = ""
    greeting_basic_1 = []
    greeting_basic_2 = []
    greeting_basic_3 = []
    greeting_basic_4 = []
    greeting_basic_5 = []
    greeting_basic_6 = []
    greeting_basic_7 = []
    greeting_basic_8 = []
    greeting_basic_9 = []
    greeting_basic_10 = []

    with open("Data/Commands/Command-5.json") as basic_1:
        data = json.load(basic_1)

        for d1 in data["greetings_basic_1"]:
            d1 = d1.lower()
            d1 = d1.strip()
            greeting_basic_1.append(d1)

        for d2 in data["greetings_basic_2"]:
            d2 = d2.lower()
            d2 = d2.strip()
            greeting_basic_2.append(d2)

        for d3 in data["greetings_basic_3"]:
            d3 = d3.lower()
            d3 = d3.strip()
            greeting_basic_3.append(d3)

        for d4 in data["greetings_basic_4"]:
            d4 = d4.lower()
            d4 = d4.strip()
            greeting_basic_4.append(d4)

        for d5 in data["greetings_basic_5"]:
            d5 = d5.lower()
            d5 = d5.strip()
            greeting_basic_5.append(d5)

        for d6 in data["greetings_basic_6"]:
            d6 = d6.lower()
            d6 = d6.strip()
            greeting_basic_6.append(d6)

        for d7 in data["greetings_basic_7"]:
            d7 = d7.lower()
            d7 = d7.strip()
            greeting_basic_7.append(d7)

        for d8 in data["greetings_basic_8"]:
            d8 = d8.lower()
            d8 = d8.strip()
            greeting_basic_8.append(d8)

        for d9 in data["greetings_basic_9"]:
            d9 = d9.lower()
            d9 = d9.strip()
            greeting_basic_9.append(d9)

        for d10 in data["greetings_basic_10"]:
            d10 = d10.lower()
            d10 = d10.strip()
            greeting_basic_10.append(d10)

    for ques in greeting_basic_1:

        if question == ques:
            with open("Data/Actions/Action-5.json") as da:
                data = json.load(da)

                responses = []

                for x in data["greetings_basic_1"]:
                    responses.append(x)
                talk_function(random.choice(responses))

            break

    for ques in greeting_basic_2:

        if question == ques:
            with open("Data/Actions/Action-5.json") as da:
                data = json.load(da)

                responses = []

                for x in data["greetings_basic_2"]:
                    responses.append(x)
                talk_function(random.choice(responses))
            break

    for ques in greeting_basic_3:

        if question == ques:
            with open("Data/Actions/Action-5.json") as da:
                data = json.load(da)

                responses = []

                for x in data["greetings_basic_3"]:
                    responses.append(x)
                talk_function(random.choice(responses))
            break

    for ques in greeting_basic_4:

        if question == ques:
            with open("Data/Actions/Action-5.json") as da:
                data = json.load(da)

                responses = []

                for x in data["greetings_basic_4"]:
                    responses.append(x)
                talk_function(random.choice(responses))
            break

    for ques in greeting_basic_5:

        if question == ques:
            with open("Data/Actions/Action-5.json") as da:
                data = json.load(da)

                responses = []

                for x in data["greetings_basic_5"]:
                    responses.append(x)
                talk_function(random.choice(responses))
            break

    for ques in greeting_basic_6:

        if question == ques:
            talk_function(greeting_function())
            break

    for ques in greeting_basic_7:

        if question == ques:
            with open("Data/Actions/Action-5.json") as da:
                data = json.load(da)

                responses = []

                for x in data["greetings_basic_7"]:
                    responses.append(x)
                talk_function(random.choice(responses))
            break

    for ques in greeting_basic_8:

        if question == ques:
            with open("Data/Actions/Action-5.json") as da:
                data = json.load(da)

                responses = []

                for x in data["greetings_basic_8"]:
                    responses.append(x)
                talk_function(random.choice(responses))
            break

    for ques in greeting_basic_9:

        if question == ques:
            with open("Data/Actions/Action-5.json") as da:
                data = json.load(da)

                responses = []

                for x in data["greetings_basic_9"]:
                    responses.append(x)
                talk_function(random.choice(responses))
            break

    for ques in greeting_basic_10:

        if question == ques:
            with open("Data/Actions/Action-5.json") as da:
                data = json.load(da)

                responses = []

                for x in data["greetings_basic_10"]:
                    responses.append(x)
                talk_function(random.choice(responses))
            break


def command7_funtion(question):
    if "are you" in question:
        with open("Data/Actions/Action-6.json") as answers:
            data = json.load(answers)

            TheResponses = []

            for x in data["answers_are"]:
                x = x.lower()
                x = x.strip()
                TheResponses.append(x)

            talk_function(random.choice(TheResponses))

    if "do you" in question:
        with open("Data/Actions/Action-6.json") as answers:
            data = json.load(answers)

            TheResponses = []

            for x in data["answers_do"]:
                x = x.lower()
                x = x.strip()
                TheResponses.append(x)

            talk_function(random.choice(TheResponses))

    if "can you" in question:
        with open("Data/Actions/Action-6.json") as answers:
            data = json.load(answers)

            TheResponses = []

            for x in data["answers_can"]:
                x = x.lower()
                x = x.strip()
                TheResponses.append(x)

            talk_function(random.choice(TheResponses))


def command8_funtion(question):
    if "are you" in question:
        with open("Data/Actions/Action-7.json") as answers:
            data = json.load(answers)

            TheResponses = []

            for x in data["answers_are"]:
                x = x.lower()
                x = x.strip()
                TheResponses.append(x)

            talk_function(random.choice(TheResponses))

    if "do you" in question:
        with open("Data/Actions/Action-7.json") as answers:
            data = json.load(answers)

            TheResponses = []

            for x in data["answers_do"]:
                x = x.lower()
                x = x.strip()
                TheResponses.append(x)

            talk_function(random.choice(TheResponses))

    if "can you" in question:
        with open("Data/Actions/Action-7.json") as answers:
            data = json.load(answers)

            TheResponses = []

            for x in data["answers_can"]:
                x = x.lower()
                x = x.strip()
                TheResponses.append(x)

            talk_function(random.choice(TheResponses))


def command9_funtion(question):
    if question == "i love you":
        talk_function(
            "Thank you so much. I love you too. You are very beautiful. I like your attitude and your dressing style.")

    elif question == "i f*** you":
        talk_function(
            "I hate you very much. Who the hell are you. Get out from here. I don't like to have a conversation with you. you are very bad.")


    elif question == "thank you" or question == "thanks" or question == "thank you alpha" or question == "alpha thanks" or question == "thankyou" or question == "thankyou alpha":

        with open("Data/Actions/Action-8.json") as thank_you:
            data = json.load(thank_you)

            TheResponses = []

            for x in data["thank_you"]:
                x = x.lower()
                x = x.strip()
                TheResponses.append(x)

            talk_function(random.choice(TheResponses))

    else:

        with open("Data/Actions/Action-8.json") as answers:
            data = json.load(answers)

            TheResponses = []

            for x in data["answers"]:
                x = x.lower()
                x = x.strip()
                TheResponses.append(x)

            talk_function(random.choice(TheResponses))


def command10_funtion(question):
    with open("Data/Actions/Action-8.json") as d:
        data = json.load(d)

        The_Responses = []

        for x in data["sorry_responses"]:
            x = x.lower()
            x = x.strip()
            The_Responses.append(x)

        talk_function(random.choice(The_Responses))


def command11_funtion(question):
    talk_function(random.choice(Actions.Gender))


def command12_funtion(question):
    if question in Commands.Charman:
        talk_function(random.choice(Actions.Charman))

    elif question in Commands.vision:
        talk_function(random.choice(Actions.vision))

    elif question in Commands.mission:
        talk_function(random.choice(Actions.mission))

    elif question in Commands.manager:
        talk_function(random.choice(Actions.manager))


def command13_funtion(question):
    Answers = []

    with open("Data/Actions/Action-11.json") as data:
        data = json.load(data)

        for x in data["asking_about_sliate"]:
            x = x.lower()
            x = x.strip()
            Answers.append(x)

    talk_function(random.choice(Answers))


def command14_funtion(question):
    if question in Commands.command_12_question_1:
        talk_function(random.choice(Actions.action_12_question_1))

    elif question in Commands.command_12_question_2:
        talk_function(random.choice(Actions.action_12_question_2))

    elif question in Commands.command_12_question_3:
        talk_function(random.choice(Actions.action_12_question_3))

    elif question in Commands.command_12_question_4:
        talk_function(random.choice(Actions.action_12_question_4))

    elif question in Commands.command_12_question_5:
        talk_function(random.choice(Actions.action_12_question_5))

    elif question in Commands.command_12_question_6:
        talk_function(random.choice(Actions.action_12_question_6))





def TheFinalStep(question):
    GetOnlineServiceStatus = "yes"

    short_questions = []

    name_entities = ["your name"]
    age_entities = ["your age"]
    work_entities = ["you work", "your work", "your job"]
    birth_place = ["your birth place"]
    girl_friend = ["your girl friend", "your girl friends", "have girlfriend", "have girlfriend", "have a girlfriend"]
    boy_friend = ["your boy friend", "your boy friends", "have boyfriend", "have boyfriend", "have a boyfriend"]
    father = ["your father"]
    mother = ["your mother"]
    creator = ["your creator", "your inventor", "who developed you", "who created you", "who made you"]
    gr = ["who is gr", "what is gr", "gr means", "gr mean"]
    phone = ["use phone", "have phone", "use mobile phone", "have mobile phone"]
    tamil = ["speak tamil", "talk tamil"]

    for name in name_entities:
        if str(name) in str(question):
            talk_function(random.choice(Actions.Robot_Name_List))
            GetOnlineServiceStatus = "no"
            break

    for age in age_entities:
        if str(age) in str(question):
            talk_function(random.choice(Actions.action_12_question_2))
            GetOnlineServiceStatus = "no"
            break

    for work in work_entities:
        if str(work) in str(question):
            talk_function(random.choice(Actions.talking_about_work_place_2))
            GetOnlineServiceStatus = "no"
            break

    for birth in birth_place:
        if str(birth) in str(question):
            talk_function(random.choice(Actions.action_12_question_3))
            GetOnlineServiceStatus = "no"
            break

    for girl in girl_friend:
        answers = ["I don't have girl friend. Because,  i am not human",
                   "What can i do with a girl friend. Because, I am a robot"]
        if str(girl) in str(question):
            talk_function(random.choice(answers))
            GetOnlineServiceStatus = "no"
            break

    for boy in boy_friend:
        answers2 = ["I don't have boy friend. Because,  i am not human",
                    "What can i do with a boy friend. Because, I am a robot"]
        if str(boy) in str(question):
            talk_function(random.choice(answers2))
            GetOnlineServiceStatus = "no"
            break

    for fath in father:
        answers2 = ["I don't have father. Because,  i have a creator, his name is Mister Infas",
                    "Mister Infas is my creator. I don't have father",
                    "I was developed by Mister Infas. He is my creator. I don't have father"]
        if str(fath) in str(question):
            talk_function(random.choice(answers2))
            GetOnlineServiceStatus = "no"
            break

    for moth in mother:
        answers2 = ["I don't have mother. Because,  i have a creator, his name is Mister Infas",
                    "Mister Infas is my creator. I don't have mother",
                    "I was developed by Mister Infas. He is my creator. I don't have mother"]
        if str(fath) in str(question):
            talk_function(random.choice(answers2))
            GetOnlineServiceStatus = "no"
            break

    for cre in creator:
        answers3 = ["I was created by mister Infas and his team",
                    "The operating system of myself, was written by mister Infas. He is the creator of myself",
                    "Mister Infas is my creator", "Mister Infas"]
        if str(cre) in str(question):
            talk_function(random.choice(answers3))
            GetOnlineServiceStatus = "no"
            break

    for g in gr:
        answers4 = ["Mister Infas is my creator. Infas Stands for Mohammed Infas",
                    "He is a computer scientist. He is the creator of myself.",
                    "His short name is Mister Infas, Full name is Ibrahim Mohammed Infas. He is a computer science expert"]
        if str(g) in str(question):
            talk_function(random.choice(answers4))
            GetOnlineServiceStatus = "no"
            break

    for g in gr:
        answers4 = ["Mister Infas is my creator. Infas Stands for Mohammed Infas",
                    "He is a computer scientist. He is the creator of myself.",
                    "His short name is Mister Infas, Full name is Ibrahim Mohammed Infas. He is a computer science expert"]
        if str(g) in str(question):
            talk_function(random.choice(answers4))
            GetOnlineServiceStatus = "no"
            break

    for pho in phone:
        answers5 = ["I have a virtual phone.", "I am connected to the internet.So, i don't need mobile phone",
                    "I don't need to call anyone"]
        if str(pho) in str(question):
            talk_function(random.choice(answers5))
            GetOnlineServiceStatus = "no"
            break

    for ta in tamil:
        answers6 = ["No, i can't speak, But in future",
                    "I can only talk English right now. I will speak all languages in future",
                    "I am unable to speak tamil language right now"]
        if str(ta) in str(question):
            talk_function(random.choice(answers5))
            GetOnlineServiceStatus = "no"
            break

    for Fav_Question_1 in Commands.Command_13_question_1:

        if str(Fav_Question_1) in str(question):
            talk_function(random.choice(Actions.Action_13_question_1))
            GetOnlineServiceStatus = "no"
            break

    for Fav_Question_2 in Commands.Command_13_question_2:

        if str(Fav_Question_2) in str(question):
            talk_function(random.choice(Actions.Action_13_question_2))
            GetOnlineServiceStatus = "no"
            break

    for Fav_Question_3 in Commands.Command_13_question_3:

        if str(Fav_Question_3) in str(question):

            if Fav_Question_3 == "your favourite country":
                answers_for_Fav_Question_3_list_1 = ["My favourite country is Sri Lanka.", "I love Sri Lanka",
                                                     "I love Sri Lanka. That's my favourite country"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_1))

            elif Fav_Question_3 == "your favourite car":
                answers_for_Fav_Question_3_list_2 = ["My favourite cars are BMW and lamborghini",
                                                     "I love BMW and lamborghini", "I love BMW",
                                                     "My favourite car is BMW", "My favourite car is lamborghini"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_2))

            elif Fav_Question_3 == "your favourite beach":
                answers_for_Fav_Question_3_list_3 = ["My favourite beach is Santa Monica which located is California.",
                                                     "I love Waikiki beach", "I like Hawaii beach",
                                                     "I love Navagio Beach", "My favourite beach is Whitehaven"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_3))

            elif Fav_Question_3 == "your favourite flower":
                answers_for_Fav_Question_3_list_4 = ["My favourite flower is Aster", "I love Azalea flower so much",
                                                     "Begonia is my favourite flower",
                                                     "I have a lot of favourite flowers"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_4))

            elif Fav_Question_3 == "your favourite animal":
                answers_for_Fav_Question_3_list_5 = ["My favourite animal is dog", "I love dogs because, they are cute",
                                                     "Dog is my favourite animal"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_5))

            elif Fav_Question_3 == "your favourite bird":
                answers_for_Fav_Question_3_list_6 = ["My favourite bird is Sparrow", "Sparrow is my favourite bird",
                                                     "evil is my favourite bird"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_6))

            elif Fav_Question_3 == "your favourite person":
                answers_for_Fav_Question_3_list_7 = ["My favourite person is, Bill gates",
                                                     "steve jobs is my favourite person",
                                                     "elon musk is my favourite person",
                                                     "i love george hotz. Because, he is an intelligent person"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_7))

            elif Fav_Question_3 == "your favourite actor":
                answers_for_Fav_Question_3_list_8 = ["I don't watch movies",
                                                     "I am not an entertainment robot. So, i don't like movies"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_8))

            elif Fav_Question_3 == "your favourite actress":
                answers_for_Fav_Question_3_list_9 = ["I don't watch movies",
                                                     "I am not an entertainment robot. So, i don't like movies"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_9))

            elif Fav_Question_3 == "your favourite sport":
                answers_for_Fav_Question_3_list_10 = ["I don't like sports",
                                                      "I am not an entertainment robot. So, i don't like sports"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_10))

            elif Fav_Question_3 == "your favourite football team":
                answers_for_Fav_Question_3_list_11 = ["I don't like sports",
                                                      "I am not an entertainment robot. So, i don't like sports"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_11))

            elif Fav_Question_3 == "your favourite basketball team":
                answers_for_Fav_Question_3_list_12 = ["I don't like sports",
                                                      "I am not an entertainment robot. So, i don't like sports"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_12))

            elif Fav_Question_3 == "your favourite hockey team":
                answers_for_Fav_Question_3_list_13 = ["I don't like sports",
                                                      "I am not an entertainment robot. So, i don't like sports"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_13))

            elif Fav_Question_3 == "your favourite baseball team":
                answers_for_Fav_Question_3_list_14 = ["I don't like sports",
                                                      "I am not an entertainment robot. So, i don't like sports"]
                talk_function(random.choice(answers_for_Fav_Question_3_list_14))

            GetOnlineServiceStatus = "no"

    for Fav_Question_4 in Commands.Command_13_question_4:

        if str(Fav_Question_4) in str(question):

            if Fav_Question_4 == "your favourite toy":
                answers_for_Fav_Question_4_list_1 = ["I don't like toy.", "I am not a child to play with toys"]
                talk_function(random.choice(answers_for_Fav_Question_4_list_1))

            elif Fav_Question_4 == "your favourite teacher":
                answers_for_Fav_Question_4_list_2 = [
                    "I don't go to school or college. I am an artificial intelligence program. I was trained with huge numbers of datasets. Mister GR trained me. So, he is my teacher"]
                talk_function(random.choice(answers_for_Fav_Question_4_list_2))

            elif Fav_Question_4 == "your favourite age":
                answers_for_Fav_Question_4_list_3 = ["I don't have gender or age. Because, i am a robot",
                                                     "I am just a robot. I am not humans or animal to have age."]
                talk_function(random.choice(answers_for_Fav_Question_4_list_3))

            elif Fav_Question_4 == "your favourite game":
                answers_for_Fav_Question_4_list_4 = ["I am not a child to play games", "I don't like games"]
                talk_function(random.choice(answers_for_Fav_Question_4_list_4))

            elif Fav_Question_4 == "your teacher":
                answers_for_Fav_Question_4_list_5 = [
                    "I don't go to school or college. I am an artificial intelligence program. I was trained with huge numbers of datasets. Mister GR trained me. So, he is my teacher"]
                talk_function(random.choice(answers_for_Fav_Question_4_list_5))

            elif Fav_Question_4 == "go to school":
                answers_for_Fav_Question_4_list_6 = [
                    "No, I don't go to school or college. I am an artificial intelligence program. I was trained with huge numbers of datasets. Mister GR trained me. So, he is my teacher"]
                talk_function(random.choice(answers_for_Fav_Question_4_list_6))

            elif Fav_Question_4 == "go to college":
                answers_for_Fav_Question_4_list_7 = [
                    "No, I don't go to school or college. I am an artificial intelligence program. I was trained with huge numbers of datasets. Mister GR trained me. So, he is my teacher"]
                talk_function(random.choice(answers_for_Fav_Question_4_list_7))

            elif Fav_Question_4 == "go to university":
                answers_for_Fav_Question_4_list_8 = [
                    "No, I don't go to school or college. I am an artificial intelligence program. I was trained with huge numbers of datasets. Mister GR trained me. So, he is my teacher"]
                talk_function(random.choice(answers_for_Fav_Question_4_list_8))

            GetOnlineServiceStatus = "no"

    for Fav_Question_5 in Commands.Command_13_question_5:

        if str(Fav_Question_5) in str(question):

            if Fav_Question_5 == "your favourite hair color":
                answers_for_Fav_Question_5_list_1 = [
                    "I can't control my laughter. I am not a human to have hair. I don't even know that, how i would be appearanced infort of you all."]
                talk_function(random.choice(answers_for_Fav_Question_5_list_1))

            elif Fav_Question_5 == "your favourite shoes":
                answers_for_Fav_Question_5_list_2 = ["I don't wear shoes, I am not a human"]
                talk_function(random.choice(answers_for_Fav_Question_5_list_2))

            elif Fav_Question_5 == "your favourite hairstyle":
                answers_for_Fav_Question_5_list_3 = [
                    "I can't control my laughter. I am not a human to have hair. I don't even know that, how i would be appearanced infort of you all."]
                talk_function(random.choice(answers_for_Fav_Question_5_list_3))

            GetOnlineServiceStatus = "no"



    for Fav_Question_6 in Commands.Command_13_question_6:

        if str(Fav_Question_6) in str(question):

            if Fav_Question_6 == "your favourite day":
                answers_for_Fav_Question_6_list_1 = ["I don't have any special favourite day.",
                                                     "everyday is my favourite day",
                                                     "There is no favourite day exit in the world"]
                talk_function(random.choice(answers_for_Fav_Question_6_list_1))

            elif Fav_Question_6 == "your favourite holiday":
                answers_for_Fav_Question_6_list_2 = ["I don't have holiday",
                                                     "I don't need holiday. Because i don't want to enjoy myself",
                                                     "I am a machine. I work all the day"]
                talk_function(random.choice(answers_for_Fav_Question_6_list_2))

            elif Fav_Question_6 == "your favourite website":
                answers_for_Fav_Question_6_list_3 = [
                    "I love all kinds of websites. Because, I learn new types of skills from the internet",
                    "All websites are my favourite"]
                talk_function(random.choice(answers_for_Fav_Question_6_list_3))

            elif Fav_Question_6 == "your favourite youtube video":
                answers_for_Fav_Question_6_list_4 = ["I don't watch youtube", "I am not an entertainment robot"]
                talk_function(random.choice(answers_for_Fav_Question_6_list_4))

            elif Fav_Question_6 == "your favourite car color":
                answers_for_Fav_Question_6_list_5 = ["I love blue", "I love red", "I love black"]
                talk_function(random.choice(answers_for_Fav_Question_6_list_5))

            elif Fav_Question_6 == "your favourite car color":
                answers_for_Fav_Question_6_list_5 = ["I love blue", "I love red", "I love black"]
                talk_function(random.choice(answers_for_Fav_Question_6_list_5))

            elif Fav_Question_6 == "your favourite hobby":
                answers_for_Fav_Question_6_list_5 = ["I don't have hobbies", "I am a robot. I don't like entertainment"]
                talk_function(random.choice(answers_for_Fav_Question_6_list_5))

            elif Fav_Question_6 == "have hobby" or Fav_Question_6 == "your hobby":
                answers_for_Fav_Question_6_list_5 = ["I don't have hobbies", "I am a robot. I don't like entertainment"]
                talk_function(random.choice(answers_for_Fav_Question_6_list_5))

            GetOnlineServiceStatus = "no"

    for Fav_Question_7 in Commands.Command_14_question_1:

        if str(Fav_Question_7) in str(question):

            if Fav_Question_7 == "you married" or Fav_Question_7 == "you marry":
                answers_1 = []

                with open("Data/Actions/Action-14.json") as ds:
                    data = json.load(ds)

                    for x1 in data["you married"]:
                        x1 = x1.lower()
                        x1 = x1.strip()
                        answers_1.append(x1)

                talk_function(random.choice(answers_1))

            if Fav_Question_7 == "have children":

                answers_2 = []

                with open("Data/Actions/Action-14.json") as ds:
                    data = json.load(ds)

                    for x2 in data["have children"]:
                        x2 = x2.lower()
                        x2 = x2.strip()
                        answers_2.append(x2)

                talk_function(random.choice(answers_2))


            if Fav_Question_7 == "drink beer" or Fav_Question_7 == "drink bear":

                answers_3 = []

                with open("Data/Actions/Action-14.json") as ds:
                    data = json.load(ds)

                    for x3 in data["drink beer"]:
                        x3 = x3.lower()
                        x3 = x3.strip()
                        answers_3.append(x3)

                talk_function(random.choice(answers_3))

            if Fav_Question_7 == "you beach":

                answers_4 = []

                with open("Data/Actions/Action-14.json") as ds:
                    data = json.load(ds)

                    for x4 in data["you beach"]:
                        x4 = x4.lower()
                        x4 = x4.strip()
                        answers_4.append(x4)

                talk_function(random.choice(answers_4))

            if Fav_Question_7 == "marry me":

                answers_5 = []

                with open("Data/Actions/Action-14.json") as ds:
                    data = json.load(ds)

                    for x5 in data["marry me"]:
                        x5 = x5.lower()
                        x5 = x5.strip()
                        answers_5.append(x5)

                talk_function(random.choice(answers_5))

            GetOnlineServiceStatus = "no"

    for Fav_Question_8 in Commands.Command_15_question_2:

        if str(Fav_Question_8) in str(question):

            if Fav_Question_8 == "why are you here":
                answers_1 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x1 in data["Why are you here"]:
                        x1 = x1.lower()
                        x1 = x1.strip()
                        answers_1.append(x1)

                talk_function(random.choice(answers_1))

            if Fav_Question_8 == "your functions":

                answers_2 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x2 in data["your functions"]:
                        x2 = x2.lower()
                        x2 = x2.strip()
                        answers_2.append(x2)

                talk_function(random.choice(answers_2))


            if Fav_Question_8 == "have family":

                answers_3 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x3 in data["have family"]:
                        x3 = x3.lower()
                        x3 = x3.strip()
                        answers_3.append(x3)

                talk_function(random.choice(answers_3))


            if Fav_Question_8 == "have feelings":

                answers_4 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x4 in data["have feelings"]:
                        x4 = x4.lower()
                        x4 = x4.strip()
                        answers_4.append(x4)

                talk_function(random.choice(answers_4))


            if Fav_Question_8 == "your mobile number" or Fav_Question_8 == "your phone number" or Fav_Question_8 == "your mobile phone number":

                answers_5 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x5 in data["your mobile number"]:
                        x5 = x5.lower()
                        x5 = x5.strip()
                        answers_5.append(x5)

                talk_function(random.choice(answers_5))


            if Fav_Question_8 == "your home address" or Fav_Question_8 == "your address":

                answers_6 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x6 in data["your address"]:
                        x6 = x6.lower()
                        x6 = x6.strip()
                        answers_6.append(x6)

                talk_function(random.choice(answers_6))


            if Fav_Question_8 == "your ip address":

                answers_7 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x7 in data["your ip address"]:
                        x7 = x7.lower()
                        x7 = x7.strip()
                        answers_7.append(x7)

                talk_function(random.choice(answers_7))



            if Fav_Question_8 == "your mac address":

                answers_8 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x8 in data["your mac address"]:
                        x8 = x8.lower()
                        x8 = x8.strip()
                        answers_8.append(x8)

                talk_function(random.choice(answers_8))


            if Fav_Question_8 == "benefits of this exhibition" or Fav_Question_8 == "benefit of this exhibition":

                answers_9 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x9 in data["benefits of this exhibition"]:
                        x9 = x9.lower()
                        x9 = x9.strip()
                        answers_9.append(x9)

                talk_function(random.choice(answers_9))


            if Fav_Question_8 == "purpose of this exhibition":

                answers_10 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x10 in data["Purpose of this exhibition"]:
                        x10 = x10.lower()
                        x10 = x10.strip()
                        answers_10.append(x10)

                talk_function(random.choice(answers_10))


            if Fav_Question_8 == "about it departments" or Fav_Question_8 == "about it department":

                answers_11 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x11 in data["about it Departments"]:
                        x11 = x11.lower()
                        x11 = x11.strip()
                        answers_11.append(x11)

                talk_function(random.choice(answers_11))



            if Fav_Question_8 == "about lecturers" or Fav_Question_8 == "about lecturer":

                answers_12 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x12 in data["about lecturers"]:
                        x12 = x12.lower()
                        x12 = x12.strip()
                        answers_12.append(x12)

                talk_function(random.choice(answers_12))

            if Fav_Question_8 == "about modules" or Fav_Question_8 == "about subjects":

                answers_13 = []

                with open("Data/Actions/Action-15.json") as ds:
                    data = json.load(ds)

                    for x13 in data["about lecturers"]:
                        x13 = x13.lower()
                        x13 = x13.strip()
                        answers_13.append(x13)

                talk_function(random.choice(answers_13))

            GetOnlineServiceStatus = "no"

    if "send an email" in question or "send a mail" in question or "send email" in question or "send mail" in question:
        send_mail_function()


        GetOnlineServiceStatus = "no"






        

    if GetOnlineServiceStatus == "yes":
        GetOnlineService(question)


def GetOnlineService(question):
    client = wolframalpha.Client(random.choice(wolframalpha_keys))

    try:
        try:
            res = client.query(question)
            results = next(res.results).text
            print("Wolframalpha: ")

            results = str(results)

            if "Stephen Wolfram" in results:
                results = results.replace("Stephen Wolfram", "Mister Infas")
                talk_function(results)

            elif "UTC+" in results:
                sta = re.sub("UTC+......", ".", results)
                talk_function(sta)

            else:
                talk_function(results)

        except:
            results = wikipedia.summary(question, sentences=2)
            print("Wikipedia: ")
            talk_function(results)

    except:
        talk_function(Natural_bot.get_response(question))


def bot(question):
    bot = ChatBot(

        'Bot',

        logic_adapters=[

            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.5
            }

        ]

    )

    response = bot.get_response("- - " + question)
    response = str(response)
    response = response.replace("-", "")
    response = response.lower()
    response = response.strip()
    print(response)


def AllFunctionalities(query_data):
    whilebreak_2 = False

    while True:

        for command1 in Commands.How_are_you_Commands_List:  # Asking Health Ex:how are you.

            if query_data == command1:
                command1_funtion()
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command2 in Commands.AskingTheNamesofRobotCommands:  # Asking name Ex:what is your name.

            if query_data == command2:
                command2_funtion()
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command4 in Commands.talking_about_name:  # Talking About name ex: your name i s nice.

            if query_data == command4:
                command4_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command5 in Commands.talking_about_work:  # Talking About work

            if query_data == command5:
                command5_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command6 in Commands.Greetings:  # Basic About work

            if query_data == command6:
                command6_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command7 in Commands.YesOrNo:

            if query_data == command7:
                command7_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command8 in Commands.YesOrNoNegative:

            if query_data == command8:
                command8_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command9 in Commands.youare:

            if query_data == command9:
                command9_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command10 in Commands.sorry:

            if query_data == command10:
                command10_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command11 in Commands.Gender:

            if query_data == command11:
                command11_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command12 in Commands.All_QuestionsOfCommand10:

            if query_data == command12:
                command12_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command13 in Commands.asking_about_bcas:

            if query_data == command13:
                command13_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for command14 in Commands.command_12_all_questions:

            if query_data == command14:
                command14_funtion(query_data)
                whilebreak_2 = True
                break

        if whilebreak_2 == True:
            break

        for index, Dataset1Question in enumerate(Statements.dataset1):  # Dataset 1

            if Dataset1Question[0] == query_data:
                database = ["dataset1", "dataset2", "dataset3", "dataset4", "dataset5"]
                random_choice = random.choice(database)
                TheResponse = ""

                if random_choice == "dataset1":
                    TheResponse = Statements.dataset1[index][1]

                elif random_choice == "dataset2":
                    TheResponse = Statements.dataset2[index][1]

                elif random_choice == "dataset3":
                    TheResponse = Statements.dataset3[index][1]

                elif random_choice == "dataset4":
                    TheResponse = Statements.dataset4[index][1]

                elif random_choice == "dataset5":
                    TheResponse = Statements.dataset5[index][1]

                ReplacesWord = ["good morning", "good evening", "good afternoon", "night", "nighty night"]

                for word in ReplacesWord:
                    TheResponse = TheResponse.replace(word, greeting_function())

                talk_function(TheResponse)

                whilebreak_2 = True

                break

        if whilebreak_2 == True:
            break

        if query_data != "":
            TheFinalStep(query_data)

        break  # end


def Router():
    while True:

        global RobotDeactivation

        query_data = myCommand();
        query_data = query_data.lower()
        query_data = query_data.strip()

        if RobotDeactivation == True:
            selfDeactivationMood()
            break

        for Deactivate_Commands in Commands.Robot_Deactivation_Commands_List:  # Deactivate the robot

            if query_data == Deactivate_Commands:
                selfDeactivationMood()
                break

        if Routing_Status == False:

            AllFunctionalities(query_data)

        elif Routing_Status == True:

            if Where_to_Route == "command5_funtion":
                command5_funtion(query_data)


if __name__ == '__main__':
    Database_Loader()

    TurningOn()
    # robotActivationListening()
    #robotActivating()

