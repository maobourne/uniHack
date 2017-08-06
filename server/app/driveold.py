from __future__ import print_function
import httplib2
import os

from apiclient import *
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload
from oauth2client.contrib import gce

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/devstorage.read_write'
SCOPES = "https://www.googleapis.com/auth/drive"
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
prefix = "https://drive.google.com/uc?export=download&id="


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # home_dir = os.path.expanduser('~')
    # credential_dir = os.path.join(home_dir, '.credentials')
    # if not os.path.exists(credential_dir):
    #     os.makedirs(credential_dir)
    # credential_path = os.path.join(credential_dir,
    #                                'client_secret.json')

    # store = Storage(credential_path)
    # credentials = store.get()
    # # print(credentials)
    # if not credentials or credentials.invalid or credentials is None:
    #     flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    #     flow.user_agent = APPLICATION_NAME  
        
    #     if flags:
    #         credentials = tools.run_flow(flow, store, flags)
    #     print('Storing credentials to ' + credential_path)
    # return credentials

    credentials = gce.AppAssertionCredentials(
        scope=SCOPES)
    return credentials


def main(fname, folder_id, IMAGE_SOURCE):
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    # https://developers.google.com/drive/v3/web/folder

    file_metadata = {
        'name': fname,
        'parents': [folder_id]
    }
    media = MediaFileUpload(IMAGE_SOURCE,
                            mimetype='image/jpeg',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    # print('File ID: %s' % file.get('id'))
    # print('Link: %s' % prefix + file.get('id'))

    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s" % response.get('id'))

    batch = service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    batch.add(service.permissions().create(
        fileId=file.get('id'),
        body=user_permission,
        fields='id',
    ))
    domain_permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    batch.add(service.permissions().create(
        fileId=file.get('id'),
        body=domain_permission,
        fields='id',
    ))
    batch.execute()

    return prefix + file.get('id'), service

# if __name__ == '__main__':
    # main(IMAGE_SOURCE)
