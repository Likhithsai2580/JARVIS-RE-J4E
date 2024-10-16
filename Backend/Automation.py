import requests
import random
import asyncio
import platform
import subprocess
import keyboard
from pywhatkit import search, playonyt
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from bs4 import BeautifulSoup
from PIL import Image
from os import listdir, name as os_name
from dotenv import load_dotenv
from random import randint
from rich import print

load_dotenv()

# Constants
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
PROFESSIONAL_RESPONSES = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
    # Add more responses as needed...
]

# Load API keys from environment
HUGGINGFACE_API_KEY = os.getenv('HuggingFaceAPI')
GROQ_API_KEY = os.getenv('GroqAPI')

# Helper function to open a file in the default text editor
def open_notepad(file):
    editor = 'notepad.exe' if os_name == 'nt' else 'open'
    subprocess.Popen([editor, file])

# Function for AI-powered content generation
def content_writer_ai(prompt, client):
    messages = [{'role': 'user', 'content': prompt}]
    system_chat_bot = [{'role': 'system', 'content': "You're a content writer. You create letters, codes, essays, etc."}]
    completion = client.chat.completions.create(
        model='mixtral-8x7b-32768', 
        messages=system_chat_bot + messages, 
        max_tokens=2048, temperature=0.7, top_p=1, stream=True
    )

    answer = ''.join([chunk.choices[0].delta.content for chunk in completion if chunk.choices[0].delta.content]).replace('</s>', '')
    return answer

# Function for generating images using Hugging Face API
async def query_image_generation(payload):
    api_url = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1'
    headers = {'Authorization': f"Bearer {HUGGINGFACE_API_KEY}"}
    response = await asyncio.to_thread(requests.post, api_url, headers=headers, json=payload)
    return response.content

async def generate_images(prompt):
    tasks = [
        asyncio.create_task(query_image_generation({'inputs': f'{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}'}))
        for _ in range(4)
    ]
    image_bytes_list = await asyncio.gather(*tasks)
    for i, image_bytes in enumerate(image_bytes_list):
        with open(f'Images/image{i + 1}.jpg', 'wb') as f:
            f.write(image_bytes)

# Function to open and display images
class ShowImage:
    def __init__(self, image_list):
        self.image_list = image_list

    def open_image(self, index):
        try:
            img = Image.open(f'Images/{self.image_list[index]}')
            img.show()
        except Exception:
            print(f'Error: Unable to open image at {index}')

# Unified function for system commands
def system_command(command):
    commands = {
        'mute': lambda: keyboard.press_and_release('volume mute'),
        'unmute': lambda: keyboard.press_and_release('volume mute'),
        'volume up': lambda: keyboard.press_and_release('volume up'),
        'volume down': lambda: keyboard.press_and_release('volume down'),
        'minimize all': lambda: keyboard.press_and_release('win+d'),
        'shutdown': lambda: os.system('shutdown /s /t 1' if platform.system() == 'Windows' else 'poweroff')
    }

    if command in commands:
        commands[command]()
        return True
    return False

# Function to handle app opening
def open_app(app_name):
    try:
        appopen(app_name, match_closest=True, output=True, throw_error=True)
        return True
    except Exception:
        return False

# Function to handle app closing
def close_app(app_name):
    try:
        close(app_name, match_closest=True, output=True, throw_error=True)
        return True
    except Exception:
        return False

# Function to play YouTube video
def play_youtube(query):
    playonyt(query)
    return True

# Asynchronous task executor
async def execute_commands(commands):
    for command in commands:
        if command.startswith('open '):
            app_name = command.removeprefix('open ')
            open_app(app_name)
        elif command.startswith('close '):
            app_name = command.removeprefix('close ')
            close_app(app_name)
        elif command.startswith('play '):
            play_youtube(command.removeprefix('play '))
        elif command.startswith('system '):
            system_command(command.removeprefix('system '))
        else:
            print(f'No function found for {command}')

# Function to run automation commands
async def run_automation(commands):
    await execute_commands(commands)
    return random.choice(PROFESSIONAL_RESPONSES)
