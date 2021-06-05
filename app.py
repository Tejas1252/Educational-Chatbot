from flask import Flask, render_template, request, url_for, redirect
import random
import json
import torch
import os
import webbrowser
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import smtplib

r = sr.Recognizer()

# name="Tejas Shinde"
dict = {}

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    sentence = request.args.get('msg')
    temp = sentence
    if (sentence == "exit"):
        feed()
        SPEAK("Please fill the feedback form")
        return redirect("index.html")
    else:
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    rr = random.choice(intent['responses'])
                    # SPEAK(rr)
                    return rr
        else:
            if temp in dict:
                count = dict[temp]
                dict.update({temp: count + 1})
            else:
                dict[temp] = 1
            if dict[temp] == 4:
                sender="gthawal75@gmail.com"
                receiver="hoganhulk159@gmail.com"
                password="@Gaurav75"
                message=temp
                server=smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(sender,password)
                print("Login success!!")
                server.sendmail(sender,receiver,message)
                print("Emiail sent!!")
            # SPEAK("I do not understand")
            return "I do not understand..."

@app.route("/get2")
def get_bot_response2():
    with sr.Microphone() as source:
        try:
            print("Say...")
            audio = r.listen(source)
            tex = r.recognize_google(audio)
            sentence = tokenize(tex)
            X = bag_of_words(sentence, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)
            _, predicted = torch.max(output, dim=1)

            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            if prob.item() > 0.75:
                for intent in intents['intents']:
                    if tag == intent["tag"]:
                        rr = random.choice(intent['responses'])
                        print(rr)
                        return rr
        except:
            pass
    return "Too much sound in background"

def feed():
    webbrowser.open("feedback.html", new=2)


@app.route('/Feedback')
def Feedback():
    feed()
    return render_template("index.html")


@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    print("printed")


def SPEAK(value):
    value = value.replace("</br>", "")
    speech = gTTS(text=value, lang='en', slow=False)
    speech.save("text.mp3")
    playsound("text.mp3")
    os.remove("text.mp3")


if __name__ == "__main__":
    app.run()
