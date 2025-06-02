from datetime import date
from typing import Any

from pydantic import BaseModel, Field, field_validator


class JeopardyQuestion(BaseModel):
    show_no: int = Field(alias='Show Number')
    air_date: date = Field(alias='Air Date')
    round: str = Field(alias='Round')  # TODO: Make this more strict, an enum / Literal?
    category: str = Field(alias='Category')
    value: int = Field(alias='Value')
    question: str = Field(alias='Question')
    answer: str = Field(alias='Answer')

    @field_validator('value', mode='before')
    def validate_value(cls, v: Any) -> Any:
        if v == 'None':  # Special-case "Final Jeopardy!" lines
            return 0
        if isinstance(v, str):
            assert v
            assert v[0] == '$'
            return int(v[1:].replace(',', ''))
        return v
