from pathlib import Path

import requests

JEOPARDY_CSV_URL = (
    'https://github.com/russmatney/go-jeopardy/raw/refs/heads/master/JEOPARDY_CSV.csv'
)


def download_csv(target_filepath: Path) -> None:
    target_filepath.parent.mkdir(exist_ok=True)

    # Skip downloading if already exists
    # TODO: Add a flag to allow force-download?
    if target_filepath.exists():
        print(target_filepath, 'already exists')
        return

    with requests.get(url=JEOPARDY_CSV_URL, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        with open(target_filepath, 'wb') as f_out:
            for chunk in resp.iter_content(chunk_size=8192):
                f_out.write(chunk)
        print('Downloaded', target_filepath)
