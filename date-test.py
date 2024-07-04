import os
import streamlit as st
from datetime import datetime

# Update with your actual root directory path
root_directory = 'records'

def list_folder_contents(folder_path):
    contents = []
    if os.path.exists(folder_path):
        for entry in os.scandir(folder_path):
            if entry.is_file():
                contents.append(entry.name)  # Add file name
            elif entry.is_dir():
                contents.append(entry.name + '/')  # Add folder name with '/'
    return contents

# Function to list all files and folders inside the selected date folder
def list_files_and_folders(selected_date_str):
    folder_path = os.path.join(root_directory, selected_date_str)
    contents = list_folder_contents(folder_path)
    return contents

# Get the available dates from the folder names
def get_available_dates():
    folder_names = os.listdir(root_directory)
    dates = []
    for folder_name in folder_names:
        try:
            date = datetime.strptime(folder_name, '%m-%d-%y')
            dates.append(date)
        except ValueError:
            # Ignore folders that don't match the expected date format
            continue
    return sorted(dates)

# Set the default date to the latest available date
available_dates = get_available_dates()
default_date = max(available_dates) if available_dates else None

st.title('Folder Contents Viewer')


if available_dates:
    # Create a date picker
    selected_date = st.date_input('Pick a date', value=default_date, min_value=min(available_dates), max_value=max(available_dates))

    # Format the selected date to match the desired format "6-03-24"
    selected_date_str = selected_date.strftime('%m-%d-%y')

    parts = selected_date_str.split('-')  # Split into parts: [month, day, year]

    # Remove leading zero from month if present
    parts[0] = parts[0].lstrip('0')

    # Recombine into desired format
    formatted_date_str = '-'.join(parts)



    # List files and folders in the selected folder
    contents = list_files_and_folders(formatted_date_str)

    # Display the files and folders
    st.write(f'Contents of folder {selected_date_str}:')
    for item in contents:
        st.write(item)
else:
    st.write('No folders available')
