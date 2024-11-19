#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import os
import sys
import requests
import platform
import pyperclip
import json


## Get the system type(Windows, Linux or Darwin)
def get_system_type():
    return platform.system()


# Call the XAI API and return the response
def call_xai_api(message):
    xai_key = os.environ.get("XAI_KEY")
    endpoint = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {xai_key}",
        "ContentType": "application/json",
    }
    payload = {
        "messages": [
            {
                "role": role,
                "content": message,
            },
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0,
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    # Check the response
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)  # Print detailed error if available
        sys.exit(1)

    result = response.text
    data = json.loads(result)

    # get the message content
    id_value = data["id"]
    object_type = data["object"]
    created_timestamp = data["created"]
    model_name = data["model"]
    message_content = data["choices"][0]["message"]["content"]
    finish_reason = data["choices"][0]["finish_reason"]
    prompt_tokens = data["usage"]["prompt_tokens"]
    completion_tokens = data["usage"]["completion_tokens"]
    total_tokens = data["usage"]["total_tokens"]
    system_fingerprint = data["system_fingerprint"]

    return message_content


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python grok.py <message>")
        sys.exit(1)
    message = sys.argv[1]
    role = sys.argv[2] if len(sys.argv) > 2 else "user"
    result = call_xai_api(message)
    print(result)
