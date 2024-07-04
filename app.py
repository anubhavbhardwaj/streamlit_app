import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from streamlit_plotly_events import plotly_events
from PIL import Image
import requests
from io import BytesIO


import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from streamlit_plotly_events import plotly_events
from PIL import Image
import os

import streamlit as st
import rasterio
from rasterio.plot import show
from tempfile import NamedTemporaryFile
import os
import matplotlib.pyplot as plt


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
from PIL import Image
import io


import streamlit as st
from fontTools.ttLib import TTFont
import os


import rasterio
from rasterio.plot import show
from tempfile import NamedTemporaryFile
import os
import matplotlib.pyplot as plt
import pyproj
import plotly.express as px
from PIL import Image
import streamlit as st
from PIL import Image

import streamlit as st
from PIL import Image

st.title('Display .tiff Image in Streamlit')

# # Path to the .tiff image
# tiff_image_path = 'OIG.tif'

# try:
#     # Load the .tiff image using Pillow
#     tiff_image = Image.open(tiff_image_path)

#     # Convert the image to RGB mode if it’s in a mode not directly displayable
#     if tiff_image.mode not in ('RGB', 'RGBA'):
#         if 'I;16' in tiff_image.mode or 'I' in tiff_image.mode:
#             # Scale the 16-bit image to 8-bit per channel
#             tiff_image = tiff_image.point(lambda i: i * (1./256)).convert('RGB')
#         else:
#             tiff_image = tiff_image.convert('RGB')

#     # Display the image in Streamlit
#     st.image(tiff_image, caption='This is a .tiff image displayed in Streamlit', use_column_width=True)

# except Exception as e:
#     st.error(f"Error loading image: {e}")




data = pd.DataFrame({
    'x': ['A', 'B', 'C', 'A', 'B', 'C'],
    'y': ['1', '1', '1', '2', '2', '2'],
    'value': [10, 20, 30, 40, 50, 60]
})


fig = go.Figure(data=go.Heatmap(
                   z=data['value'],
                   x=data['x'],
                   y=data['y'],
                   colorscale='Viridis',
                   colorbar=dict(title='Values'),
                   hoverongaps=False))


fig.update_layout(
    title='Customized Heatmap',
    xaxis_title='X Axis',
    yaxis_title='Y Axis',
    plot_bgcolor='rgba(0,0,0,0)'
)

clicked_points = plotly_events(fig, click_event=True, hover_event=False, select_event=False, key="heatmap")


def display_images(x, y):
    st.write(f"Displaying images for box: x={x}, y={y}")
    images = [
        "OIP.jpg",
    ]
    
    converted_images = []
    for image_path in images:
        with Image.open(image_path) as img:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            converted_images.append(buf)

    st.image(converted_images, caption=[img_path for img_path in images], width=250)


if clicked_points:
    point = clicked_points[0]
    x = point['x']
    y = point['y']
    display_images(x, y)
else:
    st.write("Click on a box in the heatmap to display images")


















# uploaded_file = st.file_uploader("Upload TIFF file", type=["tif", "tiff"])

# if uploaded_file is not None:
#     # Create a temporary file to save the uploaded file
#     with NamedTemporaryFile(delete=False, suffix=".tif") as tmp:
#         tmp.write(uploaded_file.getvalue())
#         tmp_path = tmp.name

#     with rasterio.open(tmp_path) as src:
#         st.write(f"Number of bands: {src.count}")
#         st.write(f"Width: {src.width}")
#         st.write(f"Height: {src.height}")
        
#         st.subheader("Visualizing the TIFF file")

























# data = pd.DataFrame({
#     'x': ['A', 'B', 'C', 'A', 'B', 'C'],
#     'y': ['1', '1', '1', '2', '2', '2'],
#     'value': [10, 20, 30, 40, 50, 60]
# })


# fig = go.Figure(data=go.Heatmap(
#                    z=data['value'],
#                    x=data['x'],
#                    y=data['y'],
#                    colorscale='Viridis',  # Change the color scale
#                    colorbar=dict(title='Values'),
#                    hoverongaps=False))

# fig.update_layout(
#     title='Customized Heatmap',
#     xaxis_title='X Axis',
#     yaxis_title='Y Axis',
#     plot_bgcolor='rgba(0,0,0,0)'
# )

# clicked_points = plotly_events(fig, click_event=True, hover_event=False, select_event=False, key="heatmap")

# def display_images(x, y):
#     st.write(f"Displaying images for box: x={x}, y={y}")
#     images = [
#         "C4_01_1_1_GFP_001.tif",
#         "C4_01_1_1_GFP_001.tif",
#         "C4_01_1_1_GFP_001.tif"
#     ]

#     images = []
#     for file in images:
#         image = Image.open(file)
#         images.append(image)

#     st.image(images, width=150)


# if clicked_points:
#     point = clicked_points[0]
#     x = point['x']
#     y = point['y']
#     display_images(x, y)

# else:
#     st.write("Click on a box in the heatmap to display images")





















# data = pd.DataFrame({
#     'x': ['A', 'B', 'C', 'A', 'B', 'C'],
#     'y': ['1', '1', '1', '2', '2', '2'],
#     'value': [10, 20, 30, 40, 50, 60]
# })


# fig = px.density_heatmap(data, x='x', y='y', z='value', text_auto=True)

# clicked_points = plotly_events(fig, click_event=True, hover_event=False, select_event=False, key="heatmap")

# def display_emojis(x, y):
#     st.write(f"Displaying emojis for box: x={x}, y={y}")
#     st.markdown("😀 😃 😄")

# if clicked_points:
#     point = clicked_points[0]
#     x = point['x']
#     y = point['y']
#     display_emojis(x, y)

# else:
#     st.write("Click on a box in the heatmap to display emojis")



