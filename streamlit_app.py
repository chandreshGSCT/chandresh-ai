from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key="AIzaSyDEkwXbCd30ye4GILxEtIWxKjzHd2uyKtk")

## Function to load OpenAI model and get respones

# def get_gemini_response(input,image,prompt):
#     model = genai.GenerativeModel('gemini-pro-vision')
#     response = model.generate_content([input,image[0],prompt])
#     return response.text

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,image[0],prompt])
    else:
       response = model.generate_content([input ,image[0],"tell me about this image"] )
    try:
        response_text = response.text
    except Exception as e:
        try:
            response_text = f"{response.parts} 🫣"
        except:
            # response_text = f"{response.candidates[0].content.parts[0].text} 🫣"
            response_text = f"""Sorry, I not give you answer!. check Image or check Input"""
    return response_text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app
st.set_page_config(
    page_title="Chandresh Patel.",
    page_icon="",
    # layout="wide"
)
st.text("Made by Chandresh Patel")
uploaded_files = st.file_uploader("અહીં તમારી બધી ઇમેજ અપલોડ કરો.", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

st.header("તમારી ઇમેજ માથી જોતું હોય તે અહીં લખો.")

input_text = st.text_input("Input Prompt: ",key="input")



# images = []

if uploaded_files is not None:
    for i , uploaded_file in enumerate(uploaded_files):
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Uploaded Image {i+1}", use_column_width=True)
        # images.append(image)


input_prompt = """
               You are an expert in understanding document or research paper.
               You will receive input images as document or research paper &
               you will have to answer questions based on the input image
               """


## If ask button is clicked
if uploaded_files:
    submit=st.button("Submit")
    if submit: 
        with st.spinner("Please Wait ... 🔄"):
            # st.caption("The Response are:")
            for i, image_data_r in enumerate(uploaded_files):
                image_data = input_image_setup(image_data_r)
                response=get_gemini_response(input_prompt,image_data,input_text)
                st.caption(f"Image {i+1} response: ")
                st.write(response)
