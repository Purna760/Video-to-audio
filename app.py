import streamlit as st
import os
from moviepy.editor import VideoFileClip
import tempfile

def extract_audio_from_video(video_path, audio_output_path):
    """
    Extracts audio from a video file and saves it as an MP3.
    """
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_output_path)
        video.close()
        return True
    except Exception as e:
        st.error(f"Error extracting audio: {e}")
        return False

st.title("Video to Audio Extractor")

# Task 1: Upload a video
st.subheader("1. Upload a Video")
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)

    # Save the uploaded video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
        temp_video_file.write(uploaded_file.read())
        video_path = temp_video_file.name

    st.success("Video uploaded successfully!")

    # Task 2: Extract audio
    st.subheader("2. Extract Audio")
    if st.button("Extract Audio"):
        audio_output_filename = "extracted_audio.mp3"
        audio_output_path = os.path.join(tempfile.gettempdir(), audio_output_filename)

        with st.spinner("Extracting audio..."):
            if extract_audio_from_video(video_path, audio_output_path):
                st.success("Audio extracted successfully!")
                
                # Task 3: Download audio
                st.subheader("3. Download Audio")
                with open(audio_output_path, "rb") as audio_file:
                    st.download_button(
                        label="Download Extracted Audio",
                        data=audio_file.read(),
                        file_name=audio_output_filename,
                        mime="audio/mp3"
                    )
            else:
                st.error("Audio extraction failed.")

    # Clean up temporary video file
    os.remove(video_path)
