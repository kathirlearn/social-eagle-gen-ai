import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0.5, 
    api_key=os.getenv("OPENAI_API_KEY"))

summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""
    You are an expert Summarizer.
    Here is a video Transcript:
    {transcript}
    Please generate a clear, concise summary of the main points and topics.
    """)

summary_chain = summary_prompt | llm

st.title("YouTube Video Summarizer")
video_url = st.text_input("Enter the YouTube video URL:")

def get_video_id(url):
    """
    Extract video Id from youtube URL
    """
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        query = parse_qs(parsed_url.query)
        return query.get("v", [None])[0]
    return None

if st.button("Summarize Video"):
    if not video_url.strip():
        st.warning("Please enter a YouTube video URL.")
    else:
        video_id = get_video_id(video_url)
        if not video_id:
            st.warning("Invalid YouTube URL. Please enter a valid URL.")
        else:
            with st.spinner("Fetching transcript and generating summary..."):
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    transcript = " ".join([entry['text'] for entry in transcript_list])
                    response = summary_chain.invoke({"transcript": transcript})
                    result = response.content if hasattr(response, "content") else str(response)
                    st.subheader("Video Summary")
                    st.write(result)
                except Exception as e:
                    st.error(f"Error fetching transcript: {e}")


