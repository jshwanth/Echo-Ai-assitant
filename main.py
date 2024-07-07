import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musicLibrary  
from openai import OpenAI

API_KEY = '{Api_key}'

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(api_key= "sk-proj-ZmKUnFJyjAMfHr9cCzcfT3BlbkFJrzNAwqDWkHfG87Ma0PIM",
    )
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = [
        {"role":"system","content":"you are a virtual assitant named echo skilled in general tasks like alexa and google cloud"},
        {"role":"user","content":command}
    ])
    return completion.choices[0].messages.content

def get_news():
    url = f"http://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    headlines = [article['title'] for article in news_data['articles'][:5]]  # Get top 5 headlines
    return headlines

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open hotstar" in c.lower():
        webbrowser.open("https://hotstar.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}")
    elif "news" in c.lower():
        headlines = get_news()
        speak("Here are the top news headlines:")
        for i, headline in enumerate(headlines, 1):
            speak(f"Headline {i}: {headline}")

    else:
        # let openai handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Echo...")

    while True:
        try:
            # Obtain audio from microphone
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(source)
            print("Recognizing wake word...")
            word = r.recognize_google(audio).lower()
            print(f"Wake word detected: {word}")

            if word == "hello":
                speak("Yes, I'm listening")

                # listen for command
                with sr.Microphone() as source:
                    print("Echo active, listening for command...")
                    audio = r.listen(source)
                print("Recognizing command...")
                command = r.recognize_google(audio).lower()
                print(f"Command recognized: {command}")

                processCommand(command)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
