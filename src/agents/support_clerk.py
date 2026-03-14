from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from ..prompts import SUPPORT_CLERK_PROMPT


def solve_user_issue():
    support_clerk_prompt = PromptTemplate(
        template = SUPPORT_CLERK_PROMPT,
        input_variables=["message"]
    )
    llm = ChatOpenAI(model="gpt-4o-mini")
    return support_clerk_prompt