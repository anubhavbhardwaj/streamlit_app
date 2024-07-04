import streamlit as st
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os
import requests
import pandas as pd

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

# Function to list all files and folders recursively in a Google Drive folder
def list_all_files_and_folders(creds, folder_id):
    service = build('drive', 'v3', credentials=creds)

    all_files = []
    
    # Recursive function to retrieve all files and folders
    def retrieve_files(folder_id):
        query = f"'{folder_id}' in parents"
        results = service.files().list(
            q=query, fields="files(id, name, mimeType)").execute()
        items = results.get('files', [])

        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Recursively call retrieve_files for subfolders
                all_files.extend(retrieve_files(item['id']))
            else:
                all_files.append(item)

        return all_files

    return retrieve_files(folder_id)

# Function to create download link
def create_download_link(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# Function to load data from Google Drive
def load_data_from_gdrive(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
        return pd.read_excel(file_name)
    else:
        st.write("Failed to fetch data from Google Drive.")
        return None

# Example usage:
def main():
    creds = get_credentials()
    folder_id = 'your_folder_id_here'
    files_and_folders = list_all_files_and_folders(creds, folder_id)
    
    for item in files_and_folders:
        if 'name' in item:
            st.write(f"Name: {item['name']}, ID: {item['id']}, Type: {item['mimeType']}")
            if item['mimeType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                gdrive_url = create_download_link(item['id'])
                data = load_data_from_gdrive(gdrive_url, f"records/{item['name']}")
                if data is not None:
                    st.write(f"Data from {item['name']}:")
                    st.write(data)

if __name__ == '__main__':
    main()
