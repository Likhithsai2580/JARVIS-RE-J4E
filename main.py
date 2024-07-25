# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: main.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)
import os
import json
import threading
import asyncio
import base64
from time import sleep
from random import choice
import pyautogui
import mtranslate as mt
import eel
from dotenv import load_dotenv, set_key
from threading import Lock

# Import backend modules (assuming they are implemented correctly)
from Backend.Extra import AnswerModifier, QueryModifier, LoadMessages, GuiMessagesConverter
from Backend.Automation import Automation, professional_responses
from Backend.RSE import RealTimeChatBotAI
from Backend.Chatbot import ChatBotAI
from Backend.AutoModel import Model
from Backend.ChatGpt import ChatBotAI as ChatGptAI
from Backend.TTS import TTS

#Lock set by kaushik
import Backend.Security
#remove this to unlock

# Load environment variables
load_dotenv()
state = 'Available...'
messages = LoadMessages()
WEBCAM = False
js_messageslist = []
working: list[threading.Thread] = []
InputLanguage = os.environ['InputLanguage']
Assistantname = os.environ['AssistantName']
Username = os.environ['NickName']
lock = Lock()

def UniversalTranslator(Text: str) -> str:
    """Translates text to English."""
    english_translation = mt.translate(Text, 'en', 'auto')
    return english_translation.capitalize()

def MainExecution(Query: str):
    """Main execution function for handling user queries."""
    global WEBCAM, state
    Query = UniversalTranslator(Query) if 'en' not in InputLanguage.lower() else Query.capitalize()
    Query = QueryModifier(Query)

    if state != 'Available...':
        return
    state = 'Thinking...'
    Decision = Model(Query)

    if 'general' in Decision or 'realtime' in Decision:
        if Decision[0] == 'general':
            if WEBCAM:
                python_call_to_capture()
                sleep(0.5)
                Answer = ChatGptAI(Query)
            else:
                Answer = AnswerModifier(ChatBotAI(Query))
            state = 'Answering...'
            TTS(Answer)
        else:
            state = 'Searching...'
            Answer = AnswerModifier(RealTimeChatBotAI(Query))
            state = 'Answering...'
            TTS(Answer)
    elif 'open webcam' in Decision:
        python_call_to_start_video()
        print('Video Started')
        WEBCAM = True
    elif 'close webcam' in Decision:
        print('Video Stopped')
        python_call_to_stop_video()
        WEBCAM = False
    else:
        state = 'Automation...'
        asyncio.run(Automation(Decision, print))
        response = choice(professional_responses)
        state = 'Answering...'
        with open('ChatLog.json', 'w') as f:
            json.dump(messages + [{'role': 'assistant', 'content': response}], f, indent=4)
        TTS(response)
    state = 'Listening...'

@eel.expose
def js_messages():
    """Fetches new messages to update the GUI."""
    global messages, js_messageslist
    with lock:
        messages = LoadMessages()
    if js_messageslist != messages:
        new_messages = GuiMessagesConverter(messages[len(js_messageslist):])
        js_messageslist = messages
        return new_messages
    return []

@eel.expose
def js_state(stat=None):
    """Updates or retrieves the current state."""
    global state
    if stat:
        state = stat
    return state

@eel.expose
def js_mic(transcription):
    """Handles microphone input."""
    print(transcription)
    if not working:
        work = threading.Thread(target=MainExecution, args=(transcription,), daemon=True)
        work.start()
        working.append(work)
    else:
        if working[0].is_alive():
            return
        working.pop()
        work = threading.Thread(target=MainExecution, args=(transcription,), daemon=True)
        work.start()
        working.append(work)

@eel.expose
def python_call_to_start_video():
    """Starts the video capture."""
    eel.startVideo()

@eel.expose
def python_call_to_stop_video():
    """Stops the video capture."""
    eel.stopVideo()

@eel.expose
def python_call_to_capture():
    """Captures an image from the video."""
    eel.capture()

@eel.expose
def js_page(cpage=None):
    """Navigates to the specified page."""
    if cpage == 'home':
        eel.openHome()
    elif cpage == 'settings':
        eel.openSettings()

@eel.expose
def js_setvalues(GeminiApi, HuggingFaceApi, GroqApi, AssistantName, Username):
    """Sets API keys and user preferences."""
    print(f'GeminiApi = {GeminiApi!r} HuggingFaceApi = {HuggingFaceApi!r} GroqApi = {GroqApi!r} AssistantName = {AssistantName!r} Username = {Username!r}')
    if GeminiApi:
        set_key('.env', 'CohereAPI', GeminiApi)
    if HuggingFaceApi:
        set_key('.env', 'HuggingFaceAPI', HuggingFaceApi)
    if GroqApi:
        set_key('.env', 'GroqAPI', GroqApi)
    if AssistantName:
        set_key('.env', 'AssistantName', AssistantName)
    if Username:
        set_key('.env', 'NickName', Username)

@eel.expose
def setup():
    """Sets up the GUI window."""
    pyautogui.hotkey('win', 'up')

@eel.expose
def js_language():
    """Returns the input language."""
    return str(InputLanguage)

@eel.expose
def js_assistantname():
    """Returns the assistant's name."""
    return Assistantname

@eel.expose
def js_capture(image_data):
    """Saves the captured image."""
    image_bytes = base64.b64decode(image_data.split(',')[1])
    with open('capture.png', 'wb') as f:
        f.write(image_bytes)

# Initialize Eel and start the application
eel.init('web')
eel.start('spider.html', port=44444)
