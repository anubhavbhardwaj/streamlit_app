import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from PIL import Image
from streamlit_plotly_events import plotly_events
import os



def heatMap(selected_file, dropdown_2, title, folder_name, col=None):
    try:
        if dropdown_2 == "None":
            # data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9])
            data = pd.read_excel(f"records/{folder_name}/{selected_file}")
        elif dropdown_2 == "0 μM":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[1, 4, 7, 10])
        elif dropdown_2 == "0.1 μM":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[2, 5, 8, 11])
        elif dropdown_2 == "1 μM":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[3, 6, 9, 12])
    except:
        pass

    # Convert the folder name to the desired format
    parts = folder_name.split('-')
    if len(parts[2]) == 2:  # Assuming year is in 2-digit format
        parts[2] = "20" + parts[2]  # Convert to 4-digit year
    formatted_folder_name = '-'.join(parts)

    try:
        if data.columns[0] == "Unnamed: 0":
            data.rename(columns={"Unnamed: 0": "Label"}, inplace=True)

        data = data.iloc[:, :-1]
        data.iloc[:, 1:] = data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
        data = data.dropna(axis=1 ,how="all")
        data = data.dropna(how="any")
        if data.empty:
            st.write("No Numeric columns to create heatmap.")
        else:
            column_names = data.iloc[:, 1:].columns.tolist()
            data_selected = data.iloc[:, 1:]

            labels = data['Label']

            # Sort labels in descending order
            data_selected = data_selected.loc[labels.sort_values(ascending=False).index]
            labels = labels.sort_values(ascending=False)


            fig = go.Figure(data=go.Heatmap(
                            z=data_selected,
                            x=column_names,
                            y=labels,
                            colorscale='Viridis',
                            colorbar=dict(title=title),
                            hoverongaps=False))

            fig.update_layout(
                title='Customized Heatmap',
                xaxis_title='Columns',
                yaxis_title='',
                plot_bgcolor='rgba(0,0,0,0)'  
            )
            col1, col2 = st.columns([3,1])
            with col1:
                clicked_points = plotly_events(fig, click_event=True, hover_event=False, select_event=False, key="heatmap")
            with col2:
                if clicked_points:
                    point = clicked_points[0]
                    x = point['x']
                    y = point['y']
                    display_images(x, y, folder_name, formatted_folder_name)
                else:
                    st.write("Click on a box in the heatmap to display images")
    except:
        st.error(f"Data Not in Valid Format for selected file {selected_file}")




def display_images(x, y, folder_name, formatted_folder_name):
    st.write(f"Displaying images for box: x={x}, y={y}")

    image_path = f"records/{folder_name}/{formatted_folder_name}-pictures-4"
    image_name_1 = f"Read 1_GFP 469,525+Read 1_CY5 628,685+Read 1_Bright Field_{y}{x}_1_001.png"
    image_name_2 = f"Read 1_Bright Field+Read 1_CY5 628,685+Read 1_GFP 469,525_{y}{x}_1_001.png"

    # Read 1_Bright Field+Read 1_CY5 628,685+Read 1_GFP 469,525_A4_1_001  ---> 17
    # Read 1_Bright Field+Read 1_CY5 628,685+Read 1_GFP 469,525_A3_1_001  ---> 18

    # Read 1_GFP 469,525+Read 1_CY5 628,685+Read 1_Bright Field_A2_1_001  ---> 16
    # Read 1_GFP 469,525+Read 1_CY5 628,685+Read 1_Bright Field_A3_1_001  ---> 19
    # Read 1_GFP 469,525+Read 1_CY5 628,685+Read 1_Bright Field_A3_1_001  ---> 22
    # Read 1_GFP 469,525+Read 1_CY5 628,685+Read 1_Bright Field_A3_1_001  ---> 23
    # Read 1_GFP 469,525+Read 1_CY5 628,685+Read 1_Bright Field_A3_1_001  ---> 24
    # Read 1_GFP 469,525+Read 1_CY5 628,685+Read 1_Bright Field_A3_1_001  ---> 25

    # Read 1_GFP 469,525+Read 1_CY5 628,685+Read 1_Bright Field_A2_1_001  ---> 25


    full_image_path_1 = os.path.join(image_path, image_name_1)
    full_image_path_2 = os.path.join(image_path, image_name_2)
    if os.path.exists(full_image_path_1):
        image(full_image_path_1)
    elif os.path.exists(full_image_path_2):
        image(full_image_path_2)
    else:
        st.write(f"The image does not exist.")


def image(full_image_path):
        image = Image.open(full_image_path)
        fig = go.Figure()
        fig.add_layout_image(
            dict(
                source=image,
                xref="x",
                yref="y",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                opacity=1,
                layer="below")
        )
        fig.update_xaxes(
            visible=False,
            range=[0, 1]
        )
        fig.update_yaxes(
            visible=False,
            range=[0, 1],
            scaleanchor="x"
        )
        fig.update_layout(
            width=400,
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig)



def whiskerPlot(selected_file, dropdown_2, title, folder_name,color_dict, col):
    try:
        if dropdown_2 == "None":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=col)
        elif dropdown_2 == "0 μM":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[1, 4, 7, 10])
        elif dropdown_2 == "0.1 μM":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[2, 5, 8, 11])
        elif dropdown_2 == "1 μM":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[3, 6, 9, 12])

    except:
        st.error(f"Could not read file: {selected_file}")
        return

    try:
        data = data.apply(pd.to_numeric, errors='coerce')
        data = data.dropna(how='all')
        numeric_data = data.select_dtypes(include=['number'])
        if numeric_data.empty:
            st.write("No numeric columns to create box plot.")
        else:
            group_size = 1
            num_columns = len(numeric_data.columns)
            grouped_data = []
            for i in range(0, num_columns, group_size):
                group_columns = numeric_data.columns[i:i + group_size]
                group_df = numeric_data[group_columns]
                melted_group_df = group_df.melt(var_name='Variable', value_name='Value')
                melted_group_df['Columns'] = ','.join(map(str, group_columns))
                grouped_data.append(melted_group_df)
            long_data = pd.concat(grouped_data, ignore_index=True)
            long_data['color'] = long_data['Variable'].copy()
            long_data['color'] = long_data['Variable'].replace(color_dict)
            fig = px.box(long_data, x='Columns', y='Value', points="all", title=title, color='color')
            fig.update_layout(
                width=1300,
                height=800
            )
            st.plotly_chart(fig)
    except:
        st.error(f"Data Not in Valid Format for selected file {selected_file}")



def whiskerPlot_for_all(selected_file, dropdown_2, title, folder_name, col):
    try:
        if dropdown_2 == "None":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=col)
        elif dropdown_2 == "0 μM":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[1, 4, 7, 10])
        elif dropdown_2 == "0.1 μM":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[2, 5, 8, 11])
        elif dropdown_2 == "1 μM":
            data = pd.read_excel(f"records/{folder_name}/{selected_file}", usecols=[3, 6, 9, 12])
    except :
        st.error(f"Could not read file: {selected_file}")
        return

    try:
        data = data.apply(pd.to_numeric, errors='coerce')
        data = data.dropna(how='all')
        numeric_data = data.select_dtypes(include=['number'])
        if numeric_data.empty:
            st.write("No numeric columns to create box plot.")
        else:
            group_size = 1
            num_columns = len(numeric_data.columns)
            grouped_data = []
            
            for i in range(0, num_columns, group_size):
                group_columns = numeric_data.columns[i:i + group_size]
                group_df = numeric_data[group_columns]
                melted_group_df = group_df.melt(var_name='Variable', value_name='Value')
                melted_group_df['Columns'] = ','.join(map(str, group_columns))
                grouped_data.append(melted_group_df)

 
            long_data = pd.concat(grouped_data, ignore_index=True)
            long_data['color'] = long_data['Variable'].copy()
            replace_dict = {
                                1: 'Group-1',  4: 'Group-1', 7: 'Group-1', 10: 'Group-1',
                                2: 'Group-2',  5: 'Group-2', 8: 'Group-2', 11: 'Group-2',
                                3: 'Group-3',  6: 'Group-3', 9: 'Group-3', 12: 'Group-3', 
                            }
            long_data['color'] = long_data['Variable'].replace(replace_dict)
            fig = px.box(long_data, x='Columns', y='Value', points="all", title=title, color='color')
            fig.update_layout(
                width=1300,
                height=800
            )
            st.plotly_chart(fig)
    except:
        st.error(f"Data Not in Valid Format for selected file {selected_file}")



