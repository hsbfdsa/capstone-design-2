import json
from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


# 관점이 다른 가상 구독자. 여러 명이 같이 고른 기사일수록 화제성이 높다고 본다.
PERSONAS = {
    "dev": "You're a machine learning engineer interested in new AI models or papers.",
    "researcher": "You're an AI researcher who follows benchmarks, new architectures and research trends.",
    "journalist": "You're a tech journalist looking for news with broad social impact.",
    "pm": "You're a product manager interested in product launches, business deals and market changes.",
}


class Picks(BaseModel):
    """Articles picked by one subscriber"""
    indices: List[int] = Field(description="indices of the picked articles, most interesting first")


def format_articles(articles):
    lines = []
    for i, a in enumerate(articles):
        lines.append(f"[{i}] {a.get('title', '')} ({a.get('source', '')}, {a.get('date', '')[:10]})\n{a.get('body', '')[:300]}")
    return "\n\n".join(lines)


def clean_indices(indices, num_articles, k):
    picked = []
    for idx in indices:
        if isinstance(idx, int) and 0 <= idx < num_articles and idx not in picked:
            picked.append(idx)
    return picked[:k]


def count_votes(votes, top_n):
    """votes: {persona: [idx, ...]} -> 많이 뽑힌 순, 같으면 앞 순위로 뽑힌 순"""
    score = {}
    for persona, picks in votes.items():
        for rank, idx in enumerate(picks):
            s = score.setdefault(idx, {"votes": 0, "points": 0, "voters": []})
            s["votes"] += 1
            s["points"] += len(picks) - rank
            s["voters"].append(persona)
    ranked = sorted(score.items(), key=lambda x: (-x[1]["votes"], -x[1]["points"], x[0]))
    return ranked[:top_n]


class CuratorAgent:
    def __init__(self, k=5):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
        self.k = k
        self.prompt = PromptTemplate.from_template(
            "{persona} You are subscribing to a newsletter about {topic}. "
            "Interests: {interests}\n\n"
            "Pick the top {k} news articles you're most interested in from the following list. "
            "Return only their indices.\n\n{context}"
        )
        # LLM은 번호만 고르고 기사 내용은 검색 결과를 그대로 쓴다
        self.chain = self.prompt | self.llm.with_structured_output(Picks)

    def pick(self, persona, state, articles):
        result = self.chain.invoke({
            "persona": persona,
            "topic": state["query"],
            "interests": state.get("interests") or "none",
            "k": self.k,
            "context": format_articles(articles),
        })
        return clean_indices(result.indices, len(articles), self.k)

    def run(self, state):
        articles = [json.loads(a) for a in state["trending_articles"]]
        votes = {}
        for name, persona in PERSONAS.items():
            try:
                votes[name] = self.pick(persona, state, articles)
            except Exception as e:
                print(f"[curator] {name} failed: {e}")

        selected = []
        for idx, s in count_votes(votes, state.get("num_articles", 5)):
            selected.append({**articles[idx], "votes": s["votes"], "voters": s["voters"]})

        return {**state, "votes": votes, "selected": selected}
