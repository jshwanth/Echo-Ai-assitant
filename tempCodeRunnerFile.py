import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Initializing REX...")

    while True:
        # Obtain audio from microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, timeout=2)


        print("Recognizing...")
        # recognize speech using google
        try:
            command = r.recognize_google_cloud(audio)
            print(command)
        except Exception as e:
            print("Error;{0}".format(e))