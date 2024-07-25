# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Backend\RSE.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from groq import Groq
from googlesearch import search
from json import load, dump
from os import environ
from dotenv import load_dotenv
global SystemChat
global messages
load_dotenv()
client = Groq(api_key=environ['GroqAPI'])
DefaultMessage = [{'role': 'user', 'content': f"Hello {environ['AssistantName']}, How are you?"}, {'role': 'assistant', 'content': f"Welcome Back {environ['NickName']}, I am doing well. How may i assist you?"}]
try:
    with open('ChatLog.json', 'r') as f:
        messages = load(f)
except:
    with open('ChatLog.json', 'w') as f:
        dump(DefaultMessage, f)

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for f'{query} 'are : \n[start]\n"
    for i in results:
        Answer += f'Title : {i.title}\nDiscription : {i.description}\n\n'
    Answer += '[end]'
    return Answer
System = f"Hello, I am {environ['NickName']}, You are a very accurate and advance AI chatbot named {environ['AssistantName']} which have realtime up-to-date information of internet.\n*** Just answer the question from the provided data in a professional way. ***"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer
SystemChat = [{'role': 'system', 'content': System}, {'role': 'user', 'content': 'Do you have realtime data ?'}, {'role': 'assistant', 'content': 'Yes, I have all real time data.'}]

def RealTimeChatBotAI(prompt):
    global messages
    with open('ChatLog.json', 'r') as f:
        messages = load(f)
    SystemChat.append({'role': 'system', 'content': GoogleSearch(prompt)})
    completion = client.chat.completions.create(model='mixtral-8x7b-32768', messages=SystemChat + messages, temperature=0.7, max_tokens=2048, top_p=1, stream=True, stop=None)
    Answer = ''
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    Answer = Answer.strip().replace('</s>', '')
    Answer = Answer[0:Answer.find('[')]
    messages.append({'role': 'assistant', 'content': Answer})
    with open('ChatLog.json', 'w') as f:
        dump(messages, f, indent=4)
    SystemChat.pop()
    return AnswerModifier(Answer)
if __name__ == '__main__':
    while True:
        prompt = input('Enter your query: ')
        print(RealTimeChatBotAI(prompt))