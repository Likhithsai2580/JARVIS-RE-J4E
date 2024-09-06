# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Backend\TTS.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import load_dotenv
load_dotenv()

async def TextToAudioFile(text) -> None:
    file_path = 'data.mp3'
    if os.path.exists(file_path):
        os.remove(file_path)
    communicate = edge_tts.Communicate(text, os.environ['AssistantVoice'], pitch='+5Hz', rate='+22%')
    await communicate.save('data.mp3')

def TextToSpeech(Text, func=lambda r=None: True):
    asyncio.run(TextToAudioFile(Text))
    pygame.mixer.init()
    pygame.mixer.music.load('data.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if func() == False:
            break
        else:
            pygame.time.Clock().tick(10)
    func(False)
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def TTS(Text, func=lambda r=None: True):
    Data = str(Text).split('.')
    responses = ['The rest of the result has been printed to the chat screen, kindly check it out sir.The rest of the text is now on the chat screen, sir, please check it.', 'You can see the rest of the text on the chat screen, sir.', 'The remaining part of the text is now on the chat screen, sir.', "Sir, you'll find more text on the chat screen for you to see.", 'The rest of the answer is now on the chat screen, sir.', 'Sir, please look at the chat screen, the rest of the answer is there.', "You'll find the complete answer on the chat screen, sir.", 'The next part of the text is on the chat screen, sir.', 'Sir, please check the chat screen for more information.', "There's more text on the chat screen for you, sir.", 'Sir, take a look at the chat screen for additional text.', "You'll find more to read on the chat screen, sir.", 'Sir, check the chat screen for the rest of the text.', 'The chat screen has the rest of the text, sir.', "There's more to see on the chat screen, sir, please look.", 'Sir, the chat screen holds the continuation of the text.', "You'll find the complete answer on the chat screen, kindly check it out sir.", 'Please review the chat screen for the rest of the text, sir.', 'Sir, look at the chat screen for the complete answer.']
    if len(Data) > 4 and len(Text) >= 250:
        TextToSpeech(' '.join(Text.split('.')[0:2]) + '. ' + random.choice(responses), func)
    else:
        TextToSpeech(Text, func)
if __name__ == '__main__':
    while True:
        TTS(input('Enter the text : '))
