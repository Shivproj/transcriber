import streamlit as st
import requests
import os

# Backend API URLs
BACKEND_BASE_URL = "http://127.0.0.1:7400"
UPLOAD_URL = f"{BACKEND_BASE_URL}/uploadfile/"
PROCESS_URL = f"{BACKEND_BASE_URL}/process_audio/"
UPLOAD_DIRECTORY = os.environ.get("Upload_dir", "uploaded_files")

st.set_page_config(layout="wide")
st.title("Audio Trimmer")
st.write("Upload your MP3 or WAV file, select a range, and process it.")

def format_time(seconds):
    """Formats seconds into hh:mm:ss format."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Initialize session state variables
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "slider_values" not in st.session_state:
    st.session_state.slider_values = (0, 0)

if "audio_length_seconds" not in st.session_state:
    st.session_state.audio_length_seconds = 0

if "audio_uploaded" not in st.session_state:
    st.session_state.audio_uploaded = False

if "transcribe_clicked" not in st.session_state:
    st.session_state.transcribe_clicked = False

# Callback function for the "Transcribe" button
def transcribe_audio():
    st.session_state.transcribe_clicked = True

# Step 1: Upload Audio
st.subheader("1. Upload Audio")
uploaded_file = st.file_uploader(
    "Choose an audio file (MP3 or WAV)",
    type=["mp3", "wav"],
    key="file_uploader",
)

if uploaded_file is not None and not st.session_state.audio_uploaded:
    st.session_state.uploaded_file = uploaded_file  # Save the uploaded file in session state
    with st.spinner("Uploading and analyzing audio..."):
        try:
            files = {
                "file": (
                    st.session_state.uploaded_file.name,
                    st.session_state.uploaded_file.getvalue(),
                    st.session_state.uploaded_file.type,
                )
            }
            response = requests.post(UPLOAD_URL, files=files, timeout=60)

            if response.status_code == 200:
                response_data = response.json()
                st.session_state.audio_length_seconds = int(response_data["audio_length_seconds"])
                st.session_state.slider_values = (0, st.session_state.audio_length_seconds)
                st.session_state.audio_uploaded = True
                st.success(f"Audio uploaded successfully! Length: {response_data['audio_length']}")
            else:
                st.error(f"Failed to upload audio: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: Could not connect to the backend at {UPLOAD_URL}. Is it running? Details: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred during upload: {str(e)}")

# Step 2: Select Start and End Points
def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def parse_time(time_str):
    try:
        parts = time_str.strip().split(":")
        parts = [int(p) for p in parts]
        while len(parts) < 3:
            parts.insert(0, 0)
        h, m, s = parts
        return h * 3600 + m * 60 + s
    except:
        return None

if st.session_state.audio_uploaded:
    st.subheader("2. Enter Start and End Points")

    total_seconds = st.session_state.audio_length_seconds

    # Default values: start=0, end=audio_length
    default_start = format_time(0)
    default_end = format_time(total_seconds)

    # Text input boxes with defaults
    start_time_str = st.text_input(
        "Start time (HH:MM:SS):",
        value=default_start,
        key="start_time_input"
    )
    end_time_str = st.text_input(
        "End time (HH:MM:SS):",
        value=default_end,
        key="end_time_input"
    )

    start_time = parse_time(start_time_str)
    end_time = parse_time(end_time_str)

    # Clamp values safely without popping errors
    if start_time is None:
        start_time = 0
    else:
        start_time = max(0, min(start_time, total_seconds))

    if end_time is None:
        end_time = total_seconds
    else:
        end_time = max(0, min(end_time, total_seconds))

    if start_time > end_time:
        st.warning("Start time is after end time. Adjust if needed.")

    st.session_state.slider_values = (start_time, end_time)

    # Display selected range and duration
    selected_duration_seconds = end_time - start_time
    st.write(f"Selected range: Start = {format_time(start_time)}, End = {format_time(end_time)}")
    st.markdown(
        f"<h2 style='text-align: center; color: green;'>Selected Duration: {format_time(selected_duration_seconds)}</h2>",
        unsafe_allow_html=True,
    )

    # Transcribe button
    st.button("Transcribe", on_click=transcribe_audio, type="secondary")

    # Step 3: Transcription
    if st.session_state.transcribe_clicked:
        with st.spinner("Transcribing audio..."):
            try:
                payload = {
                    "filename": st.session_state.uploaded_file.name,
                    "start_time": start_time,
                    "end_time": end_time,
                }
                response = requests.post(PROCESS_URL, json=payload, timeout=360)

                if response.status_code == 200:
                    transcription_content = response.content
                    st.download_button(
                        label="Download Transcription",
                        data=transcription_content,
                        file_name="transcription.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                    st.success("Transcription completed successfully! You can download the file.")
                else:
                    st.error(f"Failed to process audio: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: Could not connect to the backend at {PROCESS_URL}. Is it running? Details: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred during transcription: {str(e)}")

        st.session_state.transcribe_clicked = False