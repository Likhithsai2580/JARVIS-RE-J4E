# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Backend\Chatbot.py
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from groq import Groq
from json import load, dump
import datetime
from dotenv import load_dotenv
from os import environ
load_dotenv()
client = Groq(api_key=environ['GroqAPI'])
messages = []
System = f"Hello, I am {environ['NickName']}, You are a very accurate and advance AI chatbot named {environ['AssistantName']} which also have realtime up-to-date information of internet.\n*** Do not tell time until i ask, do not talk too much, just answer to the question.***\n*** Provide Answers In a Professional Way, make sure to add fullstops, comma, question mark and use proper grammar.***\n*** Reply in the same language, if the question is in hindi, then reply in hindi. if the question is in english, then reply in english.***\n*** Do not provide note in the output, just answer the question and never mention your training data. ***"
SystemChatBot = [{'role': 'system', 'content': System}, {'role': 'user', 'content': 'Hi'}, {'role': 'assistant', 'content': 'Hello, how can I help you?'}]
DefaultMessage = [{'role': 'user', 'content': f"Hello {environ['AssistantName']}, How are you?"}, {'role': 'assistant', 'content': f"Welcome Back {environ['NickName']}, I am doing well. How may i assist you?"}]
try:
    with open('ChatLog.json', 'r') as f:
        messages = load(f)
except:
    with open('ChatLog.json', 'w') as f:
        dump(DefaultMessage, f)

def Information():
    data = ''
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime('%A')
    date = current_date_time.strftime('%d')
    month = current_date_time.strftime('%B')
    year = current_date_time.strftime('%Y')
    hour = current_date_time.strftime('%H')
    minute = current_date_time.strftime('%M')
    second = current_date_time.strftime('%S')
    data += 'Use This Realtime Information. if needed\n'
    data += f'Day: {day}\n'
    data += f'Date: {date}\n'
    data += f'Month: {month}\n'
    data += f'Year: {year}\n'
    data += f'Time: {hour} hours :{minute} minutes :{second} seconds.\n'
    return data

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def ChatBotAI(prompt):
    try:
        with open('ChatLog.json', 'r') as f:
            messages = load(f)
        completion = client.chat.completions.create(model='llama3-70b-8192', messages=SystemChatBot + [{'role': 'system', 'content': Information()}] + messages, max_tokens=2048, temperature=0.7, top_p=1, stream=True, stop=None)
        Answer = ''
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        messages.append({'role': 'assistant', 'content': Answer})
        with open('ChatLog.json', 'w') as f:
            dump(messages, f, indent=4)
        return AnswerModifier(Answer)
    except Exception as e:
        print(e)
        with open('ChatLog.json', 'w') as f:
            dump([], f, indent=4)
        return ChatBotAI(prompt)
if __name__ == '__main__':
    while True:
        print(ChatBotAI(input('Enter Your Question : ')))