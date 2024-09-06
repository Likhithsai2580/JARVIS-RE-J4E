import json
from dotenv import load_dotenv
from os import environ

load_dotenv()

def AnswerModifier(Answer):
    """
    Removes empty lines from the given Answer.
    """
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    """
    Modifies a given query by ensuring proper casing and punctuation.
    Adds a question mark for queries with question words or a period otherwise.
    """
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ['how', 'what', 'who', 'where', 'when', 'why', 'which', 'whose', 'whom', 'can you', "what's", "where's", "how's"]
    
    # Check if the query is a question
    if any((word + ' ' in new_query for word in question_words)):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + '?'
        else:
            new_query += '?'
        return new_query.capitalize()
    
    # Add a period to non-question statements
    if query_words[-1][-1] in ['.', '?', '!']:
        new_query = new_query[:-1] + '.'
    else:
        new_query += '.'
    
    return new_query.capitalize()

def LoadMessages():
    """
    Loads messages from ChatLog.json and returns them.
    Adds error handling for file reading issues.
    """
    try:
        with open('ChatLog.json', 'r') as f:
            messages = json.load(f)
        return messages
    except FileNotFoundError:
        print("ChatLog.json file not found!")
        return []
    except json.JSONDecodeError:
        print("Error decoding ChatLog.json!")
        return []

def GuiMessagesConverter(messages: list[dict[str, str]]):
    """
    Converts a list of messages to a format suitable for a GUI.
    Each message is wrapped with HTML-like tags based on the role (user/assistant).
    """
    temp = []
    Assistantname = environ.get('AssistantName', 'Assistant')
    Username = environ.get('NickName', 'User')

    for message in messages:
        if message['role'] == 'assistant':
            temp.append(f"""<span class="Assistant">{Assistantname}</span> : {message['content']}""")
            temp.append('[*end*]')
        elif message['role'] == 'user':
            temp.append(f"""<span class="User">{Username}</span> : {message['content']}""")
        else:
            temp.append(f"""<span class="User">{Username}</span> : {message['content']}""")
    
    return temp
