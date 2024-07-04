import streamlit as st
# from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import requests
import os
import pickle
import pandas as pd
import json
from googleapiclient.http import MediaIoBaseDownload


# Define the scope
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_google_drive_access(folder_id, creds):
    if creds:
        record_folder_path = check_create_record_folder()
        st.write(record_folder_path)
        return list_folders(creds, folder_id)

# Function to get the credentials
def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Access credentials stored in Streamlit secrets
            credentials_info = {
                "client_id": st.secrets["gcp_credentials"]["client_id"],
                "project_id": st.secrets["gcp_credentials"]["project_id"],
                "auth_uri": st.secrets["gcp_credentials"]["auth_uri"],
                "token_uri": st.secrets["gcp_credentials"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["gcp_credentials"]["auth_provider_x509_cert_url"],
                "client_secret": st.secrets["gcp_credentials"]["client_secret"],
                "redirect_uris": st.secrets["gcp_credentials"]["redirect_uris"],
            }
            
            # Create a temporary file from the credentials dictionary
            with open('gcp_credentials.json', 'w') as temp_file:
                json.dump({
                    "installed": credentials_info
                }, temp_file)


            flow = InstalledAppFlow.from_client_secrets_file('gcp_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

            # Remove the temporary file after use
            os.remove('credentials.json')

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


            

# Function to list folders in a specific Google Drive folder
def list_folders(creds, folder_id):
    service = build('drive', 'v3', credentials=creds)
    query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(
        q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items




def download_file(service, file_id, file_path):
    request = service.files().get_media(fileId=file_id)
    with open(file_path, 'wb') as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            # st.spinner("Download In Progress")
            # st.write(f"Download {int(status.progress() * 100)}%.")

# Function to download an entire folder from Google Drive
def download_folder(service, folder_id, destination):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])

    for item in items:
        file_path = os.path.join(destination, item['name'])
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            download_folder(service, item['id'], file_path)
        else:
            # download_file(service, item['id'], file_path)
            download_file_with_retry(service, item['id'], file_path)



def download_file_with_retry(service, file_id, file_path, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            download_file(service, file_id, file_path)
            return
        except Exception as e:
            retries += 1
            st.write(f"Error downloading {file_id}. Retrying {retries}/{max_retries}. Error: {e}")
    st.write(f"Failed to download {file_id} after {max_retries} retries.")











# Function to download a specific folder
def download_specific_folder(creds, folder_id, folder_name):
    service = build('drive', 'v3', credentials=creds)
    destination = check_create_record_folder()
    folder_path = os.path.join(destination, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    download_folder(service, folder_id, folder_path)
    st.write(f"Downloaded folder: {folder_name} to {folder_path}")




# Main function to handle the downloading of all folders
def download_all_folders(creds, root_folder_id, destination):
    service = build('drive', 'v3', credentials=creds)
    folders = list_folders(creds, root_folder_id)
    st.title("All Folders")
    st.write(folders)

    
    for folder in folders:
        folder_path = os.path.join(destination, folder['name'])
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        download_folder(service, folder['id'], folder_path)

        st.write(f"Downloaded folder: {folder['name']} while folder path is {folder_path}")



# Function to load data from Google Drive
def load_data_from_gdrive(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
        return pd.read_excel(file_name)
    else:
        st.error("Failed to fetch data from Google Drive.")
        return None



def check_create_record_folder():
    # Root directory path
    root_directory = ''

    # Folder name to check
    folder_name = 'records'

    # Construct the full path of the folder
    folder_path = os.path.join(root_directory, folder_name)

    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder if it doesn't exist
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created successfully in {root_directory}")
    else:
        print(f"Folder '{folder_name}' already exists in {root_directory}")
    
    return folder_path


# Function to list Excel files in a specific Google Drive folder
def list_excel_files(creds, folder_id):
    service = build('drive', 'v3', credentials=creds)
    query = f"'{folder_id}' in parents and (mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')"
    results = service.files().list(
        q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return items


# Function to create download link
def create_download_link(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"











# def list_excel_files_and_folders(creds, folder_id):
#     service = build('drive', 'v3', credentials=creds)
#     query = f"'{folder_id}' in parents and (mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or mimeType='application/vnd.google-apps.folder')"
#     results = service.files().list(
#         q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
#     items = results.get('files', [])
#     return items