import json

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchAPIWrapper

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.agents import AgentFinish, AgentActionMessageLog


class Article(BaseModel):
    """Information about a related article"""
    date: str = Field(description=f"The date of the article formatted as yyyy-mm-dd")
    title: str = Field(description="The title of the article")
    body: str = Field(description="The body of the article")
    url: str = Field(description="The URL of the article")
    image: str = Field(description="The image of the article")
    source: str = Field(description="The source of the article")


class Response(BaseModel):
    """Final response to the question being asked."""
    articles: list[Article] = Field(description="List of articles")


@tool
def search_news(query):
    """Search news articles using search engine."""
    search_engine = DuckDuckGoSearchAPIWrapper(time="w")
    return [json.dumps(article) for article in search_engine._ddgs_news(query=query, max_results=50)]


class BasicRagAgent:
    def __init__(self):
        self.tools = [search_news, Response]
        
    def parse(self, output):
        if "function_call" not in output.additional_kwargs:
            return AgentFinish(return_values={"output": output.content}, log=output.content)

        function_call = output.additional_kwargs["function_call"]
        name = function_call["name"]
        inputs = json.loads(function_call["arguments"])

        if name == "Response":
            return AgentFinish(return_values=inputs, log=str(function_call))
        else:
            return AgentActionMessageLog(
                tool=name, tool_input=inputs, log="", message_log=[output]
            )
    
    def run_newsletter(self, topic, num_articles, interests):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a newsletter writer. Please write a well-written newsletter, using a friendly and engaging tone, on topics closely related to what users are interested in."),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
        )
        
        agent = create_tool_calling_agent(llm, [search_news], prompt)

        agent_executor = AgentExecutor(tools=[search_news], agent=agent, verbose=True)
        
        return agent_executor.invoke(
            {"input": f"Please tell me about the top {num_articles} {topic}-related news stories. Especially, I'm interested in {interests}"},
            return_only_outputs=True,
        )
        
    def run_structured(self, topic, num_articles, interests):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a newsletter writer. Please write a well-written newsletter, using a friendly and engaging tone, on topics closely related to what users are interested in."),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125",
            temperature=0,
        )

        llm_with_tools = llm.bind_functions(self.tools)

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | self.parse
        )

        agent_executor = AgentExecutor(tools=[search_news], agent=agent, verbose=True)
        
        return agent_executor.invoke(
            {"input": f"Please tell me about the top {num_articles} {topic}-related news stories. Especially, I'm interested in {interests}"},
            return_only_outputs=True,
        )