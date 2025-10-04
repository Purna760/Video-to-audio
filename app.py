import streamlit as st
import os
import tempfile
from moviepy.editor import VideoFileClip

# Task 1: Upload a video
st.title("Audio Extractor from Video")
st.write("Upload a video file (e.g., MP4) to extract its audio.")
uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video_file:
        tmp_video_file.write(uploaded_file.read())
        video_path = tmp_video_file.name

    st.video(uploaded_file)
    st.success("Video uploaded successfully!")

    # Task 2: Extract audio
    if st.button("Extract Audio"):
        try:
            # Create a temporary file for the extracted audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio_file:
                audio_path = tmp_audio_file.name

            # Use moviepy to extract audio
            with VideoFileClip(video_path) as video_clip:
                audio_clip = video_clip.audio
                audio_clip.write_audiofile(audio_path)
            
            st.success("Audio extracted successfully!")

            # Task 3: Download audio
            st.write("---")
            st.subheader("Download the Extracted Audio")
            
            # Read the audio file as bytes
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            st.download_button(
                label="Download Audio as MP3",
                data=audio_bytes,
                file_name="extracted_audio.mp3",
                mime="audio/mpeg"
            )

        except Exception as e:
            st.error(f"An error occurred during extraction: {e}")

        finally:
            # Clean up the temporary video and audio files
            if 'video_path' in locals() and os.path.exists(video_path):
                os.remove(video_path)
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)
