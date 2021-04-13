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
                'D:/skola_ING/semestr2/FGIS/SP_GDrive_QGIS/credentials.json', SCOPES)
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

def download(file_id, filepath, filename):
    service = getCredentials()
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
filepath = "D:/skola_ING/semestr2/FGIS/SP_GDrive_QGIS"
file_ID_GDrive = '1s06LAx6uThbifIlJcnRoIWOscrpviaUa'
filename = 'tabulka_test.csv'

download(file_ID_GDrive, filepath, filename)
loadVector(filepath, filename)


