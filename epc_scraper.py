import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict


class EPCWebScraper:
    """Scraper for retrieving EPC data from the EPC website."""
    
    def __init__(self) -> None:
        """Initialize the scraper with base URL and headers."""
        self.base_url = "https://find-energy-certificate.service.gov.uk/find-a-certificate/search-by-postcode?postcode="
        # self.headers = {
        #     "User-Agent": (
        #         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        #         "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        #     )
        # }
        # print("base urls ", self.base_url)

    def fetch_html(self, postcode: str) -> str:
        """
        Fetch the HTML content for the given postcode.
        
        :param postcode: The postcode to search for.
        :return: HTML content as a string.
        """
        url = f"{self.base_url}{postcode}"
        # response = requests.get(url, headers=self.headers)
        response = requests.get(url)
        # print("url: ", url)
        # print("response: ",response.status_code)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch data for postcode '{postcode}'. Status code: {response.status_code}")
        return response.text
    
    def parse_html(self, html_content: str) -> pd.DataFrame:
        """
        Parse the HTML content to extract address data.
        
        :param html_content: HTML content as a string.
        :return: DataFrame containing address data.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Extract EPC data
        results = []
        table = soup.find("table")
        body = table.find('tbody')
        row = body.find_all("tr")
        for entry in row:
            # print("-----start-----")
            address = entry.find("a", class_="govuk-link").text.strip()
            energy_rating = entry.find("td", class_="govuk-table__cell").text.strip()
            valid_until = entry.find("td", class_="govuk-table__cell date").text.strip()
            if "Expired" in valid_until:
                valid_until, blank, expired = valid_until.split('\n')
                # print("valid_date: "+valid_date)
                # # print(valid_date)
                # print("expired: " + expired)
            else:
                expired = ""

            # expired = entry.find_all(string="Expired")
            # print("address: " + address)
            # print("energy_rating: " + energy_rating)
            # print("valid_until: " + repr(valid_until))
            #
            # print("expired: " + expired)


        # for entry in soup.find_all("div", class_="certificate-result"):
        #     address = entry.find("a", class_="govuk-link").text.strip()
        #     energy_rating = entry.find("td", class_="govuk-table__cell").text.strip()
        #     valid_until = entry.find("td", class_="govuk-table__cell date").text.strip()
        #
            results.append({
                "Address": address,
                "Energy Rating": energy_rating,
                "Valid Until": valid_until,
                "Expired": expired
            })
        # print(results)
        # Return as a DataFrame
        return pd.DataFrame(results)
    
    def fetch_addresses(self, postcode: str) -> pd.DataFrame:
        """
        Fetch addresses for a given postcode by scraping the EPC webpage.
        
        :param postcode: The postcode to search for.
        :return: DataFrame containing address data.
        """
        html_content = self.fetch_html(postcode)
        return self.parse_html(html_content)


# Example usage
if __name__ == "__main__":
    scraper = EPCWebScraper()
    postcode = "HA0 3PS"  # Example postcode
    try:
        addresses_df = scraper.fetch_addresses(postcode)
        if addresses_df.empty:
            print(f"No addresses found for postcode '{postcode}'.")
        else:
            print(f"Addresses for postcode '{postcode}':\n{addresses_df}")
    except RuntimeError as e:
        print(e)
