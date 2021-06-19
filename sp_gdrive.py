#GDrive Download + load

import os.path, io#, httplib2

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaIoBaseDownload, MediaFileUpload

from qgis.core import QgsVectorLayer, Qgis
from qgis.utils import iface

# If modifying these scopes, delete the file token.json.
SCOPES = [
          'https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive.file'
          ]

def getCredentials(filepath):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(filepath + '/token.json'):
        creds = Credentials.from_authorized_user_file(filepath + '/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            iface.messageBar().pushMessage('Authorize in your browser.', duration=1, level=Qgis.Info)
            flow = InstalledAppFlow.from_client_secrets_file(
                filepath + '/credentials.json', SCOPES)
            print(filepath)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(filepath + '/token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def search(service, query):
    # search for the file
    result = []
    page_token = None
    while True:
        response = service.files().list(q=query,
                                        spaces="drive",
                                        fields="nextPageToken, files(id, name, mimeType)",
                                        pageToken=page_token).execute()
        # iterate over filtered files
        for file in response.get("files", []):
            # print(f"Found file: {file['name']} with the id {file['id']} and type {file['mimeType']}")
            result.append((file["id"], file["name"], file["mimeType"]))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            # no more files
            break
    return result

def downloadSpreadsheet(filepath, filename):
    service = getCredentials(filepath)
    search_result = search(service, query=f"name='{filename}'")
    file_id = search_result[0][0]
    request = service.files().export_media(fileId=file_id, mimeType='text/csv')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

        # "Download %d%%." % int(status.progress() * 100)
    with io.open(filepath+"/"+filename+".csv", "wb") as f:
        fh.seek(0)
        f.write(fh.read())


