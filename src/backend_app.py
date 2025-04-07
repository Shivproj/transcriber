import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import aiofiles
import uvicorn
import math 

# --- Add pydub ---
from pydub import AudioSegment


# FastAPI Backend
app = FastAPI()

# Set the upload directory
UPLOAD_DIRECTORY = os.environ.get("Upload_dir", "uploaded_files")
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """Handles file uploads and returns duration."""
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        async with aiofiles.open(file_location, "wb") as f:
            content = await file.read()
            await f.write(content)
        audio = AudioSegment.from_file(file_location)
        duration_seconds = len(audio) / 1000
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
            
            
        return JSONResponse(
            content={"filename": file.filename, "message": "File uploaded successfully","audio_length":f"{hours}h {minutes}m {seconds}s","audio_length_seconds": int(duration_seconds)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


# @app.post("/process_audio/")
# async def process_audio(filename: str, start_time: float, end_time: float):
#     """Processes the audio file to trim it based on start and end times."""
#     file_path = os.path.join(UPLOAD_DIRECTORY, filename)
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     try:
#         # Load the audio file
#         audio = AudioSegment.from_file(file_path)

#         # Trim the audio
#         start_ms = int(start_time * 1000)  # Convert seconds to milliseconds
#         end_ms = int(end_time * 1000)  # Convert seconds to milliseconds
#         trimmed_audio = audio[start_ms:end_ms]

#         # Save the processed audio
#         processed_file_path = os.path.join(UPLOAD_DIRECTORY, f"processed_{filename}")
#         trimmed_audio.export(processed_file_path, format="mp3")

#         return JSONResponse(
#             content={"processed_file_url": f"/download/{os.path.basename(processed_file_path)}"}
#         )
#     except CouldntDecodeError:
#         raise HTTPException(status_code=400, detail="Could not decode the audio file")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")
