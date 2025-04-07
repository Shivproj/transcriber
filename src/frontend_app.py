import streamlit as st
import requests
import os

BACKEND_BASE_URL = "http://127.0.0.1:7400"
UPLOAD_URL = f"{BACKEND_BASE_URL}/uploadfile/"
PROCESS_URL = f"{BACKEND_BASE_URL}/process_audio/"
UPLOAD_DIRECTORY = os.environ.get("Upload_dir", "uploaded_files")

st.set_page_config(layout="wide")
st.title("Audio Trimmer")
st.write("Upload your MP3 or WAV file, select a range, and process it.")

# Helper function to format time in hours, minutes, and seconds
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

# Initialize session state for uploaded file, slider values, and audio metadata
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "slider_values" not in st.session_state:
    st.session_state.slider_values = (0, 0)

if "audio_length_seconds" not in st.session_state:
    st.session_state.audio_length_seconds = 0

if "audio_uploaded" not in st.session_state:
    st.session_state.audio_uploaded = False

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
                st.session_state.audio_uploaded = True  # Mark as uploaded
                st.success(f"Audio uploaded successfully! Length: {response_data['audio_length']}")
            else:
                st.error(f"Failed to upload audio: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: Could not connect to the backend at {UPLOAD_URL}. Is it running? Details: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred during upload: {str(e)}")

# Step 2: Select Start and End Points
if st.session_state.audio_uploaded:
    st.subheader("2. Select Start and End Points")
    total_seconds = st.session_state.audio_length_seconds

    # Create a list of formatted time labels for the slider
    time_labels = [format_time(i) for i in range(total_seconds + 1)]

    # Slider for selecting start and end points (with custom labels)
    start_time, end_time = st.select_slider(
        "Select the range to trim the audio:",
        options=list(range(total_seconds + 1)),  # Use seconds as the underlying values
        value=st.session_state.slider_values,
        format_func=lambda x: time_labels[x],  # Map seconds to formatted time
        key="audio_slider",
    )

    # Update session state with slider values
    st.session_state.slider_values = (start_time, end_time)

    # Convert slider values to hours:minutes:seconds format
    start_time_formatted = format_time(start_time)
    end_time_formatted = format_time(end_time)

    # Calculate the selected duration
    selected_duration_seconds = end_time - start_time
    selected_duration_formatted = format_time(selected_duration_seconds)

    # Display the selected range in formatted time

    # Display the selected duration in large font
    st.markdown(
        f"<h2 style='text-align: center; color: green;'>Selected Duration: {selected_duration_formatted}</h2>",
        unsafe_allow_html=True,
    )