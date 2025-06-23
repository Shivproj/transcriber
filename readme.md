# 🎙️ The Transcriber: Your AI-Powered Audio Transcription Tool

**Unlock the power of your audio with The Transcriber!** This tool provides a seamless way to upload, trim, and transcribe audio files with high accuracy. Leveraging advanced AI models, The Transcriber excels at generating English transcriptions, even for audio containing a mix of English and Indian languages. Say goodbye to manual transcription and hello to efficiency!

## ✨ Key Features

* **Effortless Audio Upload:** Easily upload your MP3 or WAV audio files for processing.
* **Precise Audio Trimming:** Select the exact audio segment you need with an intuitive slider interface. No more transcribing unnecessary parts!
* **Accurate AI Transcription:** Benefit from high-quality English transcriptions powered by cutting-edge AI, capable of handling mixed-language audio.
* **Intelligent Speaker Labeling:** Automatically identifies and labels speakers as "Moderator" (M) and "Responder" (R) for clear and organized transcripts.
* **Convenient Downloadable Transcriptions:** Export your transcriptions as `.docx` files for easy sharing and editing.
* **User-Friendly Interface:** Enjoy a seamless experience with the intuitive Streamlit frontend.
* **Robust Backend:** Rely on the FastAPI backend for efficient file handling, audio processing, and transcription tasks.

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed and configured:

* **Python:** Version 3.11.3.
* **Virtual Environment (Recommended):** Helps isolate project dependencies.
* **Google GenAI API Key:** Required for accessing the transcription service.
* **FFMPEG:** An additional dependency required for audio processing.

## 🚀 Installation: Get Started in Minutes!

Follow these simple steps to get The Transcriber up and running on your machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Shivproj/transcriber.git
   cd transcriber
   ```

2. **Create and Activate a Virtual Environment:**

   * **Linux/macOS:**
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
   * **Windows:**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   * **Copy the Example File:**
     ```bash
     cp .env.example .env
     ```
   * **Edit `.env`:** Open the `.env` file and fill in your Google GenAI API key and the desired backend URL (if different from the default):
     ```
     GENAI_API_KEY=YOUR_GOOGLE_GENAI_API_KEY
     FASTAPI_URL=http://127.0.0.1:7400
     ```

5. **Alternatively on Windows:**
   Create a shortcut on the desktop and map it to the `.bat` file. Enjoy!

## 🛠️ Usage: Transcribe Your Audio

Here's how to use The Transcriber:

### 1. Start the Backend

1. Navigate to the `src` directory:
   ```bash
   cd src
   ```

2. Run the FastAPI backend:
   ```bash
   uvicorn backend_app:app --host 127.0.0.1 --port 7400 --reload
   ```
   Keep this terminal window open while using the frontend.

### 2. Start the Frontend

1. Open a **new** terminal window.
2. Run the Streamlit app:
   ```bash
   streamlit run src/frontend_app.py
   ```

3. Your browser will automatically open the Streamlit app (usually at `http://localhost:8501`). If not, open your browser and navigate to this address.

### 3. Transcribe Your Audio

1. **Upload Audio:** Drag and drop your MP3 or WAV file into the designated area, or click to select it from your file system.
2. **Trim Audio:** Once uploaded, an audio player with a slider will appear. Use the handles on the slider to select the desired start and end points of the audio you want to transcribe.
3. **Transcribe:** Click the **"Transcribe"** button below the audio player. The backend will process your audio and generate the transcription.
4. **Download Transcription:** Once the transcription is complete, a **"Download Transcription as DOCX"** button will appear. Click it to save the transcribed text to your computer.

## 📂 File Structure

```
transcriber/
├── .env.example          # Example environment variables
├── .gitignore            # Ignored files and directories
├── requirements.txt      # Python dependencies
├── readme.md             # Project documentation
├── src/                  # Source code
│   ├── __init__.py       # Package initialization
│   ├── frontend_app.py   # Streamlit frontend
│   ├── backend_app.py    # FastAPI backend
```

## ⚠️ Troubleshooting

Encountering issues? Here are some common problems and their solutions:

* **Backend Connection Error:**
  * **Solution:** Ensure the FastAPI backend is running in its terminal window. Double-check that the `FASTAPI_URL` in your `.env` file matches the host and port where the backend is running (default: `http://127.0.0.1:7400`).
* **Missing API Key:**
  * **Solution:** Verify that you have correctly set your Google GenAI API key in the `.env` file.
* **Dependency Issues:**
  * **Solution:** If you encounter errors related to missing packages, try running the dependency installation command again:
    ```bash
    pip install -r requirements.txt
    ```
    Make sure your virtual environment is activated.
* **System Performance Issues:** 
  * **Solution:** Increase the timeouts if your system is slower.

## 🤝 Contributing

We welcome contributions! If you have ideas for improvements, bug fixes, or new features, feel free to:

* Open an issue to discuss your ideas.
* Submit a pull request with your changes.

Love y'all famnig

---
