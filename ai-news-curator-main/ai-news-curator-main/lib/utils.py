import time

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def translate_to_korean(text):
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    prompt = PromptTemplate.from_template("Translate the following text to Korean while keeping the markdown formatting. {input}")
    chain = prompt | llm | StrOutputParser()
    return chain.stream({"input": text})


def stream_data(text):
  for word in text.split(" "):
    yield word + " "
    time.sleep(0.02)
    
    