# EPC Data Explorer

**EPC Data Explorer** is a Flask-based web application that allows users to input a **postcode**, retrieve a list of relevant **addresses**, and view detailed data for a selected address. It integrates data from multiple sources, processes it, and stores it in a database for efficient access.

## Key Features

- **User Input**: Enter a postcode through a web interface.
- **Data Retrieval**:
  - **Web Scraper**: Fetches a list of addresses from an external website.
  - **API Integration**: Retrieves additional details about addresses from an official EPC database API.
- **User Interaction**:
  - Displays a list of up to 10 addresses for the user to choose from.
  - Fetches and shows detailed data for the selected address.
- **Data Processing**:
  - Cleans and normalizes data from multiple sources.
  - Combines results from the web scraper and API to provide complete details.
- **SQLite Database**:
  - Stores and caches results to improve performance and avoid redundant requests.
- **Frontend**:
  - Provides a simple and user-friendly interface for entering postcodes and viewing results.
- **Dockerized**:
  - Each component runs in a separate Docker container for scalability and modularity.

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (via Flask templates)
- **Database**: SQLite
- **Containerization**: Docker
- **Version Control**: GitHub
- **Web Scraping**: BeautifulSoup, Requests
- **API Interaction**: Requests

## Workflow After User Input

1. **Input**: The user enters a postcode in the web interface.
2. **Address List**: The application retrieves up to 10 addresses related to the postcode from:
   - A web scraper that fetches data from an EPC website.
   - An API that provides additional data from an EPC database.
3. **Selection**: The user selects an address from the list.
4. **Details**: The application fetches and displays detailed information about the selected address.
5. **Caching**: Results are stored in the SQLite database to avoid redundant data retrieval.

## Getting Started

### Prerequisites
- Install Python3
- Install Docker
- Install Git

### License
This project is licensed under the MIT License.
