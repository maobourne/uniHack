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
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'client_secret.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid or credentials is None:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME  
        
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials
    # home_dir = os.path.expanduser('~')
    # credential_dir = os.path.join(home_dir, '.credentials')

    # flow = client.flow_from_clientsecrets(
    #     credential_dir + '\client_secrets.json',
    #     scope=SCOPES,
    #     redirect_uri='http://www.example.com/oauth2callback')
    # flow.params['access_type'] = 'offline'         # offline access
    # flow.params['include_granted_scopes'] = True   # incremental auth
    # auth_uri = flow.step1_get_authorize_url()
    # auth_code = redirect(auth_uri)
    # credentials = flow.step2_exchange(auth_code)
    # return credentials


def main(fname, folder_id, IMAGE_SOURCE):
    """Creates a Google Drive API service object"""
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
