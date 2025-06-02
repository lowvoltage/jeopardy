import os
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient


def test_read_main() -> None:
    with TemporaryDirectory() as d:
        os.environ['J_DATA_PATH'] = d
        from server_main import app  # pylint: disable=import-outside-toplevel

        client = TestClient(app)
        # This is going to be SLOW
        # TODO: Mock the CSV and or DB
        response = client.get('/question/?round=Jeopardy!&value=$200')
        assert response.status_code == 200
        assert response.json()['round'] == 'Jeopardy!'
        assert response.json()['value'] == '$200'
