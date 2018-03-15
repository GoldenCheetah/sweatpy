import vcr

from sweat.io.goldencheetah import Client
from sweat.io.models.dataframes import WorkoutDataFrame


class TestClient:
    @vcr.use_cassette('tests/fixtures/goldencheetah/test_get_last_activity.yaml')
    def test_get_last_activity(self):
        client = Client(athlete='Aart')
        wdf = client.get_last_activity()
        assert isinstance(wdf, WorkoutDataFrame)
