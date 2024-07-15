from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class DirectGenAgent:
    def __init__(self):
        pass
        
    def run_newsletter(self, topic, num_articles, interests):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a newsletter writer. Please write a well-written newsletter, using a friendly and engaging tone, on topics closely related to what users are interested in."),
                ("user", "Please tell me about the top {num_articles} {topic}-related news. Especially, I'm interested in {interests}"),
            ]
        )

        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
        )

        chain = prompt | llm | StrOutputParser()
        
        return chain.invoke({"num_articles": num_articles, "topic": topic, "interests": interests})