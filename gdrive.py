from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path, json

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

service = None


def get_file_data():
    data = json.load(open('quotes.json')) 
    return data
    # List the files in your Google Drive
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f'{item["name"]} ({item["id"]})')

def get_quotes():
    data = get_file_data() # получить доступ к содержимому файла
    quotes = []
    for el in data['messages']:
        if el['type'] == 'message':
            if type(el['text']) is list:
                quotes.append(el['text'][0]['text'])
            else:
                quotes.append(el['text'])
    return quotes

def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


# service = build('drive', 'v3', credentials=get_creds())


