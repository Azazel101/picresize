import streamlit as st
import io
from PIL import Image
import base64
import uuid
import re


st.set_page_config(
    page_title = 'Image Resize',
    page_icon = '😇'
)

def get_image_download_link(img, quality=50, resolution=0.5, filename=None):

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;

            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """
    
    buffered = io.BytesIO()
    if not img.mode == 'RGB':
        img = img.convert('RGB')
    size = [int(resolution * s) for s in img.size]
    img = img.resize(size)
    img.save(buffered, format="JPEG", quality=quality)

    name = 'comp_' + str(filename)

    st.write('Compressed file : ')
    st.write({"FileName" : name,
            "Resolution": size,
            "FileSize": str(round(buffered.tell() / 1000,2)) + 'Kb'
            })
    img_str = base64.b64encode(buffered.getvalue()).decode()

    href = custom_css + f'<a download="{name}" id="{button_id}" href="data:file/jpg;base64,{img_str}"> Download </a>'
    return href

st.header("Image Resize")
fileUpload = st.file_uploader("Choose a file", type = ['jpg','jpeg', 'png'])

if fileUpload is not None:
    file = fileUpload.read()
    result = Image.open(fileUpload)
    file_details = {"FileName" : fileUpload.name, "FileType": fileUpload.type,"FileSize": str(round(fileUpload.size / 1000,2)) + 'Kb' , "Resolution": result.size}

    quality = st.slider('Select image quality (%)', 5, 100, (50))
#    resolution = st.slider('Select resolution', round(result.width * 0.1), result.width,(round(result.width / 2)))
    resolution = st.slider('Select resolution (%)', 10, 100,(50))
    resolution = resolution / 100
    st.write('Original file : ')
    st.write(file_details)
#    st.image(result, width = 200)

    st.markdown(get_image_download_link(result,quality, resolution, fileUpload.name), unsafe_allow_html=True)