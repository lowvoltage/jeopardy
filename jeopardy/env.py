import os
from pathlib import Path

DATA_PATH = Path(os.environ.get('J_DATA_PATH', './data')).resolve()

# Allow for an external (PostgreSQL) DB to be configured
DEFAULT_SQLITE_DB_FILEPATH = DATA_PATH / 'jeopardy.db'
DB_URI = os.environ.get('J_DB_URI', f'sqlite:///{DEFAULT_SQLITE_DB_FILEPATH}')
