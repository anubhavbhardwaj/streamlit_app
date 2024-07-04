import streamlit as st
from google_drive_logic import *


# Main function to get Google Drive access and download folders
def get_google_drive_access(date_options,folder_id, creds):
    if creds:
        record_folder_path = check_create_record_folder()
        st.write(record_folder_path)
        download_all_folders(creds, folder_id, record_folder_path)

























# def get_google_drive_access(date_options,folder_id, creds):
#     if creds:
#         subfolders = list_folders(creds, folder_id)
#         st.write(subfolders)
        # if not subfolders:
        #     st.write('No subfolders found.')
        # else:
        #     st.write('Subfolders:')
        #     for folder in subfolders:
        #         folder_name = folder['name']


        #         date_options.append(folder_name)
        #         excel_files = list_excel_files(creds, folder['id'])
        #         if not excel_files:
        #             st.write(f"No Excel files found in {folder['name']}.")
        #         else:
        #             st.write(f"Excel files in {folder['name']}:")
        #             for file in excel_files:
        #                 gdrive_url = create_download_link(file['id'])
        #                 data = load_data_from_gdrive(gdrive_url, f"records/{file['name']}")
        #                 if data is not None:
        #                     pass
        #                     # st.write(f"Data from {folder['name']}:")
        #                     # st.write(f"Data from {file['name']}:")
        #                     # st.dataframe(data)