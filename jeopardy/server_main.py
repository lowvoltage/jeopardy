from typing import Annotated, Any

from db.db_models import Jeopardy
from env import DB_URI
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Create an engine connected to the SQLite database
# TODO: Session management
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
session = Session()

print('Available:', session.query(Jeopardy).count(), 'questions in DB')


# TODO: Add more docs to show up in SwaggerUI?
class GetRandomQuestionInput(BaseModel):
    # TODO: Restrict: One of: ... ...
    round: str = Field(description='The requested round of the question')
    value: str = Field(description='The requested dollar value of the question')


# TODO: How do we attach JSON examples for input & output payloads?
@app.get('/question/')
async def get_random_question(
    filter_query: Annotated[GetRandomQuestionInput, Query()],
) -> dict[str, Any]:
    """
    Returns a random question based on the provided Round and Value
    """
    q = (
        session.query(Jeopardy)
        .filter_by(round=filter_query.round, value=int(filter_query.value[1:]))
        .order_by(func.random())  # pylint:disable=not-callable
        .first()
    )
    if not q:
        # TODO: Do we want to return a specialized JSON payload here?
        raise HTTPException(status_code=404, detail='Item not found')
    return q.to_dict()
