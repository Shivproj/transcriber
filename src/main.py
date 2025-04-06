import os
import requests
import streamlit as st
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
import uvicorn  # Only needed if running FastAPI separately

# FastAPI Backend
app = FastAPI()

# Set the upload directory
UPLOAD_DIRECTORY = os.environ.get("Upload_dir", "uploaded_files")
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """Handles file uploads."""
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        async with aiofiles.open(file_location, "wb") as f:
            content = await file.read()
            await f.write(content)
        return JSONResponse(
            content={"filename": file.filename, "message": "File uploaded successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


BACKEND_URL = "http://127.0.0.1:7400/uploadfile/"


# Streamlit Frontend
st.title("Transcriber")
st.write("Upload your file here.")
uploaded_file = st.file_uploader("Choose a file", type=["png", "pdf", "mp3", "wav"])


if uploaded_file is not None:
    with st.spinner("Uploading file..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(BACKEND_URL, files=files)

            if response.status_code == 200:
                st.success(f"File uploaded successfully: {response.json()['filename']}")
                duration_seconds = 50000
                st.write("Select the start and end points for the audio:")
                start_time, end_time = st.slider(
                    "Select a range (in seconds)",
                    0,
                    duration_seconds,
                    (0, duration_seconds),
                    step=1,
                )
                
                

            else:
                try:
                    error_message = response.json().get('detail', 'Unknown error')
                except:
                    error_message = f"Server returned status code: {response.status_code}"

                st.error(f"Failed to upload file: {error_message}")


        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while connecting to the backend: {str(e)}")


if __name__ == "__main__":
    pass 