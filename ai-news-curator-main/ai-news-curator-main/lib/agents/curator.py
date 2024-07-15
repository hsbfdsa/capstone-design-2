from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


class Article(BaseModel):
    """Information about a related article"""
    date: str = Field(description="The date of the article")
    title: str = Field(description="The title of the article")
    body: str = Field(description="The body of the article")
    url: str = Field(description="The URL of the article")
    image: str = Field(description="The image of the article")
    source: str = Field(description="The source of the article")

class ArticleList(BaseModel):
    """List of articles"""
    articles: list[Article] = Field(description="List of articles")
        

class CuratorAgent:
    def __init__(self):
        self.llm = ChatOpenAI()
        
        self.prompt_dict = {
            "dev": "You're a machine learning engineer interested in new AI models or papers. Pick top 5 news article you're most interested in from the following list: {context}",
        }
    
    def select_preferred_article(self, prompt, trending_articles):
        curate_prompt = PromptTemplate.from_template(prompt)
        
        curate_chain = curate_prompt | self.llm | StrOutputParser()

        return curate_chain.invoke({"context": trending_articles})
    
    
    def get_related_articles(self, curate_response, trending_articles):
        find_prompt = PromptTemplate.from_template("Your task is to find top 5 news article among those provided below that is most relevant to the following sentence. {sentence}. Here are the news articles: {context}")
        
        find_chain = find_prompt | self.llm.with_structured_output(ArticleList)
        
        return find_chain.invoke({"sentence": curate_response, "context": trending_articles})
    
    def run(self, search_result):
        curate_response = self.select_preferred_article(self.prompt_dict["dev"], search_result["trending_articles"])
        related_articles = self.get_related_articles(curate_response, search_result["trending_articles"])
        
        return {
            "curate_response": curate_response,
            "related_articles": related_articles
        }
