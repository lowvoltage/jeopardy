import csv

from env import DATA_PATH
from ingestion.dataset import download_csv
from ingestion.models import JeopardyQuestion

CSV_FILEPATH = DATA_PATH / 'j.csv'

if __name__ == '__main__':
    print(DATA_PATH)

    download_csv(CSV_FILEPATH)

    with open(CSV_FILEPATH) as f_in:
        reader = csv.DictReader(f_in, skipinitialspace=True)
        q_and_as = [JeopardyQuestion.model_validate(row) for row in reader]

    for q in q_and_as[:5]:
        print(q)
