from flask import Blueprint, render_template, request, redirect, url_for
from app.epc_api import EPCAPIClient
from app.epc_scraper import EPCWebScraper
import os
from dotenv import load_dotenv

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
    """
    Home page: Input postcode and decide workflow.
    """
    error = None

    if request.method == 'POST':
        postcode = request.form.get('postcode')
        if postcode:
            # Redirect to the API results page
            return redirect(url_for('main.api_results', postcode=postcode))
        else:
            error = "Please enter a valid postcode."

    return render_template('index.html', error=error)


@main.route('/api_results', methods=['GET', 'POST'])
def api_results():
    """
    Show API results and allow selection of an address.
    """
    postcode = request.args.get('postcode')
    api_result = None
    error = None

    if postcode:
        try:
            api_data = client.fetch_addresses(postcode)
            if not api_data.empty:
                api_result = api_data[
                    ['lmk-key', 'address1', 'address2', 'address3', 'postcode', 'inspection-date', 'uprn']
                ].reset_index(drop=True)
                api_result.index += 1
                api_result.insert(0, 'Order', api_result.index)
            else:
                error = f"No API results found for postcode '{postcode}'."
        except Exception as e:
            error = str(e)

    return render_template('api_results.html', api_result=api_result, error=error, postcode=postcode)


@main.route('/scraper_results', methods=['POST'])
def scraper_results():
    """
    Show scraper results for the given postcode.
    """
    postcode = request.form.get('postcode')
    scraper_result = None
    error = None

    if postcode:
        try:
            scraper_result = scraper.fetch_addresses(postcode)
            if scraper_result.empty:
                error = f"No scraper results found for postcode '{postcode}'."
        except Exception as e:
            error = str(e)

    return render_template('scraper_results.html', scraper_result=scraper_result, error=error, postcode=postcode)


@main.route('/details', methods=['POST'])
def details():
    """
    Show detailed data for the selected address.
    """
    selected_row = request.form.get('selected_row')
    postcode = request.form.get('postcode')
    details = None

    if selected_row:
        api_data = client.fetch_addresses(postcode)
        if not api_data.empty:
            details = api_data.iloc[int(selected_row) - 1].to_dict()

    return render_template('details.html', details=details)
