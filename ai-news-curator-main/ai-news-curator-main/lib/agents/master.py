import os
from langgraph.graph import Graph

from agents import SearchAgent, CuratorAgent, EditorAgent


class MasterAgent:
    def __init__(self):
        pass
        
    def run(self, topic):
        
        search_agent = SearchAgent(os.getenv("SERP_API_KEY"))
        curator_agent = CuratorAgent()
        editor_agent = EditorAgent()
        
        workflow = Graph()
        
        workflow.add_node("search", search_agent.run)
        workflow.add_node("curate", curator_agent.run)
        workflow.add_node("edit", editor_agent.run)
        
        workflow.add_edge("search", "curate")
        workflow.add_edge("curate", "edit")
        
        workflow.set_entry_point("search")
        workflow.set_finish_point("edit")
        
        chain = workflow.compile()
        
        return chain.invoke(topic)
    
