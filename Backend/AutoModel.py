# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Backend\AutoModel.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import cohere
from Nara.Extra import TimeIt
from rich import print
from json import load, dump
from dotenv import load_dotenv
from os import environ
load_dotenv()
co = cohere.Client(api_key=environ['CohereAPI'])
funcs = ['general', 'realtime', 'open', 'close', 'play', 'generate image', 'system', 'content', 'google search', 'youtube search', 'click', 'double click']

@TimeIt
def Model(prompt: str='test'):
    with open('ChatLog.json', 'r') as f:
        messages = load(f)
    messages.append({'role': 'user', 'content': f'{prompt}'})
    with open('ChatLog.json', 'w') as f:
        dump(messages, f, indent=4)
    stream = co.chat_stream(model='command-r-plus', message=prompt, temperature=0.7, chat_history=[{'role': 'User', 'message': 'how are you'}, {'role': 'Chatbot', 'message': 'general'}, {'role': 'User', 'message': 'do you like pizza'}, {'role': 'Chatbot', 'message': 'general'}, {'role': 'User', 'message': 'open chrome'}, {'role': 'Chatbot', 'message': 'open chrome'}, {'role': 'User', 'message': 'open chrome and firefox'}, {'role': 'Chatbot', 'message': 'open chrome, open firefox'}, {'role': 'User', 'message': 'chat with me'}, {'role': 'Chatbot', 'message': 'general'}], prompt_truncation='OFF', connectors=[], preamble="You are a very accurate Decision-Making-Model, which decides what kind of a query is given to you.\n    You will decide weather a query is a 'general' query or 'realtime' query or is it asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'\n    *** Do not answer any query, just decide what kind of query is given to you. ***\n    -> Respond with 'general' if a query can be answered by a llm model ( conversational ai chatbot ) and doesn't require any up to date information like 'who was akbar?', 'how can i study more effectively?', 'can you help me with this math problem?', 'Thanks, i really liked it.', 'what is python programming language?', etc. Respond with 'general' if a query doesn't have a proper noun or is incomplete like 'who is he?', 'what's his networth?', 'tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general' if the query is asking about time, day, date, month, year, etc.\n    -> Respond with 'realtime' if a query can not be answered by a llm model ( cause they don't have realtime data ) and requires up to date information like 'who is indian prime minister', 'tell me about facebook's recent update.', 'tell me news about coronavirus', etc and if the query is asking about any individual or thing like 'who is akshay kumar', 'what is today's headline', etc.\n    -> Respond with 'open ( application name or website name )' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.\n    -> Respond with 'close ( application name )' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.\n    -> Respond with 'play ( song name )' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.\n    -> Respond with 'generate image ( image prompt )' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.\n    -> Respond with 'system ( task name )' if a query is asking to mute, unmute, minimize, maximize, volmume up, volume down, minimize all windows, maximize all windows, shutdown, restart, etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.\n    -> Respond with 'content ( topic )' if a query is asking to write any type of content like application, codes, emails or anything else about a sepecific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic , content 2nd topic' and so on.\n    -> Respond with 'google search ( topic )' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.\n    -> Respond with 'youtube search ( topic )' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.\n    -> Respond with 'click ( text )' if a query is asking to click any text on the screen like 'click on facebook', 'click on instagram', etc. but if the query is asking to click multiple texts, respond with 'click 1st_text, click 2nd_text' and so on.\n    -> Respond with 'double click ( text )' if a query is asking to click any text on the screen like 'double click on facebook', 'double click on instagram', etc. but if the query is asking to click multiple texts, respond with 'double click 1st_text, double click 2nd_text' and so on.\n    -> Respond with 'open webcam' if a query is asking to open webcam.\n    -> Respond with 'close webcam' if a query is asking to close webcam.\n    *** if the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp', respond with 'open facebook, open telegram, close whatsapp' ***\n    *** Respond with 'general' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***")
    response = ''
    for event in stream:
        if event.event_type == 'text-generation':
            response += event.text
            print(event.text, end='')
    print()
    response = response.replace('\n', '')
    response = response.split(',')
    response = [i.strip() for i in response]
    temp = []
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)
    if len(temp) == 0:
        temp.append('general')
    response = temp
    return response
if __name__ == '__main__':
    while True:
        print(Model(input('>>> ')))