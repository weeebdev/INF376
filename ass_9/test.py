import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from tensorflow.keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
import re
import spacy
import requests
from time import sleep
import pandas as pd
data = pd.read_csv("timetable.csv")

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))
def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.7
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": r[1]})
    return return_list

def getCourseCode(msg):
    x = re.search(r"\b(CSS|INF|MDE|TFL) \b...", msg, re.IGNORECASE)
    if (x is None): return None
    return x.group().upper()

courses = data["courseName"].values
instructors = data["instructor"].values
timetable = data["timetable"].values

def getInstructor(msg):
    for i in instructors:
        for j in i.split(" "):
            x = re.search(j, msg, re.IGNORECASE)
            if (x is not None):
                return i
    return None

def getCourseName(msg):
    for i in courses:
        x = re.search(i, msg, re.IGNORECASE)
        if (x is not None):
            return x.group()
    return None

nlp = spacy.load("en_core_web_sm")

def getAllFromWeekday(weekday):
    res = []
    for time in timetable:
        t = time.lower()
        if (weekday.lower() in t):
            res.append(time)
    return res

def getAllFromTime(time):
    res = []
    for time in timetable:
        t = time.lower()
        if (time.lower() in t):
            res.append(time)
    return res

def getAllFromTimetable(weekday, time):
    res = []
    for time in timetable:
        t = time.lower()
        if (weekday.lower() in t and time.lower() in t):
            res.append(time)
    return res

def getTimetable(msg):
    ents = nlp(msg).ents
    weekday = ''
    time = ''
    for ent in ents:
        if (ent.label_ == 'DATE'):
            weekday = ent.text
        elif (ent.label_ == 'TIME'):
            time = ent.text
    if (len(weekday) > 0 and len(time) == 0):
        return getAllFromWeekday(weekday)
    elif (len(weekday) == 0 and len(time) > 0):
        return getAllFromTime(time)
    else:
        return getAllFromTimetable(weekday, time)



def getResponse(msg, ints: list, intents_json):
    error = "Sorry, I don't understand"
    if (len(ints) == 0): return error
    tag = ints[0]['intent']
    print(ints)
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            if (tag == "time-course"):
                course_code = getCourseCode(msg)
                if (course_code == None):
                    course_name = getCourseName(msg)
                    if (course_name == None):
                        result = "Cannot find the course"
                        break
                    course = data[data['courseName'].apply(lambda v: v.lower() == course_name.lower())]
                    if (course.size < 1): return "Couldn't find the course " + course_name
                    result = result.replace("|", course["timetable"].values[0])

                else:
                    course = data[data.code == course_code]
                    if (course.size < 1): return "Couldn't find the course " + course_code
                    result = result.replace("|", course["timetable"].values[0])
            
            elif (tag == "course-instructor"):
                course_code = getCourseCode(msg)
                if (course_code == None):
                    course_name = getCourseName(msg)
                    if (course_name == None):
                        result = "Cannot find the instructor"
                        break
                    course = data[data['courseName'].apply(lambda v: v.lower() == course_name.lower())]
                    if (course.size < 1): return "Couldn't find the instructor " + course_name
                    result = result.replace("|", course["instructor"].values[0])

                else:
                    course = data[data.code == course_code]
                    if (course.size < 1): return "Couldn't find the course " + course_code
                    result = result.replace("|", course["instuctor"].values[0])

            elif (tag == "instructor-time"):
                instructor = getInstructor(msg)
                if (instructor == None):
                    result = "Cannot find the instructor"
                    break
                else:
                    course = data[data['instructor'].apply(lambda v: v.lower() == instructor.lower())]
                    if (course.size < 1): return "Couldn't find the instructor " + instructor
                    result = result.replace("|", course["timetable"].values[0])

            elif (tag == "time-course-info"):
                timetable = set(getTimetable(msg))
                if (len(timetable) == 0):
                    result = "Cannot find the datetime"
                    break
                else:
                    course = data[data['timetable'].apply(lambda v: v in timetable)]
                    if (course.size < 1): return "Couldn't find the datetime for " + timetable[0]
                    course = course.values
                    res = ''
                    for i in course:
                        res+="On -> " + ', '.join([str(j) for j in i]) + '\n'
                    result = result.replace("|", res)
            
    return result

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update

TELEGRAM_TOKEN = '1592904673:AAEwgwq6Hi-xqZEJLW9G-OVMaM55u7znhw0'

greet_bot = BotHandler(TELEGRAM_TOKEN)

upd_id_prev = ''

while(True):
    upd = greet_bot.get_last_update()
    msg, upd_id, chat_id = upd['message']['text'], upd['update_id'], upd['message']['chat']['id']
    if (upd_id_prev!=upd_id):
        upd_id_prev = upd_id
        ints = predict_class(msg) 
        res = getResponse(msg, ints, intents) 
        greet_bot.send_message(chat_id,res)
    sleep(3)