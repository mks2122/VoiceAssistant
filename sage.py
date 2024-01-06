import g4f
import speech_recognition as sr
import time
import pyttsx3

g4f.debug.logging = False  # Enable debug logging
g4f.debug.check_version = False  # Disable automatic version checking

r = sr.Recognizer()
source = sr.Microphone(0)
engine = pyttsx3.init()

def speak(text):
    text = text[0:text.find("Some possible follow-up messages")]
    text = text.replace("Bing", "Sage")
    engine.say(text)
    engine.runAndWait()

def bing(query):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": query}],
    )
    print(response, flush=True, end='')
    speak(response)

speak("Hello! How can I help you?")
while True:

    try:
            with source as s:
                r.adjust_for_ambient_noise(s,duration=1)
                print('Listening')
                audio=r.listen(s)
                query=r.recognize_google(audio)
                print(f"\nUser said: {query}")
                bing(query)
                
    except sr.UnknownValueError:
        source = sr.Microphone(0)
        r = sr.Recognizer()
    except KeyboardInterrupt:
        speak("Goodbye!")
        break



