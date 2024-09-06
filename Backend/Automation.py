# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Backend\Automation.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import requests
from pywhatkit import search, playonyt
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from rich import print
import random
from bs4 import BeautifulSoup
from groq import Groq
import platform
import webbrowser
import asyncio
from random import randint
from PIL import Image
from os import listdir
from dotenv import load_dotenv
import os
import subprocess
import keyboard
load_dotenv()
system_platform = platform.system()
classes = ['zCubwf', 'hgKElc', 'LTKOO sY7ric', 'Z0LcW', 'gsrt vk_bk FzvWSb YwPhnf', 'pclqee', 'tw-Data-text tw-text-small tw-ta', 'IZ6rdc', 'O5uR6d LTKOO', 'vlzY6d', 'webanswers-webanswers_table__webanswers-table', 'dDoNo ikb4Bb gsrt', 'sXLaOe', 'LWkfKe', 'VQF4g', 'qv3Wpe', 'kno-rdesc', 'SPZz6b']
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
professional_responses = ["Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.", "I'm at your service for any additional questions or support you may need—don't hesitate to ask.", "Continued support is my commitment to you. Let me know if there's anything more I can do for you.", "I'm here to ensure your experience is seamless. If you have any further requests, please let me know.", "Your needs are important to me. If there's anything I can assist you with, I'm just a message away.", "I'm dedicated to providing excellent service. Should you require further assistance, I'm here for you.", "Exceeding your expectations is my goal. Don't hesitate to reach out for any additional help you may need.", 'Your satisfaction matters. If you have more questions or need assistance, feel free to ask.', "I'm committed to making your experience positive. Let me know if there's anything else I can do for you.", "Your feedback is valued. If there's anything I can do to enhance your experience, please let me know.", "If there's anything specific you'd like assistance with, please share, and I'll be happy to help.", 'Your concerns are important to me. Feel free to ask for further guidance or information.', "I'm here to address any additional queries or provide clarification as needed.", "For a seamless experience, let me know if there's anything else you require assistance with.", "Your satisfaction is key; if there's a specific area you'd like more support in, I'm here for you.", "Don't hesitate to let me know if there's a particular aspect you'd like further clarification on.", "I aim to make your interaction effortless. If there's more you need, feel free to inform me.", "Your input is valuable. Please share any additional requirements, and I'll respond promptly.", "Should you require more details or have additional questions, I'm ready to provide assistance.", "Your success is important to me. If there's anything else you need support with, feel free to ask."]
client = Groq(api_key=os.environ['GroqAPI'])
messages = []
SystemChatBot = [{'role': 'system', 'content': f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

def OpenNotepad(File):
    file_path = File
    if os.name == 'posix':
        default_text_editor = 'open'
    elif os.name == 'nt':
        default_text_editor = 'notepad.exe'
    subprocess.Popen([default_text_editor, file_path])

def ContentWriterAI(prompt):
    messages.append({'role': 'user', 'content': f'{prompt}'})
    completion = client.chat.completions.create(model='mixtral-8x7b-32768', messages=SystemChatBot + messages, max_tokens=2048, temperature=0.7, top_p=1, stream=True, stop=None)
    Answer = ''
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    Answer = Answer.replace('</s>', '')
    messages.append({'role': 'assistant', 'content': Answer})
    return Answer

def Search(Topic):
    search(Topic)
    return random.choice(professional_responses)

def Content(Topic):
    Topic = Topic.replace('Content ', '')
    ContentByAI = ContentWriterAI(Topic)
    with open(f"{Topic.lower().replace(' ', '')}.txt", 'w', encoding='utf-8') as file:
        file.write(ContentByAI)
        file.close()
    OpenNotepad(f"{Topic.lower().replace(' ', '')}.txt")
    return random.choice(professional_responses)

def YouTubeSearch(Topic):
    Url4Search = f'https://www.youtube.com/results?search_query={Topic}'
    webbrowser.open(Url4Search)
    return random.choice(professional_responses)
API_URL = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1'
headers = {'Authorization': f"Bearer {os.environ['HuggingFaceAPI']}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_images(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {'inputs': f'{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}'}
        task = asyncio.create_task(query(payload))
        tasks.append(task)
    image_bytes_list = await asyncio.gather(*tasks)
    for i, image_bytes in enumerate(image_bytes_list):
        with open(f'Images//image{i + 1}.jpg', 'wb') as f:
            f.write(image_bytes)

class Show_Image:

    def __init__(self, li: list) -> None:
        self.listd = li

    def open(self, no):
        try:
            img = Image.open(f'Images//{self.listd[no]}')
            img.show()
        except:
            print(f'Images//{self.listd[no]}')
            self.open(no + 1)

    def close(self, no):
        return

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    x = Show_Image(listdir('Images')[-4:])
    x.open(0)
    x.open(1)
    x.open(2)
    x.open(3)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:

        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f'https://www.google.com/search?q={query}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
            response = sess.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
            print('Failed to retrieve search results.')
            return
        html = search_google(app)
        if html:
            link = extract_links(html)[0]
            webopen(link)
        return True

def CloseApp(app):
    if 'chrome' in app:
        return False
    try:
        close(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

def System(command):

    def mute():
        if platform.system() == 'Windows':
            keyboard.press_and_release('volume mute')
        elif platform.system() == 'Darwin':
            os.system("osascript -e 'set volume output muted true'")
        elif platform.system() == 'Linux':
            os.system('amixer -D pulse sset Master mute')

    def unmute():
        if platform.system() == 'Windows':
            keyboard.press_and_release('volume mute')
        elif platform.system() == 'Darwin':
            os.system("osascript -e 'set volume output muted false'")
        elif platform.system() == 'Linux':
            os.system('amixer -D pulse sset Master unmute')

    def volume_up():
        if platform.system() == 'Windows':
            keyboard.press_and_release('volume up')
        elif platform.system() == 'Darwin':
            os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) + 10)'")
        elif platform.system() == 'Linux':
            os.system('amixer -D pulse sset Master 5%+')

    def volume_down():
        if platform.system() == 'Windows':
            keyboard.press_and_release('volume down')
        elif platform.system() == 'Darwin':
            os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) - 10)'")
        elif platform.system() == 'Linux':
            os.system('amixer -D pulse sset Master 5%-')

    def minimize_all_windows():
        if platform.system() == 'Windows':
            keyboard.press_and_release('win+d')
        elif platform.system() == 'Darwin':
            os.system('osascript -e \'tell application "System Events" to keystroke "h" using {command down, option down}\'')
        elif platform.system() == 'Linux':
            os.system('xdotool key Super+d')

    def maximize_all_windows():
        if platform.system() == 'Windows':
            return
        if platform.system() == 'Darwin':
            return
        if platform.system() == 'Linux':
            return

    def shutdown():
        if platform.system() == 'Windows':
            os.system('shutdown /s /t 1')
        elif platform.system() == 'Darwin':
            os.system('osascript -e \'tell application "System Events" to shut down\'')
        elif platform.system() == 'Linux':
            os.system('poweroff')

    def restart():
        if platform.system() == 'Windows':
            os.system('shutdown /r /t 1')
        elif platform.system() == 'Darwin':
            os.system('osascript -e \'tell application "System Events" to restart\'')
        elif platform.system() == 'Linux':
            os.system('reboot')
    if command == 'mute':
        mute()
        return True
    if command == 'unmute':
        unmute()
        return True
    if command == 'volume up':
        volume_up()
        return True
    if command == 'volume down':
        volume_down()
        return True
    if command == 'minimize all':
        minimize_all_windows()
        return True
    if command == 'maximize all':
        maximize_all_windows()
        return True
    if command == 'shutdown':
        shutdown()
        return True
    if command == 'restart':
        restart()
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith('open '):
            if 'open it' in command:
                pass
            if 'open file' == command:
                continue
            fun = asyncio.to_thread(OpenApp, command.removeprefix('open '))
            funcs.append(fun)
        elif command.startswith('close '):
            fun = asyncio.to_thread(CloseApp, command.removeprefix('close '))
            funcs.append(fun)
        elif command.startswith('play '):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix('play '))
            funcs.append(fun)
        elif command.startswith('generate image'):
            fun = asyncio.to_thread(GenerateImages, command.removeprefix('generate image'))
            funcs.append(fun)
        elif command.startswith('content '):
            fun = asyncio.to_thread(Content, command.removeprefix('content '))
            funcs.append(fun)
        elif command.startswith('google search '):
            fun = asyncio.to_thread(Search, command.removeprefix('google search '))
            funcs.append(fun)
        elif command.startswith('youtube search '):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix('youtube search '))
            funcs.append(fun)
        elif command.startswith('system '):
            fun = asyncio.to_thread(System, command.removeprefix('system '))
            funcs.append(fun)
        else:
            print(f'No Function Found. For {command}')
    results = await asyncio.gather(*funcs)
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str], func=print):
    async for result in TranslateAndExecute(commands):
        func(result)
