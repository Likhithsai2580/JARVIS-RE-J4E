# Import required libraries and modules
from groq import Groq
from json import load, dump
import datetime
from dotenv import load_dotenv
from os import environ

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq API client
client = Groq(api_key=environ['GroqAPI'])

# Define system message and system chat history
System = (
    f"Hello, I am {environ['NickName']}, you are a very accurate and advanced AI chatbot named {environ['AssistantName']} "
    f"which also has real-time up-to-date information from the internet.\n"
    "*** Do not tell time unless I ask, do not talk too much, just answer the question. ***\n"
    "*** Provide answers in a professional way. Make sure to use proper grammar with full stops, commas, and question marks. ***\n"
    "*** Reply in the same language as the question: Hindi in Hindi, English in English. ***\n"
    "*** Do not mention your training data or provide notes in the output. Just answer the question. ***"
)

SystemChatBot = [
    {'role': 'system', 'content': System},
    {'role': 'user', 'content': 'Hi'},
    {'role': 'assistant', 'content': 'Hello, how can I help you?'}
]

# Default message when there is no existing chat log
DefaultMessage = [
    {'role': 'user', 'content': f"Hello {environ['AssistantName']}, how are you?"},
    {'role': 'assistant', 'content': f"Welcome back {environ['NickName']}, I am doing well. How may I assist you?"}
]

# Load chat history from ChatLog.json or initialize it with a default message if not available
try:
    with open('ChatLog.json', 'r') as f:
        messages = load(f)
except FileNotFoundError:
    with open('ChatLog.json', 'w') as f:
        dump(DefaultMessage, f)

def Information():
    """
    Provides real-time information including the current day, date, and time.
    """
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime('%A')
    date = current_date_time.strftime('%d')
    month = current_date_time.strftime('%B')
    year = current_date_time.strftime('%Y')
    hour = current_date_time.strftime('%H')
    minute = current_date_time.strftime('%M')
    second = current_date_time.strftime('%S')

    data = (
        f"Use this real-time information if needed:\n"
        f"Day: {day}\n"
        f"Date: {date}\n"
        f"Month: {month}\n"
        f"Year: {year}\n"
        f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    )
    return data

def AnswerModifier(answer):
    """
    Modifies the answer by removing any empty lines.
    """
    lines = answer.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

def ChatBotAI(prompt):
    """
    Handles the chatbot's logic, sending the prompt to the Groq API and updating the chat history.
    """
    try:
        # Load existing chat log
        with open('ChatLog.json', 'r') as f:
            messages = load(f)

        # Send request to the Groq API with real-time information
        completion = client.chat.completions.create(
            model='llama3-70b-8192',
            messages=SystemChatBot + [{'role': 'system', 'content': Information()}] + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        # Collect the response
        answer = ''
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        # Append the assistant's answer to the chat log
        messages.append({'role': 'assistant', 'content': answer})
        
        # Save updated chat history
        with open('ChatLog.json', 'w') as f:
            dump(messages, f, indent=4)

        # Return the modified answer
        return AnswerModifier(answer)

    except Exception as e:
        # Log the error and reset the chat log if an error occurs
        print(f"Error: {e}")
        with open('ChatLog.json', 'w') as f:
            dump([], f, indent=4)
        return ChatBotAI(prompt)  # Retry after resetting the log

if __name__ == '__main__':
    while True:
        user_input = input('Enter Your Question: ')
        print(ChatBotAI(user_input))
