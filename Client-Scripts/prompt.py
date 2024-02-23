import base64
import requests
import display_response
from datetime import datetime
from client.client import main
from typing import Optional, Any

IMAGE_PATH = "./resources/Image_to_analyze.jpg"
ARCHIVE_NAME = "resources/session.json"
legal_session_terminators = ('good bye', 'goodbye', 'end session', 'turn off', 'shut down', 'shutdown', 'shutoff', 'shut off')

# OpenAI API Key
api_key = "OPEN_AI_API"


def write_to_file(content: str):
  timestamp = datetime.today().strftime('%Y-%m-%d')
  file_entry = f'({str(timestamp)}'+' : '+ f'{content})'
  with open(ARCHIVE_NAME, 'a+') as file:
    file.write(file_entry)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_response(user_prompt: str, image: bool) -> str:

  for word in legal_session_terminators:
    if word in user_prompt:
      print('Haibo, says goodbye')
      main('POST', ARCHIVE_NAME)
      exit(0)

  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
  }

  content_array = [{"type": "text",
                    "text": f"{user_prompt}"
                  }]
  if image:
    # Path to image
    # Getting the base64 string
    base64_image = encode_image(IMAGE_PATH)
    content_array.append({"type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                        }})
  
  role_system = {"role": "system",
                 "content": "Your name is "Haibo", you are an daily AI assistant, \
                             skilled in providing your user with summaries of information \
                             and answering their queries in short messages no more than 25 words."
                }
  
  role_user = {"role": "user",
                "content": content_array
              }

  payload = {
      "model": "gpt-4-vision-preview",
      "messages": [role_system, role_user],
      "max_tokens": 30
  }
  write_to_file(user_prompt)

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

  assistant_message = (response.json())['choices'][0]['message']['content']
  
  display_response.message_to_display(assistant_message, image)
  print(f'Haibo: {assistant_message}')
  return f'Haibo: {assistant_message}'
