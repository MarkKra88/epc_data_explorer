import pandas as pd
import io
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from typing import Dict, Any


class EPCAPIClient:
    """Client to interact with the EPC API."""

    def __init__(self, authentication_token: str) -> None:
        """
        Initialize the client with the given authentication token.

        :param authentication_token: API token for authorization.
        """
        self.base_url = 'https://epc.opendatacommunities.org/api/v1/domestic/search'
        self.headers = {
            'Accept': 'text/csv',
            'Authorization': f'Basic {authentication_token}'
        }

    def build_url(self, query_params: Dict[str, Any]) -> str:
        """
        Build the full URL with query parameters.

        :param query_params: A dictionary of query parameters.
        :return: The full URL with encoded parameters.
        """
        encoded_params = urlencode(query_params)
        return f"{self.base_url}?{encoded_params}"

    def fetch_addresses(self, postcode: str) -> pd.DataFrame:
        """
        Fetch addresses that match the given postcode and return them as a DataFrame.

        :param postcode: The postcode to search for.
        :return: A DataFrame containing the response data.
        """
        query_params = {'postcode': postcode}
        full_url = self.build_url(query_params)

        # Make the API request
        try:
            with urlopen(Request(full_url, headers=self.headers)) as response:
                csv_data = response.read().decode('utf-8')
                return pd.read_csv(io.StringIO(csv_data))
        except pd.errors.EmptyDataError:
            # Return an empty DataFrame if no data is returned
            return pd.DataFrame()
        except Exception as e:
            raise RuntimeError(f"Error fetching data from EPC API: {e}")
