from db.db_models import Jeopardy
from env import DB_URI
from ingestion.models import JeopardyQuestion
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker


def populate_db(dataset_questions: list[JeopardyQuestion], engine: Engine | None = None) -> None:
    # Create an engine connected to the SQLite database
    engine = engine or create_engine(DB_URI)

    # ReCreate all tables in the engine
    # TODO: [Better] DB lifecycle management. Replace with an "exists" check?
    try:
        Jeopardy.__table__.drop(bind=engine)
    except Exception:
        pass

    Jeopardy.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # TODO: Replace with a bulk op. Batch by 1k items?
    # Populate DB - filter only questions up to $1200
    # TODO: What about "Final Jeopardy!" Qs? Include? Exclude?
    for q in dataset_questions:
        if q.value <= 1200:
            session.add(Jeopardy(**q.model_dump()))

    # Commit the transaction
    session.commit()

    # # DEBUG: Query for all questions
    # for db_q in session.query(Jeopardy).all():
    #     print(db_q.show_no, db_q.question)

    print('Loaded', len(dataset_questions), 'dataset questions')
    print('Persisted', session.query(Jeopardy).count(), 'questions in DB')
