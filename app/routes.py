from flask import Blueprint, render_template, request
from epc_api import EPCAPIClient
import os
from dotenv import load_dotenv

# Blueprint for the main routes
main = Blueprint('main', __name__)

# Load environment variables
load_dotenv()
authentication_token = os.getenv('authentication_token')

# Initialize the EPC API client
client = EPCAPIClient(authentication_token=authentication_token)

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    Home route: displays the input form and the resulting DataFrame as a table.
    """
    result = None
    error = None

    if request.method == 'POST':
        postcode = request.form.get('postcode')
        if postcode:
            try:
                # Fetch DataFrame from the API
                result = client.fetch_addresses(postcode)
                print("DEBUG: Result DataFrame:")
                print(result)
                print("DEBUG: DataFrame is empty:", result.empty)
                if result.empty:  # Check if DataFrame is empty
                    error = f"No results found for postcode '{postcode}'."
            except Exception as e:
                error = str(e)
        else:
            error = "Please enter a valid postcode."

    return render_template('index.html', result=result, error=error)
