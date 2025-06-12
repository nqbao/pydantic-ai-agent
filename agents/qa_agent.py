from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic import BaseModel

from agents.models import main_model

class Answer(BaseModel):
    text: str

class NoAnswer(BaseModel):
    pass

agent = Agent(
    main_model,
    model_settings=ModelSettings(max_tokens=1024, temperature=0),
    output_type=Answer | NoAnswer,
    system_prompt=(
        "Answer the following questions about the given text. Only answer the questions if the provided text is relevant."
    ),
)
