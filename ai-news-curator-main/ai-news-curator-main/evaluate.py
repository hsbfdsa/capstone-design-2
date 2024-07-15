import os
import json
import datetime
import argparse

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from lib.baseline import agent_dict


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', default='basic_rag', type=str, help='[direct_gen, basic_rag, multi_agent]')
    parser.add_argument('--num_articles', default=5, type=int)
    parser.add_argument('--topic', default='AI, LLM', type=str)
    parser.add_argument('--interests', default='Newly released models', type=str)
    parser.add_argument('--num_iters', default=1, type=int)
    parser.add_argument('--eval_dir', default='./eval_results', type=str)
    args = parser.parse_args()
    return args


class Result(BaseModel):
    """Evaluation result."""
    feedback: str = Field(description="Feedback")
    score: int = Field(description="Score")


def main(args):
    os.makedirs(args.eval_dir, exist_ok=True)
    
    # --------------------------------------------------------------------------------
    # Evaluation chain setup
    # --------------------------------------------------------------------------------
    llm = ChatOpenAI(
        model="gpt-4-turbo",
        temperature=0,
    )
    
    prompt = PromptTemplate.from_template(
        """###Task Description:
    An instruction (might include an Input inside it), a response to evaluate, and a score rubric representing a evaluation are given.
    1. Write a detailed feedback that assess the quality of the response strictly based on the given score rubric, not evaluating in general.
    2. After writing a feedback, write a score that is an integer between 1 and 5. You should refer to the score rubric.
    3. The output format should look as follows: \"Feedback: (write a feedback for  [RESULT] (an integer number between 1 and 5)\"
    4. Please do not generate any other opening, closing, and explanations.

    ###The instruction to evaluate:
    You are an AI news curator. Your task is to find distinct news articles that users will be most interested in. 
    
    User: Please tell me about the top {num_articles} {topic}-related news stories. Especially, I'm interested in {interests}.
    Please arrange the final selected news articles in the order I would like. Today's date is {today}.

    ###Response to evaluate:
    {response}

    ###Score Rubrics:
    {score_rubric}

    ###Feedback: 
    """
    )
    
    chain = prompt | llm.with_structured_output(Result)
    
    # --------------------------------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------------------------------
    agent = agent_dict[args.title]    
    response = agent.run(args.topic, args.num_articles, args.interests)

    score_rubric = json.load(open("./score_rubric.json", encoding="utf-8"))

    eval_results = {
        "response": response,
        "eval_results": []
    }
    
    for _ in range(args.num_iters):        
        for eval_aspect in list(score_rubric.keys()):
            outputs = chain.invoke(
                {
                    "num_articles": args.num_articles,
                    "topic": args.topic,
                    "interests": args.interests,
                    "response": response,
                    "score_rubric": score_rubric[eval_aspect],
                    "today": datetime.datetime.now().strftime("%Y-%m-%d")
                }
            )
            
            eval_result = {
                "eval_aspect": eval_aspect,
                "feedback": outputs.feedback,
                "score": outputs.score,
            }
            
            eval_results["eval_results"].append(eval_result)
            
    eval_result_path = f'{args.eval_dir}/{args.title}.json'
    
    with open(eval_result_path, 'a') as f:
        json.dump(eval_results, f, indent=4)
            
        
if __name__=="__main__":
    args = get_args()
    main(args)