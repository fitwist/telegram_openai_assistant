import requests
from dotenv import load_dotenv
from os import environ as env

load_dotenv()

# Установите ваш API ключ
API_KEY = env['OPENAI_API_KEY']
ASSISTANT_ID = env['ASSISTANT_ID']
BASE_URL = f'https://api.openai.com/v1/assistants/{ASSISTANT_ID}/messages'

def send_message_to_assistant(message):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'message': {
            'role': 'user',
            'content': message
        }
    }
    
    response = requests.post(BASE_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    else:
        return f'Error: {response.status_code}, {response.text}'

if __name__ == "__main__":
    user_message = "Привет, как дела?"
    assistant_response = send_message_to_assistant(user_message)
    print("Ассистент:", assistant_response)
