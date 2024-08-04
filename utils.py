import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()
file_id = os.getenv("FILE_ID")


def get_file_data():
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(download_url)

    response.raise_for_status()

    return json.loads(response.content)


def get_quotes():
    data = get_file_data()  # получить доступ к содержимому файла
    quotes = []
    for el in data["messages"]:
        if el["type"] == "message":
            if type(el["text"]) is list:
                quotes.append(el["text"][0]["text"])
            else:
                quotes.append(el["text"])
    return quotes
