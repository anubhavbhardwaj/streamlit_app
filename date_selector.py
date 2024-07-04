# import streamlit as st
import re
# from datetime import datetime





import streamlit as st
import os
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

# # Set the default date to the latest available date
# available_dates = get_available_dates()
# default_date = max(available_dates) if available_dates else None

# st.title('Folder Contents Viewer')

def select_date(available_dates, default_date):
    if available_dates:
        # Create a date picker
        selected_date = st.sidebar.date_input('Pick a date', value=default_date, min_value=min(available_dates), max_value=max(available_dates))

        # Format the selected date to match the desired format "6-03-24"
        selected_date_str = selected_date.strftime('%m-%d-%y')

        parts = selected_date_str.split('-')  # Split into parts: [month, day, year]

        # Remove leading zero from month if present
        parts[0] = parts[0].lstrip('0')

        # Recombine into desired format
        formatted_date_str = '-'.join(parts)
        return formatted_date_str


        # List files and folders in the selected folder
        # contents = list_files_and_folders(formatted_date_str)

        # # Display the files and folders
        # st.write(f'Contents of folder {selected_date_str}:')
        # for item in contents:
        #     st.write(item)
    else:
        st.write('No folders available')






























# def date_selector(filtered_files, delimiter, key):
#     if filtered_files:
#         # Extract dates from the filenames
#         dates = []
#         for file in filtered_files:
#             # Assuming the filenames are in the format "mm-dd-yy-c.xlsx"
#             base_name = file.split(delimiter)[0]
#             try:
#                 date_obj = datetime.strptime(base_name, "%m-%d-%y")
#                 dates.append(date_obj)
#             except ValueError:
#                 st.write(f"Filename {file} does not match the expected format 'mm-dd-yy-c.xlsx'")
#         # Sort the dates for the date selector
#         dates.sort()


#         # Streamlit date input
#         selected_date = st.sidebar.date_input('Select Date:', value=dates[-1], min_value=dates[0], max_value=dates[-1], key=key)
#         # Check if the selected date corresponds to an available file
#         selected_date_str = selected_date.strftime("%m-%d-%y")
#         formatted_date_str = f"{selected_date.month}-{selected_date.day}-{selected_date.strftime('%y')}"
#         selected_file = next((file for file in filtered_files if formatted_date_str in file), None)
#         if selected_file:
#             col1, col2 = st.columns([1,4])
#             with col1:
#                 # st.success(f"Selected file: {selected_file}")
#                 pass
#             with col2:
#                 pass
#             return selected_file
#         else:
#             st.warning("No file found for the selected date.")
#     else:
#         st.warning("No files ending with '-c' found in the 'records' folder.")



def date_selector_multiple_files(filtered_files, selected_date, key):
    if filtered_files:
        dates = []

        for file in filtered_files:
            # Define your patterns
            patterns = ['-p', '-cc', '-c']

            # Create a regular expression pattern by joining all patterns with '|'
            pattern = '|'.join(re.escape(p) for p in patterns)

            # Split the file name using the pattern
            base_name = re.split(pattern, file)[0].strip('-')

            try:
                date_obj = datetime.strptime(base_name, "%m-%d-%y")
                dates.append(date_obj)
            except ValueError:
                print(f"Filename {file} does not match the expected format 'mm-dd-yy-p.xlsx', 'mm-dd-yy-cc.xlsx', or 'mm-dd-yy-c.xlsx'.")

        # Sort the dates for the date selector
        dates.sort()

        # Streamlit date input
        # selected_date = st.sidebar.date_input('Select Date:', value=dates[0], min_value=dates[0], max_value=dates[-1])
        selected_date = selected_date

        # Check if the selected date corresponds to an available file
        formatted_date_str = selected_date.strftime("%m-%d-%y")
        formatted_date_str_alt = f"{selected_date.month}-{selected_date.day}-{selected_date.strftime('%y')}"

        # Filter files for the selected date
        selected_files = [file for file in filtered_files if formatted_date_str in file or formatted_date_str_alt in file]

        # Filter further to only include files that end with '-c', '-cc', or '-p'
        selected_files = [file for file in selected_files if file.endswith(('-c.xlsx', '-cc.xlsx', '-p.xlsx'))]

        if selected_files:
            # st.success(f"Selected files for {selected_date}: {selected_files}")
            return selected_files
        else:
            st.warning(f"No files ending with '-c', '-cc', or '-p' found for {selected_date}.")
    else:
        st.warning("No files ending with '-c', '-cc', or '-p' found.")



# Function to extract the last part
def extract_last_part(file_name, keywords):
    for keyword in keywords:
        if keyword in file_name:
            return keyword
    return None