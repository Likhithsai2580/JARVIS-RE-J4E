import cohere
from Nara.Extra import TimeIt
from rich import print
from json import load, dump
from dotenv import load_dotenv
from os import environ

# Load environment variables from .env file
load_dotenv()

# Initialize Cohere client with API key
co = cohere.Client(api_key=environ['CohereAPI'])

# List of known functions that the model will decide upon
funcs = [
    'general', 'realtime', 'open', 'close', 'play', 
    'generate image', 'system', 'content', 'google search', 
    'youtube search', 'click', 'double click'
]

@TimeIt
def Model(prompt: str = 'test'):
    """
    The main function that processes a prompt, appends it to the chat log,
    and sends it to the Cohere API for decision-making on query types.
    """
    
    # Load chat history from ChatLog.json
    with open('ChatLog.json', 'r') as f:
        messages = load(f)
    
    # Append the user's prompt to the chat history
    messages.append({'role': 'user', 'content': f'{prompt}'})
    
    # Save the updated chat history
    with open('ChatLog.json', 'w') as f:
        dump(messages, f, indent=4)
    
    # Cohere streaming response to classify the prompt
    stream = co.chat_stream(
        model='command-r-plus', 
        message=prompt, 
        temperature=0.7, 
        chat_history=[
            {'role': 'User', 'message': 'how are you'},
            {'role': 'Chatbot', 'message': 'general'},
            {'role': 'User', 'message': 'do you like pizza'},
            {'role': 'Chatbot', 'message': 'general'},
            {'role': 'User', 'message': 'open chrome'},
            {'role': 'Chatbot', 'message': 'open chrome'},
            {'role': 'User', 'message': 'open chrome and firefox'},
            {'role': 'Chatbot', 'message': 'open chrome, open firefox'},
            {'role': 'User', 'message': 'chat with me'},
            {'role': 'Chatbot', 'message': 'general'}
        ],
        prompt_truncation='OFF',
        connectors=[], 
        preamble=(
            "You are a very accurate Decision-Making-Model, which decides what kind of a query is given to you.\n"
            "You will decide whether a query is a 'general' query or 'realtime' query or is it asking to perform any task or automation like 'open facebook, instagram', etc.\n"
            "*** Do not answer any query, just decide what kind of query is given to you. ***\n"
            "-> Respond with 'general' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require up-to-date information.\n"
            "-> Respond with 'realtime' if a query cannot be answered by an llm model (needs real-time data).\n"
            "-> Respond with 'open (application name or website name)' if a query asks to open any application.\n"
            "-> Respond with 'close (application name)' if a query asks to close any application.\n"
            "-> Respond with 'play (song name)' if a query asks to play any song.\n"
            "-> Respond with 'generate image (image prompt)' if a query asks to generate an image.\n"
            "-> Respond with 'system (task name)' if a query asks to perform system tasks (mute, shutdown, etc.).\n"
            "-> Respond with 'content (topic)' if a query asks to write content (application, email, code, etc.).\n"
            "-> Respond with 'google search (topic)' if a query asks to search a topic on Google.\n"
            "-> Respond with 'youtube search (topic)' if a query asks to search a topic on YouTube.\n"
            "-> Respond with 'click (text)' or 'double click (text)' if a query asks to click on any text on the screen.\n"
            "*** If the query asks for multiple tasks, respond accordingly. ***\n"
            "*** Respond with 'general' if you can't decide the type of query. ***"
        )
    )

    response = ''
    # Collect the response text from the Cohere API stream
    for event in stream:
        if event.event_type == 'text-generation':
            response += event.text
            print(event.text, end='')

    print()  # Print a newline after streaming
    
    # Clean up the response, split it by commas and remove extra spaces
    response = response.replace('\n', '').split(',')
    response = [i.strip() for i in response]

    # Filter out only the valid tasks based on the known functions
    valid_responses = [task for task in response if any(task.startswith(func) for func in funcs)]

    # If no valid tasks were found, assume the response is 'general'
    if not valid_responses:
        valid_responses.append('general')

    return valid_responses

if __name__ == '__main__':
    # Continuously take user input and classify the prompt
    while True:
        user_input = input('>>> ')
        print(Model(user_input))
