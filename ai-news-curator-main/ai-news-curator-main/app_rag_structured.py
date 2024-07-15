import os
import streamlit as st

from lib.baseline.basic_rag import BasicRagAgent
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
  
  # if language == "English":
  #   duration = st.radio(
  #     "How long do you want the response to be?",
  #     ["Past 1 day", "Past 1 week", "Past 1 month"],
  #   )
  # else:
  #   duration = st.radio(
  #     "How long do you want the response to be?",
  #     ["지난 1일", "지난 1주", "지난 1개월"],
  #   )
  # st.write(f"{time}간 {topic} 관련 최신 뉴스를 가져옵니다.")
  num_articles = st.slider("Number of articles", 3, 10, 5)
  
  submitted = st.form_submit_button("Submit")
  
  if submitted and openai_api_key.startswith("sk-"):
    news_curator_agent = BasicRagAgent()
    
    with st.spinner("Searching..."):
      response = news_curator_agent.run_structured(topic, num_articles, interests)
    
    for article in response["articles"]:
      with st.container():
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
          try:
            st.image(article["image"])
          except:
            st.write("No image available")
        with col2:
          # ----------------------------------------------------------------------------------------------------
          # English version
          # ----------------------------------------------------------------------------------------------------
          if language == "English":
            st.write_stream(stream_data("##### " + article["title"] + "\n" + article["body"]))
            with st.expander("Read more"):
              st.write("Details here")
            col2_1, col2_2 = st.columns([3, 2])
            with col2_1:
              st.write(f"Source: {article['source']}")
              st.write(f"Published: {article['date']}")
            with col2_2:
              st.link_button("Go to link", article["url"])
          # ----------------------------------------------------------------------------------------------------
          # Korean version
          # ----------------------------------------------------------------------------------------------------
          else:
            st.write_stream(translate_to_korean("##### " + article["title"] + "\n" + article["body"]))
            with st.expander("자세히 보기"):
              st.write("여기에 세부 정보")
            col2_1, col2_2 = st.columns([3, 2])
            with col2_1:
              st.write(f"출처: {article['source']}")
              st.write(f"작성: {article['date']}")
            with col2_2:
              st.link_button("원문 기사 보기", article["url"])
                 
        
        