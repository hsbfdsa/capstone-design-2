import json

from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchAPIWrapper
    

class SearchAgent:
    def __init__(self):
        self.time_dict = {
            "1 Day": "d",
            "1 Week": "w",
            "1 Month": "m"
        }
    
    def get_news_from_search_engine(self, query, time):
        
        search_engine = DuckDuckGoSearchAPIWrapper(time=self.time_dict[time])
        return [json.dumps(article) for article in search_engine._ddgs_news(query=query, max_results=15)]
        
    def run(self, state):
        # 그래프의 다른 노드와 같은 형식으로 state(dict)를 받아 필드를 추가해서 넘긴다
        return {
            **state,
            "trending_articles": self.get_news_from_search_engine(state["query"], state.get("time", "1 Week")),
        }
        
        