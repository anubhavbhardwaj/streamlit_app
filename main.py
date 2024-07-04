import streamlit as st

from google_drive_logic import *




from plots import heatMap, whiskerPlot, whiskerPlot_for_all

from records import manage_record_of_p
from records import manage_record_of_c
from records import manage_record_of_cc

from date_selector import *
from google_drive_logic import *



# https://drive.google.com/drive/folders/1_2C9QwYtAtcv9hxL15zZQv5Xz70uIGkt
# https://stackoverflow.com/questions/62374432/displaying-images-when-hovering-over-point-in-plotly-scatter-plot-in-python


def trend_func(dropdown_1, dropdown_2):
        current_directory = os.getcwd()
        records_folder = os.path.join(current_directory, 'records')
        # Check if the records_folder exists and is a directory
        if os.path.exists(records_folder) and os.path.isdir(records_folder):
            # st.write(f"The 'records' folder is located at: {records_folder}")
            # List all directories within the records_folder
            directories = [d for d in os.listdir(records_folder) if os.path.isdir(os.path.join(records_folder, d))]
            if directories:
                # st.write("The following subfolders and their '-cc' Excel files are found in the 'records' folder:")
                for directory in directories:
                    subfolder_path = os.path.join(records_folder, directory)
                    # st.write(f"Subfolder: {directory}")
                    # List all Excel files in the current subfolder that contain "-cc"
                    excel_files = list_excel_files(dropdown_1, subfolder_path)
                    if excel_files:
                        for excel_file in excel_files:
                            if dropdown_1 == "Cell Count":
                                title = f"Cell Count {directory}"
                            elif dropdown_1 == "Circularity":
                                title = f"Circularity {directory}"
                            elif dropdown_1 == "Perimeter":
                                title = f"Perimeter {directory}"
                                
                            color_dict = {
                                        1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                        2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                        3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                        }
                            selected_file = excel_files[0]
                            whiskerPlot(selected_file, dropdown_2, title, directory, color_dict, col=None)
                    else:
                        st.write("  No '-cc' Excel files found in this subfolder.")
            else:
                st.write("There are no subfolders in the 'records' folder.")
        else:
            st.write("The 'records' folder does not exist in the current directory.")



# Function to list all Excel files in a given directory
def list_excel_files(dropdown_1, directory):
    if dropdown_1 == "Cell Count":
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.xls', '.xlsx')) and "-cc" in f]
    elif dropdown_1 == "Circularity":
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.xls', '.xlsx')) and "-c" in f]
    elif dropdown_1 == "Perimeter":
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(('.xls', '.xlsx')) and "-p" in f]




def main():
    st.set_page_config(layout="wide")
    check_create_record_folder()
    folder_id = st.secrets["credentials"]["FOLDER_ID"]
    save_button = st.sidebar.checkbox("Save Record From Drive", key="Save_Record")
    trend      = st.sidebar.checkbox("Trend")
    date_options = []
    creds = get_credentials()
    if creds and save_button:
        folders = get_google_drive_access(folder_id, creds)
        st.title("All Folders")

        for folder in folders:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(folder['name'])
            with col2:
                if st.button("Download", key=folder['id']):
                    download_specific_folder(creds, folder['id'], folder['name'])


    if trend:
        options = [
            "Cell Count",
            "Circularity",
            "Perimeter"
        ]
        dropdown_1 = st.sidebar.selectbox("Choose an option:", options)

        if dropdown_1 == "Cell Count":
            mole_options = [
            "None",
            "0 μM",
            "0.1 μM",
            "1 μM"
            ]
            dropdown_2 = st.sidebar.selectbox("Choose an option:", mole_options)
            trend_func(dropdown_1, dropdown_2)

        elif dropdown_1 == "Circularity":
            mole_options = [
            "None",
            "0 μM",
            "0.1 μM",
            "1 μM"
            ]
            dropdown_2 = st.sidebar.selectbox("Choose an option:", mole_options)
            trend_func(dropdown_1 ,dropdown_2)

        elif dropdown_1 == "Perimeter":
            mole_options = [
            "None",
            "0 μM",
            "0.1 μM",
            "1 μM"
            ]
            dropdown_2 = st.sidebar.selectbox("Choose an option:", mole_options)
            trend_func(dropdown_1 ,dropdown_2)
    else:
        options = [
            "None",
            "All",
            "Cell Count",
            "Circularity",
            "Perimeter"
        ]
        dropdown_1 = st.sidebar.selectbox("Choose an option:", options)    

        current_directory = os.getcwd()
        records_folder = os.path.join(current_directory, 'records')

        if os.path.exists(records_folder) and os.path.isdir(records_folder):
            print(f"The 'records' folder is located at: {records_folder}")
        else:
            print("The 'records' folder does not exist in the current directory.")


        if dropdown_1 == "None":
            pass

        elif dropdown_1 == "All":
            mole_options = [
            "None",
            "0 μM",
            "0.1 μM",
            "1 μM"
            ]
            dropdown_2 = st.sidebar.selectbox("Choose an option:", mole_options)
            available_dates = get_available_dates()
            selected_date   = max(available_dates) if available_dates else None
            if available_dates:
                folder_name = select_date(available_dates, selected_date)


            filtered_files_cc = manage_record_of_cc(folder_name)
            filtered_files_c  = manage_record_of_c(folder_name)
            filtered_files_p  = manage_record_of_p(folder_name)


            if filtered_files_cc == None and filtered_files_c == None and filtered_files_p == None :
                st.error(f"No Record Found For Selected Date {folder_name}")

            try:
                if filtered_files_cc:
                    title = "Cell Count"
                    selected_file = filtered_files_cc[0]
                    whiskerPlot_for_all(selected_file, dropdown_2, title, folder_name, col=None)
            except:
                pass

            try:
                if filtered_files_c:
                    title = "Circularity"
                    selected_file = filtered_files_c[0]
                    whiskerPlot_for_all(selected_file, dropdown_2, title, folder_name, col=None)                  
            except:
                pass
            try:
                if filtered_files_p:
                    title = "Perimeter"
                    selected_file = filtered_files_p[0]
                    whiskerPlot_for_all(selected_file, dropdown_2, title, folder_name, col=None)
            except:
                pass

        elif dropdown_1 == "Cell Count":
            treatment_options = [
            "With Treatment",
            "Without Treatment",
            ]
            dropdown_3 = st.sidebar.selectbox("Choose an option:", treatment_options)

            mole_options = [
            "None",
            "0 μM",
            "0.1 μM",
            "1 μM"
            ]
            dropdown_2 = st.sidebar.selectbox("Choose an option:", mole_options)
            
            available_dates = get_available_dates()
            selected_date   = max(available_dates) if available_dates else None
            if available_dates:
                folder_name = select_date(available_dates, selected_date)
            filtered_files_cc = manage_record_of_cc(folder_name)
            if not filtered_files_cc:
                st.error(f"No Record Found For Selected Date {folder_name}")

            image_with_heatmap = st.sidebar.checkbox("Images")
            if image_with_heatmap and filtered_files_cc:
                try:
                    if dropdown_2 == "None":
                        title = "Cell Count WhiskerPlot"
                        selected_file = filtered_files_cc[0]
                        heatMap(selected_file, dropdown_2, title, folder_name, col=None)
                    else:
                        title = "Cell Count WhiskerPlot"
                        selected_file = filtered_files_cc[0]
                        heatMap(selected_file, dropdown_2, title, folder_name, col=None)                        
                except:
                    pass
            elif not image_with_heatmap and dropdown_3 == "Without Treatment": 
                try:    
                    if dropdown_2 == "None":
                        col = [1,2,3,4,5,6,7,8,9,10,11,12]
                        title_1 = "Cell Count WhiskerPlot"
                        selected_file = filtered_files_cc[0]
                        color_dict = {
                                    1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                    2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                    3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                    }
                        whiskerPlot(selected_file, dropdown_2, title_1, folder_name,color_dict, col)
                    else:
                        color_dict = {
                                    1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                    2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                    3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                    }
                        title = "Cell Count WhiskerPlot"
                        selected_file = filtered_files_cc[0]
                        whiskerPlot(selected_file, dropdown_2, title, folder_name,color_dict, col=None)
                        heatMap(selected_file, dropdown_2, title, folder_name, col=None)
                except:
                    pass

            elif not image_with_heatmap and dropdown_3 == "With Treatment":
                try:    
                    if dropdown_2 == "None":
                        col1, col2, col3 = st.columns([1,2,3])
                        col = [1,2,3,4,5,6,7,8,9,10,11,12]
                        color_dict = {
                                        1: 'Group-1',  4: 'Group-2', 7: 'Group-3', 10: 'Group-4',
                                        2: 'Group-1',  5: 'Group-2', 8: 'Group-3', 11: 'Group-4',
                                        3: 'Group-1',  6: 'Group-2', 9: 'Group-3', 12: 'Group-4', 
                                        }
                        title_1 = "Cell Count WhiskerPlot"
                        selected_file = filtered_files_cc[0]
                        whiskerPlot(selected_file, dropdown_2, title_1, folder_name,color_dict, col)
                    else:
                        color_dict = {
                                    1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                    2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                    3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                    }
                        title = "Cell Count WhiskerPlot"
                        selected_file = filtered_files_cc[0]
                        whiskerPlot(selected_file, dropdown_2, title, folder_name,color_dict, col=None)
                except:
                    pass                

        elif dropdown_1 == "Circularity":
            treatment_options = [
            "With Treatment",
            "Without Treatment",
            ]
            dropdown_3 = st.sidebar.selectbox("Choose an option:", treatment_options)

            mole_options = [
            "None",
            "0 μM",
            "0.1 μM",
            "1 μM"
            ]
            dropdown_2 = st.sidebar.selectbox("Choose an option:", mole_options)

            available_dates = get_available_dates()
            selected_date   = max(available_dates) if available_dates else None
            if available_dates:
                folder_name = select_date(available_dates, selected_date)

            filtered_files_c  = manage_record_of_c(folder_name)
            

            if not filtered_files_c:
                st.error(f"No Record Found For Selected Date {folder_name}")

            if dropdown_3 == "Without Treatment":
                try:
                    if dropdown_2 == "None":
                        color_dict = {
                                    1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                    2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                    3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                    }
                        col = [1,2,3,4,5,6,7,8,9,10,11,12]
                        title_1 = "Circularity Group-1 WhiskerPlot"
                        selected_file = filtered_files_c[0]
                        whiskerPlot(selected_file, dropdown_2, title_1, folder_name,color_dict, col)                       
                    else:
                        color_dict = {
                                    1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                    2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                    3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                    }
                        title = "Circularity WhiskerPlot"
                        selected_file = filtered_files_c[0]
                        whiskerPlot(selected_file, dropdown_2, title, folder_name,color_dict, col=None)
                except:
                    pass

            elif dropdown_3 == "With Treatment": 
                try:
                    if dropdown_2 == "None":
                        col1, col2, col3 = st.columns([1,2,3])
                        color_dict = {
                                        1: 'Group-1',  4: 'Group-2', 7: 'Group-3', 10: 'Group-4',
                                        2: 'Group-1',  5: 'Group-2', 8: 'Group-3', 11: 'Group-4',
                                        3: 'Group-1',  6: 'Group-2', 9: 'Group-3', 12: 'Group-4', 
                                        }
                        col = [1,2,3,4,5,6,7,8,9,10,11,12]
                        title_1 = "Circularity WhiskerPlot"
                        selected_file = filtered_files_c[0]
                        whiskerPlot(selected_file, dropdown_2, title_1, folder_name,color_dict, col)
                        # with col1:
                        #     color_dict = {
                        #                 1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                        #                 2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                        #                 3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                        #                 }
                        #     col = [1,4,7,10]
                        #     title_1 = "Circularity Group-1 WhiskerPlot"
                        #     selected_file = filtered_files_c[0]
                        #     whiskerPlot(selected_file, dropdown_2, title_1, folder_name,color_dict, col)
                        # with col2:
                        #     color_dict = {
                        #                 1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                        #                 2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                        #                 3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                        #                 }   
                        #     col = [2,5,8,11]
                        #     title_2 = "Circularity Group-2 WhiskerPlot"
                        #     selected_file = filtered_files_c[0]
                        #     whiskerPlot(selected_file, dropdown_2, title_2, folder_name,color_dict, col)
                        # with col3:
                        #     color_dict = {
                        #                 1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                        #                 2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                        #                 3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                        #                 }
                        #     col = [3,6,9,12]
                        #     title_3 = "Circularity Group-3 WhiskerPlot"
                        #     selected_file = filtered_files_c[0]
                        #     whiskerPlot(selected_file, dropdown_2, title_3, folder_name,color_dict, col)                          
                    else:
                        color_dict = {
                                    1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                    2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                    3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                    }
                        title = "Circularity WhiskerPlot"
                        selected_file = filtered_files_c[0]
                        whiskerPlot(selected_file, dropdown_2, title, folder_name,color_dict, col=None)
                except:
                    pass


                
        elif dropdown_1 == "Perimeter":
            treatment_options = [
            "With Treatment",
            "Without Treatment",
            ]
            dropdown_3 = st.sidebar.selectbox("Choose an option:", treatment_options)
            mole_options = [
            "None",
            "0 μM",
            "0.1 μM",
            "1 μM"
            ]
            dropdown_2 = st.sidebar.selectbox("Choose an option:", mole_options)

            available_dates = get_available_dates()
            selected_date   = max(available_dates) if available_dates else None
            if available_dates:
                folder_name = select_date(available_dates, selected_date)

            filtered_files_p  = manage_record_of_p(folder_name)

            if not filtered_files_p:
                st.error(f"No Record Found For Selected Date {folder_name}")


            if dropdown_3 == "Without Treatment":
                try:
                    if dropdown_2 == "None":
                        color_dict = {
                                    1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                    2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                    3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                    }
                        col = [1,2,3,4,5,6,7,8,9,10,11,12]
                        title_1 = "Perimeter Group-1 WhiskerPlot"
                        selected_file = filtered_files_p[0]
                        whiskerPlot(selected_file, dropdown_2, title_1, folder_name,color_dict, col)                       
                    else:
                        color_dict = {
                                    1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                    2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                    3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                    }
                        title = "Perimeter WhiskerPlot"
                        selected_file = filtered_files_p[0]
                        whiskerPlot(selected_file, dropdown_2, title, folder_name,color_dict, col=None)
                except:
                    pass



            elif dropdown_3 == "With Treatment": 
                try:
                    if dropdown_2 == "None":
                        col1, col2, col3 = st.columns([1,2,3])
                        color_dict = {
                                        1: 'Group-1',  4: 'Group-2', 7: 'Group-3', 10: 'Group-4',
                                        2: 'Group-1',  5: 'Group-2', 8: 'Group-3', 11: 'Group-4',
                                        3: 'Group-1',  6: 'Group-2', 9: 'Group-3', 12: 'Group-4', 
                                        }
                        col = [1,2,3,4,5,6,7,8,9,10,11,12]
                        title_1 = "Perimeter WhiskerPlot"
                        selected_file = filtered_files_p[0]
                        whiskerPlot(selected_file, dropdown_2, title_1, folder_name,color_dict, col)
                        # with col1:
                        #     color_dict = {
                        #                 1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                        #                 2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                        #                 3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                        #                 }
                        #     col = [1,4,7,10]
                        #     title_1 = "Perimeter Group-1 WhiskerPlot"
                        #     selected_file = filtered_files_p[0]
                        #     whiskerPlot(selected_file, dropdown_2, title_1, folder_name,color_dict, col)
                        # with col2:
                        #     color_dict = {
                        #                 1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                        #                 2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                        #                 3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                        #                 }
                        #     col = [2,5,8,11]
                        #     title_2 = "Perimeter Group-2 WhiskerPlot"
                        #     selected_file = filtered_files_p[0]
                        #     whiskerPlot(selected_file, dropdown_2, title_2, folder_name,color_dict, col)
                        # with col3:
                        #     color_dict = {
                        #                 1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                        #                 2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                        #                 3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                        #                 }
                        #     col = [3,6,9,12]
                        #     title_3 = "Perimeter Group-3 WhiskerPlot"
                        #     selected_file = filtered_files_p[0]
                        #     whiskerPlot(selected_file, dropdown_2, title_3, folder_name,color_dict, col)                          
                    else:
                        color_dict = {
                                    1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                    2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                    3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                                    }
                        title = "Perimeter WhiskerPlot"
                        selected_file = filtered_files_p[0]
                        whiskerPlot(selected_file, dropdown_2, title, folder_name,color_dict, col=None)
                except:
                    pass


if __name__ == '__main__':
    main()