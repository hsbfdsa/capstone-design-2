from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter


class Outline(BaseModel):
    """Outline of the article"""
    image: str = Field(description="The image of the article. If not available, then print it unknown")
    summary: str = Field(description="The summary of the article")
    url: str = Field(description="The URL of the article") 


class EditorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125",
            temperature=0,
        )
        
        self.prompt = ChatPromptTemplate.from_template(
            """You are a very good assistant that summarizes online articles.

        Here's the article you want to summarize.

        ==================
        title: {title}
        body : {body}
        ==================

        Write a summary of the previous article.:
        You must write summary in Korean.

        {text} {image}"""
        )
        
        self.chain = self.prompt | self.llm.with_structured_output(Outline)
               
    
    def summarize_articles(self, results):
        samples = results["related_articles"]
        sample = samples[0]
        
        loader = WebBaseLoader(sample.url)
        text_splitter = CharacterTextSplitter(        
            separator="\n\n",
            chunk_size=3000,     
            chunk_overlap=300,   
            length_function=len,
            is_separator_regex=False,
        )
        docs = loader.load_and_split(text_splitter)    
            
        return self.chain.invoke(
            {
                "title": sample.title, 
                "body": sample.body,
                "text": docs[0],
                "image": sample.image,
            }
        )
    
    def run(self, results):
        return self.summarize_articles(results)