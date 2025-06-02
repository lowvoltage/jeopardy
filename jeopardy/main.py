from env import DATA_PATH
from ingestion.dataset import download_csv

print('hello, world')
print(DATA_PATH)

download_csv(DATA_PATH / 'j.csv')
