import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import pyjokes
import pyautogui
import time
import requests
import math
import operator
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Text to speech
def say(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Voice to text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        say("Say that again, please...")
        return "none"
    return query

# Greet the user
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        say("Good morning!")
    elif hour > 12 and hour <= 16:
        say("Good afternoon!")
    else:
        say("Good evening!")
    say("I am Nova, your AI assistant. How can I help you?")

# Fetch latest news
def news():
    main_url = 'https://newsapi.org/v2/top-headlines?sources=the-times-of-india,india-today&apiKey=c6af72bc615e4b22b8634823b1c7801d'
    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]

    for ar in articles:
        head.append(ar["title"])

    for i in range(len(day)):
        if i < len(head):
            say(f"Today's {day[i]} news is: {head[i]}")
        else:
            break

# Fetch Nifty Fifty price
def get_nifty_fifty_price():
    url = "https://www.moneycontrol.com/indian-indices/nifty-50-9.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        price_element = soup.find('span', attrs={'id': 'inp_nse'})
        change_element = soup.find('span', attrs={'id': 'sp_val'})
        if price_element and change_element:
            price = price_element.text.strip()
            change = change_element.text.strip()
            say(f"The current Nifty Fifty price is {price} and the change is {change}")
        else:
            say("Unable to fetch Nifty Fifty price at the moment.")
    except Exception as e:
        say("Sorry, I couldn't fetch Nifty Fifty price.")
        print(e)

# Fetch stock price
def get_stock_price(stock_name):
    try:
        search_url = f"https://www.google.com/search?q={stock_name}+share+price"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find('div', class_='BNeawe iBp4i AP7Wnd')
        if price_element:
            price = price_element.text.strip()
            say(f"The current price of {stock_name} stock is {price}")
        else:
            say("Unable to fetch the stock price. Please try again later.")
    except Exception as e:
        say("Sorry, I couldn't fetch the stock price.")
        print(e)

# Helper Functions for Calculation
def get_operator_fn(op):
    """Map operators to their respective functions."""
    return {
        '+': operator.add,
        'add': operator.add,
        '-': operator.sub,
        'subtract': operator.sub,
        'x': operator.mul,
        'multiply': operator.mul,
        '/': operator.truediv,
        'divided': operator.truediv,
        'mod': operator.mod,
        'remainder': operator.mod,
        '**': operator.pow,
        'power': operator.pow,
    }.get(op, None)

def eval_binary_expr(op1, oper, op2):
    """Evaluate binary expressions like '3 + 4'."""
    try:
        op1, op2 = float(op1), float(op2)
        operation = get_operator_fn(oper)
        if operation:
            return operation(op1, op2)
        else:
            raise ValueError(f"Unknown operator: {oper}")
    except Exception as e:
        return f"Error in calculation: {e}"

# Main Program
if __name__ == "__main__":
    wish()
    while True:
        query = takecommand().lower()

        # Self-introduction
        if "describe yourself" in query:
            say("Hi, I’m Nova, your AI assistant always ready to help you.")

        # Open applications
        elif "open notepad" in query:
            npath = r"C:\\Windows\\notepad.exe"
            os.startfile(npath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")

        elif "open google" in query:
            say("What should I search on Google?")
            cm = takecommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={cm}")

        # Fetch IP address
        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            say(f"Your IP address is {ip}")

        # Wikipedia search
        elif "wikipedia" in query:
            say("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            say("According to Wikipedia")
            say(results)

        # Joke
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            say(joke)

        # News
        elif "tell me news" in query:
            say("Fetching the latest news...")
            news()

        # Location using IP
        elif "where i am" in query or "where we are" in query:
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data.get('city', 'unknown city')
                state = geo_data.get('region', 'unknown state')
                country = geo_data.get('country', 'unknown country')
                say(f"We are in {city} city of {state} state in {country}.")
            except Exception as e:
                say("Unable to determine location.")

        # Screenshot
        elif "take screenshot" in query:
            say("What should I name the file?")
            name = takecommand().lower()
            say("Taking screenshot...")
            time.sleep(2)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            say(f"Screenshot saved as {name}.png.")

        # Stock prices
        elif "stock price" in query:
            if "nifty 50" in query or "nifty fifty" in query:
                get_nifty_fifty_price()
            else:
                say("Which stock's price would you like to know?")
                stock_name = takecommand().lower()
                get_stock_price(stock_name)

        # Calculations
        elif "do some calculations" in query or "can you calculate" in query:
            say("What would you like to calculate?")
            calculation = takecommand().lower()
           
