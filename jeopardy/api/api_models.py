from pydantic import BaseModel, ConfigDict, Field


# TODO: Add more docs to show up in SwaggerUI?
class GetRandomQuestionInputPayload(BaseModel):
    model_config = ConfigDict(extra='forbid')  # Note: Be more strict with query params

    # TODO: Restrict: One of: ... ...
    round: str = Field(description='The requested round of the question')
    value: str = Field(description='The requested dollar value of the question')


class VerifyAnswerInputPayload(BaseModel):
    model_config = ConfigDict(extra='forbid')

    # TODO: Further validation: Non-negative?
    question_id: int = Field(description='The question Database ID')
    user_answer: str = Field(description='The answer to be validated')


class VerifyAnswerOutputPayload(BaseModel):
    model_config = ConfigDict(extra='forbid')

    is_correct: bool = Field(description='True if the answer is deemed correct')
    ai_response: str = Field(description='Details')
