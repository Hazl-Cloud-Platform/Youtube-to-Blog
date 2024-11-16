import streamlit as st
import os
from src.video_info import GetVideo
from src.model import Model
from src.prompt import Prompt
from src.misc import Misc
from src.db_handler import DatabaseHandler
from st_copy_to_clipboard import st_copy_to_clipboard

st.set_page_config(
    page_title="YouTube to Blog by HAZL",
    layout="wide",
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            .stDeployButton {
                    visibility: hidden;
                }
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


class YouTubeToBlog:
    def __init__(self):
        self.youtubeUrl = None
        self.videoId = None
        self.videoTitle = None
        self.videoTranscript = None
        self.blogPost = None
        self.col1 = None
        self.col2 = None
        self.db = DatabaseHandler()
        
        if 'openai_api_key' not in st.session_state:
            apiKey = self.db.get_api_key()
            if apiKey:
                st.session_state['openai_api_key'] = apiKey

    def setup_sidebar(self):
        with st.sidebar:
            st.title("Settings")
            apiKey = st.text_input("Enter OpenAI API Key", 
                                value=st.session_state.get('openai_api_key', ''),
                                type="password")
            
            if st.button("Save API Key"):
                self.db.save_api_key(apiKey)
                st.session_state['openai_api_key'] = apiKey
                st.success("API key saved successfully!")

    def check_api_key(self):
        if 'openai_api_key' not in st.session_state or not st.session_state['openai_api_key']:
            st.warning("Please enter your OpenAI API key in the sidebar.", icon="⚠️")
            return False
        return True

    def get_youtube_info(self):
        self.youtubeUrl = st.text_input("Enter YouTube Video Link")
        
        if self.youtubeUrl:
            self.videoId = GetVideo.Id(self.youtubeUrl)
            if self.videoId is None:
                st.write("**Error**")
                st.image("https://i.imgur.com/KWFtgxB.png", use_column_width=True)
                st.stop()
            self.videoTitle = GetVideo.title(self.youtubeUrl)
            st.write(f"**{self.videoTitle}**")
            st.image(f"http://img.youtube.com/vi/{self.videoId}/0.jpg", use_column_width=True)

    def generate_blog_post(self):
        if not self.check_api_key():
            return
        
        if st.button(":rainbow[**Generate Blog Post**]"):
            self.videoTranscript = GetVideo.transcript(self.youtubeUrl)
            blogPrompt = """Create a well-structured blog post from this video transcript. 
            The blog post should:
            1. Have an engaging title
            2. Include an introduction
            3. Break down the main points into sections with subheadings
            4. Include a conclusion
            5. Use proper formatting with markdown
            6. Maintain a professional yet conversational tone
            7. Include relevant quotes from the video where appropriate
            
            Format the blog post in markdown."""
            
            self.blogPost = Model.openai_chatgpt(
                transcript=self.videoTranscript, 
                prompt=blogPrompt
            )
            
            st.markdown("## Generated Blog Post:")
            st.markdown(self.blogPost)
            
            # Download and copy options
            st.download_button(
                label="Download Blog Post", 
                data=self.blogPost, 
                file_name=f"Blog-{self.videoTitle}.md"
            )
            st_copy_to_clipboard(self.blogPost)

    def run(self):
        st.title("YouTube to Blog Converter")
        
        self.setup_sidebar()
        self.col1, padding_col, self.col2 = st.columns([1, 0.1, 1])
        
        with self.col1:
            self.get_youtube_info()

        ranLoader = Misc.loaderx()
        n, loader = ranLoader[0], ranLoader[1]

        with self.col2:
            with st.spinner(loader[n]):
                self.generate_blog_post()
        
        st.write(Misc.footer(), unsafe_allow_html=True)


if __name__ == "__main__":
    app = YouTubeToBlog()
    app.run() 