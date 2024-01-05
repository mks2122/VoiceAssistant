import g4f
import speech_recognition as sr
import time
import pyttsx3

g4f.debug.logging = False  # Enable debug logging
g4f.debug.check_version = False  # Disable automatic version checking

r = sr.Recognizer()
source = sr.Microphone()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def callback(recognizer, audio):
    try:
        query = r.recognize_google(audio)
        print(f"\nUser said: {query}")
        response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": query}],
        )
        print(response, flush=True, end='')
        speak(response)
        return query.lower()
    except sr.UnknownValueError:
        pass
    except Exception as e:
       print("Prompt error: ", e)

def start_listening():
    with source as s:
        r.adjust_for_ambient_noise(s, duration=2)
    print('Listening\n')
    speak("Hello! How can I help you?")
    stop_listening = r.listen_in_background(source, callback)
    while True:
        time.sleep(0.5)

start_listening()
