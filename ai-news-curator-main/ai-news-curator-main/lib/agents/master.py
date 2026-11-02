from langgraph.graph import Graph

from lib.agents import SearchAgent, CuratorAgent, EditorAgent


class MasterAgent:
    def __init__(self):
        self.search_agent = SearchAgent()
        self.curator_agent = CuratorAgent()
        self.editor_agent = EditorAgent()

        workflow = Graph()

        workflow.add_node("search", self.search_agent.run)
        workflow.add_node("curate", self.curator_agent.run)
        workflow.add_node("edit", self.editor_agent.run)

        workflow.add_edge("search", "curate")
        workflow.add_edge("curate", "edit")

        workflow.set_entry_point("search")
        workflow.set_finish_point("edit")

        self.chain = workflow.compile()

    def run(self, topic, num_articles=5, interests="", time="1 Week"):
        return self.chain.invoke({
            "query": topic,
            "time": time,
            "interests": interests,
            "num_articles": num_articles,
        })

    def run_newsletter(self, topic, num_articles, interests):
        state = self.run(topic, num_articles, interests)
        lines = [f"# {topic} Newsletter", ""]
        for i, a in enumerate(state["newsletter"], 1):
            lines += [
                f"## {i}. {a['title']}",
                a["summary"],
                f"- {a.get('source', '')} · {a.get('date', '')[:10]} · 관심 {a['votes']}명 ({', '.join(a['voters'])})",
                f"- {a['url']}",
                "",
            ]
        return "\n".join(lines)
