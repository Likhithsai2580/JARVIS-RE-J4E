import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def TextToAudioFile(text: str) -> None:
    """Converts text to an audio file."""
    file_path = 'data.mp3'
    if os.path.exists(file_path):
        os.remove(file_path)
    communicate = edge_tts.Communicate(text, os.environ['AssistantVoice'], pitch='+5Hz', rate='+22%')
    await communicate.save(file_path)

def TextToSpeech(text: str, func=lambda r=None: True) -> None:
    """Plays the converted text audio file."""
    try:
        asyncio.run(TextToAudioFile(text))
        pygame.mixer.init()
        pygame.mixer.music.load('data.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if not func():
                break
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

def TTS(text: str, func=lambda r=None: True) -> None:
    """Handles TTS for long texts by splitting and adding additional instructions."""
    responses = [
        'The rest of the result has been printed to the chat screen, kindly check it out.',
        'You can see the rest of the text on the chat screen.',
        'The remaining part of the text is now on the chat screen.',
        "You'll find more text on the chat screen.",
        'Please check the chat screen for additional text.'
    ]
    
    data = text.split('.')
    if len(data) > 4 and len(text) >= 250:
        prompt = ' '.join(data[:2]) + '. ' + random.choice(responses)
        TextToSpeech(prompt, func)
    else:
        TextToSpeech(text, func)

if __name__ == '__main__':
    while True:
        user_input = input('Enter the text: ')
        TTS(user_input)
