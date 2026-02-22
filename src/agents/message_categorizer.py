
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from ..prompts import MESSAGE_CATEGORIZER_PROMPT
from src.structured_outputs import CategorizerMessageOutput

load_dotenv()

def categorize_message():
    message_categorizer_prompt = PromptTemplate(
        template= MESSAGE_CATEGORIZER_PROMPT,
        input_variables=["message"]
    )
    llm = ChatOpenAI(model="gpt-4o-mini")
    return message_categorizer_prompt | llm.with_structured_output(CategorizerMessageOutput)
