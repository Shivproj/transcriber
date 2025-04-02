from fastapi import FastAPI, File, UploadFile, HTTPException
import os
import aiofiles

app = FastAPI()


UPLOAD_DIRECTORY = os.environ.get("Upload_dir", "uploaded_files")

@app.get("/")
def read_root():
    return {"message": "Welcome to the File Uploader API"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        async with aiofiles.open(file_location, "wb") as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    
    return {"filename": file.filename, "message": "File uploaded successfully"}