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

def get_image_download_link(img, quality=50):

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
    img.save(buffered, format="JPEG", quality=quality)
    st.write(str(round(buffered.tell() / 1000,2)) + 'Kb')

    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = custom_css + f'<a download="compressed.jpg" id="{button_id}" href="data:file/jpg;base64,{img_str}">Download</a>'
    return href

st.header("Image Resize")
fileUpload = st.file_uploader("Choose a file", type = ['jpg','jpeg', 'png'])
quality = st.slider('Select image quality', 0, 100, (10))


if fileUpload is not None:
    file = fileUpload.read()
    result = Image.open(fileUpload)
    file_details = {"FileName" : fileUpload.name, "FileType": fileUpload.type, "Resolution": result.size}
    st.write(file_details)
    st.image(result, width = 200)

    st.markdown(get_image_download_link(result,quality), unsafe_allow_html=True)