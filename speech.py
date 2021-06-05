import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

r=sr.Recognizer()
with sr.Microphone() as source:
    print("Say...")
    audio=r.listen(source)
    try:
        tex=r.recognize_google(audio)
        print("You: {}".format(tex))
        speech = gTTS(text=tex, lang='en', slow=True)
        speech.save("text.mp3")
        playsound("text.mp3")
    except:
        speech = gTTS(text="Too much sound in background", lang='en', slow=True)
        speech.save("text.mp3")
        playsound("text.mp3")
