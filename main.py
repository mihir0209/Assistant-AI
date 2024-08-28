import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import google.generativeai as genai
from pytube import Search
import sys
# import re
import subprocess
import os
from dotenv import load_dotenv
recognizer = sr.Recognizer()
engine = pyttsx3.init()
GEMINI_api_key = os.getenv('API_KEY')
news_api_key = os.getenv("NEWS_API_KEY")
news_url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}"

genai.configure(api_key=GEMINI_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_first_video_id(search_query):
    search = Search(search_query)
    
    if search.results:
        first_video = search.results[0]
        return first_video.video_id
    else:
        return None

def process_command(command):
    command_lower = command.lower()
    
    # if "open" in command_lower:
    #     if "open google" in command_lower:
    #         webbrowser.open("https://www.google.com")
    #     elif "open youtube" in command_lower:
    #         webbrowser.open("https://www.youtube.com")
    #     elif "open facebook" in command_lower:
    #         webbrowser.open("https://www.facebook.com")
    #     elif "open linkedin" in command_lower:
    #         webbrowser.open("https://www.linkedin.com")
    if "stop" in command_lower:
        speak("Thank you for using assistant, the program will end here.")
        print("Thank you!!")
        sys.exit()
        
        
    if "search"  in command_lower:
        search_query="+".join(command_lower.split(" ")[1:])
        google_search_query=f"https://www.google.com/search?q={search_query}"
        print(f"Opening browser for the search: {command.split(" ")[1:]}")
        webbrowser.open(google_search_query)
        
        
    elif command_lower.startswith("play"):
        # pattern = r"at time\s+(\d+)\s+minutes"
        # match = re.search(pattern, command_lower)
        search_query = " ".join(command_lower.split(" ")[1:])
        # if match:
        #     search_query = " ".join(command_lower.split("at time")[0].strip())
        video_id = get_first_video_id(search_query)
        #C:\Program Files\BraveSoftware\Brave-Browser\Application
        path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        url= f"https://www.youtube.com/watch?v={video_id}"
        
        
        # if match:
        #     minutes = int(match.group(1))
        #     seconds = minutes*60+int(match.group(2)) if match.group(2) else 0
        #     url=f"https://www.youtube.com/watch?v={video_id}?t={seconds}"
        
        subprocess.run([path,url])
        
        #youtube_search_url = f"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe https://www.youtube.com/watch?v={video_id}"
        print(f"Playing {search_query}")
        # webbrowser.open(youtube_search_url)
        
        
    elif "news" in command_lower:
        try:
            r = requests.get(news_url)
            r.raise_for_status() 
            data = r.json()
            articles = data.get('articles', [])
            
            if articles:
                # print("Say 'Stop' to stop the assistant")
                print("Top Headlines in India:")
                speak("Top Headlines in India:")
                
                for article in articles:
                    print(article.get('title', 'No title available'))
                    speak(article.get('title', 'No title available'))
                    # with sr.Microphone() as source:
                    #     audio = recognizer.listen(source)
                    #     word = recognizer.recognize_google(audio)
                    #     if 'stop' in word.lower():
                    #         break   
            else:
                speak("No articles found.")
        except requests.RequestException as e:
            speak(f"Failed to retrieve data: {e}")  
    else:
        # Let Gemini AI handle the request
        try:
            response = model.generate_content(command)
            text_response = response.text
            speak(text_response)
            
        except Exception as e:
            speak(f"Error generating response: {e}")
if __name__ == '__main__':
    speak("How can I help you today?")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=1)
            
            word = recognizer.recognize_google(audio)
            
            if word.lower() == 'assistant':
                speak("Yes?")
                
                with sr.Microphone() as source:
                    print("Assistant is active now...")
                    audio = recognizer.listen(source,timeout=7, phrase_time_limit=5)
                
                command = recognizer.recognize_google(audio)
                process_command(command)
        except Exception as e:
            print(f"Error: {e}")
        else:
            print("The recognition was done and the output was shown successfully")
        
'''

    (\/)
   ( O.O)
    ) ==>❤️ Here, take this!❤️
   (_)(_)
   
'''