from .direct_gen import DirectGenAgent
from .basic_rag import BasicRagAgent
# from .multi_agent import MultiAgent


agent_dict = {
    "direct_gen": DirectGenAgent(),
    "basic_rag": BasicRagAgent(),
    # "multi_agent": MultiAgent(),
}