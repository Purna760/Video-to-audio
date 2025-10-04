import streamlit as st
import moviepy.editor as mp
import io
import os
import tempfile

def main():
    """
    Main function for the Streamlit app.
    Handles video upload, audio extraction, and audio download.
    """
    st.title("Audio Extractor from Video")
    st.write("Upload a video file to extract its audio.")

    # Task 1: Upload a video
    uploaded_file = st.file_uploader("Choose a video file (.mp4)", type=["mp4"])

    if uploaded_file is not None:
        st.video(uploaded_file, format='video/mp4')
        
        # Display a status message
        st.info("Extracting audio... Please wait.")
        
        try:
            # Task 2: Extract audio
            # Create a temporary file to save the uploaded video
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
                temp_video_file.write(uploaded_file.read())
                temp_video_path = temp_video_file.name
            
            # Load the video clip from the temporary file
            video_clip = mp.VideoFileClip(temp_video_path)
            
            # Create an in-memory buffer for the audio
            audio_buffer = io.BytesIO()
            video_clip.audio.write_audiofile(audio_buffer, codec='mp3')
            
            # Reset the buffer's position to the beginning
            audio_buffer.seek(0)
            
            # Clean up the temporary video file
            os.remove(temp_video_path)
            
            # Display success message
            st.success("Audio extracted successfully!")

            # Task 3: Download audio
            st.subheader("Download Audio")
            st.download_button(
                label="Download Audio as MP3",
                data=audio_buffer,
                file_name=os.path.splitext(uploaded_file.name)[0] + ".mp3",
                mime="audio/mpeg"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

