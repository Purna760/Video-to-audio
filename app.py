import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile
import os

st.set_page_config(page_title="MoviePy Video Editor", page_icon="🎬", layout="wide")

st.title("🎬 MoviePy Video Editor on Streamlit")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    # Save uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_video_path = tmp_file.name

    st.video(temp_video_path)

    st.subheader("✂️ Trim Video")
    start_time = st.number_input("Start time (seconds)", min_value=0, value=0)
    end_time = st.number_input("End time (seconds)", min_value=10, value=10)

    if st.button("Trim and Download"):
        clip = VideoFileClip(temp_video_path).subclip(start_time, end_time)

        output_path = "output.mp4"
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        with open(output_path, "rb") as file:
            st.download_button("⬇️ Download Edited Video", file, file_name="edited_video.mp4")

        clip.close()

    # Cleanup
    os.remove(temp_video_path)
