import os
from pathlib import Path

DATA_PATH = Path(os.environ.get('J_DATA_PATH', './data')).resolve()
