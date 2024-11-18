import os
from dotenv import load_dotenv
from epc_api import EPCAPIClient


def main() -> None:
    """Main function to run the script."""
    # Load environment variables
    load_dotenv()

    # Retrieve authentication token from .env
    authentication_token = os.getenv('authentication_token')
    if not authentication_token:
        raise ValueError("Authentication token not found in environment variables.")

    # Initialize the EPC API client
    client = EPCAPIClient(authentication_token=authentication_token)

    # Input postcode (can be replaced with user input in the frontend)
    postcode = 'HA0 3PS'

    # Fetch addresses as a DataFrame
    try:
        data = client.fetch_addresses(postcode)
        print(f"Data fetched for postcode '{postcode}':\n{data.head()}")
    except RuntimeError as e:
        print(e)


if __name__ == '__main__':
    main()
