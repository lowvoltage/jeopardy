import csv

from db.db_models import Jeopardy
from env import DATA_PATH, DB_URI
from ingestion.dataset import download_csv
from ingestion.models import JeopardyQuestion
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

CSV_FILEPATH = DATA_PATH / 'jeopardy_questions.csv'


def ingest_dataset(engine: Engine | None = None) -> None:
    # Download the dataset CSV
    download_csv(CSV_FILEPATH)

    # Read and validate into Python objects
    with open(CSV_FILEPATH) as f_in:
        # Note: Without `skipinitialspace` the CSV headers do not map nicely into the model fields
        reader = csv.DictReader(f_in, skipinitialspace=True)
        dataset_questions = [JeopardyQuestion.model_validate(row) for row in reader]

    # # DEBUG:
    # for q in dataset_questions[:3]:
    #     print(q)

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


if __name__ == '__main__':
    ingest_dataset()
