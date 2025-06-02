import random
from typing import Annotated, Any

from api.api_models import (
    GetRandomQuestionInputPayload,
    VerifyAnswerInputPayload,
    VerifyAnswerOutputPayload,
)
from db.db_models import Jeopardy
from env import DB_URI
from fastapi import FastAPI, HTTPException, Query
from ingestion_main import ingest_dataset
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import sessionmaker

# Part 1: Prepare backend content
# Create an engine connected to the SQLite database
# TODO: Session management
engine = create_engine(DB_URI)

if not inspect(engine).has_table(Jeopardy.__tablename__):
    ingest_dataset(engine=engine)

Session = sessionmaker(bind=engine)
session = Session()
print('Info:', session.query(Jeopardy).count(), 'questions available in DB')

# Part 2: Start the API
app = FastAPI()


# TODO: How do we attach JSON examples for input & output payloads?
@app.get('/question/')
async def get_random_question(
    filter_query: Annotated[GetRandomQuestionInputPayload, Query()],
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

    # 404 if missing
    if not q:
        # TODO: Do we want to return a specialized JSON payload here?
        raise HTTPException(status_code=404, detail='Item not found')
    return q.to_dict()


@app.post('/verify-answer/')
async def verify_answer(input_payload: VerifyAnswerInputPayload) -> VerifyAnswerOutputPayload:
    # Load the question from DB. 404 if missing
    q = session.query(Jeopardy).get(input_payload.question_id)
    if not q:
        raise HTTPException(status_code=404, detail='Item not found')

    return VerifyAnswerOutputPayload(
        is_correct=random.choice([True, False]),
        ai_response='TODO: Coming soon...',  # TODO: Not implemented
    )
