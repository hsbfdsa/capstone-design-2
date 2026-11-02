from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter


class Summary(BaseModel):
    """Summary of the article"""
    summary: str = Field(description="The summary of the article in Korean")


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

        Write a summary of the previous article in 3 sentences.
        Use only facts in the article. You must write summary in Korean.

        {text}"""
        )

        self.chain = self.prompt | self.llm.with_structured_output(Summary)
        self.text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=3000,
            chunk_overlap=300,
            length_function=len,
            is_separator_regex=False,
        )

    def load_text(self, url):
        docs = WebBaseLoader(url).load_and_split(self.text_splitter)
        return docs[0].page_content if docs else ""

    def summarize(self, article):
        try:
            text = self.load_text(article["url"])
        except Exception as e:
            # 원문을 못 가져오면 검색 결과의 짧은 본문으로 요약
            print(f"[editor] load failed {article['url']}: {e}")
            text = ""

        summary = self.chain.invoke({
            "title": article["title"],
            "body": article.get("body", ""),
            "text": text,
        }).summary
        return {**article, "summary": summary}

    def run(self, state):
        # 선택된 기사 전부 요약 (이전에는 첫 번째 기사만 요약했음)
        newsletter = [self.summarize(a) for a in state["selected"]]
        return {**state, "newsletter": newsletter}
