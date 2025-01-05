import os

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel

class Answer(BaseModel):
    text: str
    
class NoAnswer(BaseModel):
    pass

model = OpenAIModel(
    "gpt-4o",
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL")
)

qa_agent = Agent(
    model,
    model_settings=ModelSettings(max_tokens=1024, temperature=0),
    result_type=Answer | NoAnswer,
    system_prompt=(
        "Answer the following questions about the given text. Only answer the questions if the provided text is relevant."
    ),
)
