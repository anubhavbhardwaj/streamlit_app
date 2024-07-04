import os
import pandas as pd
import traceback
import streamlit as st


# def manage_record_of_all(folder_name):
#     # Root directory path
#     root_directory = '/'  # Update with your actual root directory path
#     # Folder name to check
#     folder_name = f'records/{folder_name}'
#     # List all files in the folder
#     file_names = os.listdir(folder_name)
#     # Filter files that end with '-p'
#     filtered_files = list(filter(lambda file: '.xlsx' in file.lower(), file_names))
#     # Display the file names
#     if filtered_files:
#         print("### Files ending with '-p' in the 'records' folder:")
#         for file in filtered_files:
#             print(file)
#     else:
#         print("No files ending with '-p' found in the 'records' folder.")

#     return filtered_files











def manage_record_of_p(folder_name):
    try:
        # Root directory path
        root_directory = '/'  # Update with your actual root directory path
        # Folder name to check
        folder_name = f'records/{folder_name}'
        # List all files in the folder
        file_names = os.listdir(folder_name)
        # Filter files that end with '-p'
        filtered_files = list(filter(lambda file: '-p' in file.lower() and '-pic' not in file.lower(), file_names))
        # Display the file names
        if filtered_files:
            print("### Files ending with '-p' in the 'records' folder:")
            for file in filtered_files:
                print(file)
        else:
            print("No files ending with '-p' found in the 'records' folder.")

        return filtered_files
    except:
        pass

def manage_record_of_c(folder_name):
    try:
        # Root directory path
        root_directory = '/'  # Update with your actual root directory path
        # Folder name to check
        folder_name = f'records/{folder_name}'
        # List all files in the folder
        file_names = os.listdir(folder_name)
        # Filter files that end with '-p'
        filtered_files = list(filter(lambda file: '-c' in file.lower() and '-cc' not in file.lower(), file_names))

        # Display the file names
        if filtered_files:
            print("### Files ending with '-c' in the 'records' folder:")
            for file in filtered_files:
                print(file)
        else:
            print("No files ending with '-c' found in the 'records' folder.")

        return filtered_files
    except:
        pass

def manage_record_of_cc(folder_name):
    try:
        # Root directory path
        root_directory = '/'  # Update with your actual root directory path
        # Folder name to check
        folder_name = f'records/{folder_name}'
        # List all files in the folder
        file_names = os.listdir(folder_name)
        # Filter files that end with '-p'
        filtered_files = list(filter(lambda file: '-cc' in file.lower(), file_names))

        # Display the file names
        if filtered_files:
            print("### Files ending with '-cc' in the 'records' folder:")
            for file in filtered_files:
                print(file)
        else:
            print("No files ending with '-cc' found in the 'records' folder.")

        return filtered_files
    except:
        pass