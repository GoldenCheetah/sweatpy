from goldencheetahlib.client import GoldenCheetahClient

from .models.dataframes import WorkoutDataFrame


class Client(GoldenCheetahClient):
    def _request_activity_data(self, athlete, filename):
        """
        This method overwrites this method on the GoldenCheetahClient class so
        methods like get_last_activity() return a WorkoutDataFrame instead of a
        regular pandas.DataFrame

        Parameters
        ----------
        athlete : str
        filename : str

        Returns
        -------
        df : WorkoutDataFrame
        """
        df = super(Client, self)._request_activity_data(athlete, filename)
        return WorkoutDataFrame(df)
