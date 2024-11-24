from flask import Blueprint, render_template, request
from flask import redirect, url_for
from app.epc_api import EPCAPIClient
from app.epc_scraper import EPCWebScraper
import os
from dotenv import load_dotenv
from app.db_utils import save_api_results, get_api_results, reset_database

# Blueprint for the main routes
main = Blueprint('main', __name__)

# Load environment variables
load_dotenv()
authentication_token = os.getenv('authentication_token')

# Initialize API client and scraper
client = EPCAPIClient(authentication_token=authentication_token)
scraper = EPCWebScraper()


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch postcode from the form
        postcode = request.form.get('postcode', '').strip()

        # Validate postcode input
        if not postcode:
            return render_template('index.html', error="Please enter a valid postcode.")

        # Reset database for new search
        print("Resetting database...")
        reset_database()
        print("Database reset complete.")

        # Fetch and save new results
        client = EPCAPIClient(authentication_token=os.getenv('authentication_token'))
        try:
            data = client.fetch_addresses(postcode)
            print(f"Fetched data for postcode '{postcode}': {data}")

            # Save results to the database
            save_api_results(data.to_dict(orient='records'))
        except Exception as e:
            print(f"Error during API fetch or save: {e}")
            return render_template('index.html', error="Error fetching data from the API.")

        # Retrieve saved results for the given postcode
        results = get_api_results(postcode)
        print(f"Results for postcode '{postcode}': {results}")

        # Render API results page
        return render_template('api_results.html', api_result=results, postcode=postcode, enumerate=enumerate)

    # Render the main search page
    return render_template('index.html')


@main.route('/api-results/<postcode>', methods=['GET'])
def api_results(postcode):
    """
    Display API results for a given postcode.
    """
    print(f"Fetching results for postcode: {postcode}")

    # Query the database for results
    results = get_api_results(postcode)

    # Debugging: Check the fetched results
    print(f"Results fetched: {results}")

    # Check if results are empty
    if not results:
        return render_template('api_results.html', error="No results found for this postcode.", postcode=postcode)

    # Render the results page
    return render_template('api_results.html', api_result=results, postcode=postcode, enumerate=enumerate)

@main.route('/scraper-results/<postcode>', methods=['POST'])
def scraper_results(postcode):
    results = scraper.fetch_addresses(postcode)  # Fetch results using the scraper
    if not results.empty:
        scraper_result = results.to_dict(orient="records")
    else:
        scraper_result = []

    return render_template('scraper_results.html', scraper_result=scraper_result, postcode=postcode, enumerate=enumerate)


@main.route('/details', methods=['POST'])
def details():
    selected_row = request.form.get('selected_row')
    postcode = request.form.get('postcode')
    details = None

    if selected_row:
        api_data = client.fetch_addresses(postcode)
        if not api_data.empty:
            details = api_data.iloc[int(selected_row) - 1].to_dict()

    return render_template('details.html', details=details, postcode=postcode)

if __name__ == "__main__":
    from app import create_app

    # Create the Flask app instance
    app = create_app()

    # Use the application context
    with app.app_context():
        # Instantiate the EPC API client
        client = EPCAPIClient(authentication_token=os.getenv('authentication_token'))

        # Fetch data
        data = client.fetch_addresses("SW10 0XE")

        # Save results to the database
        save_api_results(data.to_dict(orient='records'))

        # Query results
        results = get_api_results("SW10 0XE")
        print("API Results:", results)