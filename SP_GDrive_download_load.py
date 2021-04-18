#GDrive Download + load

from __future__ import print_function

import os.path, io#, httplib2

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.http import MediaIoBaseDownload #, MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file'
          ]

def getCredentials():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                filepath + '/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def listFiles(size):
    # Call the Drive v3 API
    service = getCredentials()
    results = service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            
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

def download(filepath, filename):
    service = getCredentials()
    search_result = search(service, query=f"name='{filename}'")
    file_id = search_result[0][0]
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath+"/"+filename, "wb") as f:
        fh.seek(0)
        f.write(fh.read())

def loadVector(filepath, filename):
    uri = "file:///"+filepath+"/"+filename+"?encoding={}&delimiter={}&xField={}&yField={}&crs={}".format("UTF-8",",", "longitude", "latitude","epsg:4326")

    eq_layer=QgsVectorLayer(uri,filename,"delimitedtext")

    if not eq_layer.isValid():
        print ("Layer not loaded")

    QgsProject.instance().addMapLayer(eq_layer)

#listFiles(10)
os.chdir(QgsProject.instance().readPath("./"))
filepath = os.getcwd()

filename = 'eq-data.csv'

download(filepath, filename)
loadVector(filepath, filename)


