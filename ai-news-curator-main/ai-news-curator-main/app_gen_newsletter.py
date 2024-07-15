import os
import streamlit as st

from lib.baseline.direct_gen import DirectGenAgent
from lib.utils import translate_to_korean, stream_data


openai_api_key = os.getenv("OPENAI_API_KEY")  

st.set_page_config(page_title="Demo", layout="wide")
st.title("AAI Capstone Team 6 Demo")

language = st.radio(
  "Choose language",
  ["Korean", "English"],
)

with st.form("my_form"):
  col1, col2 = st.columns(2)
  with col1:
    topic = st.text_area("Enter keyword:", "AI, LLM")
  with col2:
    interests = st.text_area("Interests: (optional)", "Newly released models")  
  
  num_articles = st.slider("Number of articles", 3, 10, 5)
  
  submitted = st.form_submit_button("Submit")
  
  if submitted and openai_api_key.startswith("sk-"):
    news_curator_agent = DirectGenAgent()
    
    with st.spinner("Searching..."):
      response = news_curator_agent.run_newsletter(topic, num_articles, interests)
      
    if language == "English":
        st.write_stream(stream_data(response))
    else:
        st.write_stream(translate_to_korean(response))
        
    