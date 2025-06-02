import csv

from db.core import populate_db
from env import DATA_PATH
from ingestion.dataset import download_csv
from ingestion.models import JeopardyQuestion
from sqlalchemy import Engine

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

    populate_db(dataset_questions, engine)


if __name__ == '__main__':
    ingest_dataset()
