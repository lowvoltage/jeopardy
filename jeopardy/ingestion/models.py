from datetime import date

from pydantic import BaseModel, Field


class JeopardyQuestion(BaseModel):
    show_no: int = Field(alias='Show Number')
    air_date: date = Field(alias='Air Date')
    round: str = Field(alias='Round')  # TODO: Make this more strict, an enum / Literal?
    category: str = Field(alias='Category')

    # TODO: Add an int getter / property? Use a validator to load into an int directly?
    value_str: str = Field(alias='Value')
    question: str = Field(alias='Question')
    answer: str = Field(alias='Answer')
