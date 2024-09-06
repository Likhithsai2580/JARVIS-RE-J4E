import requests
import os
from rich import print
from dotenv import load_dotenv
import base64
from json import load, dump
import datetime

load_dotenv()

class LLM:
    USER = 'user'
    ASSISTANT = 'assistant'
    SYSTEM = 'system'

    def __init__(self, messages: list[dict[str, str]] = [], model: str = 'rohan/tune-gpt-4o', temperature: float = 0.0, system_prompt: str = '', max_tokens: int = 2048, verbose: bool = False, api_key: str | None = None) -> None:
        """
        Initializes the LLM with the given parameters.
        """
        self.api_key = api_key or os.getenv('TuneStudioAPI', '')
        if not self.api_key:
            raise ValueError("API key is missing")
        
        self.session = requests.Session()
        self.messages = messages
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.verbose = verbose

    def run(self, prompt: str | None = None) -> str:
        """
        Runs the LLM with the given prompt and returns the response.
        """
        if prompt:
            self.add_message('user', prompt)

        url = 'https://proxy.tune.app/chat/completions'
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json',
            'X-Org-Id': 'b7e11655-fa97-4f1c-8cde-d9eca2b9814b'
        }
        data = {
            'temperature': self.temperature,
            'messages': self.messages,
            'model': self.model,
            'stream': False,
            'frequency_penalty': 0.0,
            'max_tokens': self.max_tokens
        }
        response = self.session.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception if the request fails

        if self.verbose:
            print(response.json())
        
        return response.json()['choices'][0]['message']['content']

    def add_message(self, role: str, content: str = '', base64_image: str = '') -> None:
        """
        Adds a message to the LLM conversation.
        """
        message_content = []
        if content:
            message_content.append({'type': 'text', 'text': content})
        if base64_image:
            message_content.append({'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{base64_image}'}})
        
        if message_content:
            self.messages.append({'role': role, 'content': message_content})
        else:
            raise ValueError('Both content and base64_image are empty')

    def __getitem__(self, index) -> dict[str, str] | list[dict[str, str]]:
        """
        Returns the message at the given index.
        """
        return self.messages[index] if isinstance(index, int) else self.messages[index]

    def __setitem__(self, index, value) -> None:
        """
        Sets the message at the given index to the given value.
        """
        if isinstance(index, int):
            self.messages[index] = value
        else:
            raise TypeError('Invalid argument type')

def Information() -> str:
    """
    Provides real-time information such as date and time.
    """
    current_date_time = datetime.datetime.now()
    data = f"""Use This Realtime Information if needed:
Day: {current_date_time.strftime('%A')}
Date: {current_date_time.strftime('%d')}
Month: {current_date_time.strftime('%B')}
Year: {current_date_time.strftime('%Y')}
Time: {current_date_time.strftime('%H')} hours :{current_date_time.strftime('%M')} minutes :{current_date_time.strftime('%S')} seconds.
"""
    return data

def AnswerModifier(answer: str) -> str:
    """
    Cleans up the answer by removing unnecessary blank lines.
    """
    return '\n'.join([line.strip() for line in answer.split('\n') if line.strip()])

def FileToBase64(file_path: str) -> str:
    """
    Convert an image file to base64.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    
    with open(file_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ChatBotAI(prompt: str) -> str:
    """
    Main function to handle the chatbot logic.
    """
    try:
        with open('ChatLog.json', 'r') as f:
            messages = load(f)

        llm = LLM(messages=SystemChatBot + [{'role': 'system', 'content': Information()}])

        base64_image = FileToBase64('capture.png')
        llm.add_message('user', content=prompt, base64_image=base64_image)

        answer = llm.run()

        messages.append({'role': 'assistant', 'content': answer})
        
        with open('ChatLog.json', 'w') as f:
            dump(messages, f, indent=4)

        return AnswerModifier(answer)
    
    except Exception as e:
        print(f"Error: {e}")
        # Resetting the chat log in case of failure
        with open('ChatLog.json', 'w') as f:
            dump([], f, indent=4)
        return ChatBotAI(prompt)

if __name__ == '__main__':
    print(ChatBotAI('What can you see in the image?'))
