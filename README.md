# EPC Data Explorer

**EPC Data Explorer** is a Flask-based web application that allows users to input a **postcode**, retrieve a list of relevant **addresses**, and view detailed data for a selected address. It integrates data from multiple sources, processes it, and stores it in a database for efficient access.

---

## Key Features

- **User Input**: 
  - Enter a postcode through a web interface.

- **Data Retrieval**:
  - **Web Scraper**: Fetches a list of addresses from an external EPC website.
  - **API Integration**: Retrieves additional details about addresses from an official EPC database API.

- **User Interaction**:
  - Displays a list of addresses retrieved via the API.
  - Allows users to fetch results via a web scraper if desired address is not found.
  - Fetches and shows detailed data for the selected address.

- **Data Processing**:
  - Cleans and normalizes data from multiple sources.
  - Combines results from the web scraper and API to provide complete details.

- **SQLite Database**:
  - **Stores API Results**:
    - Key address details like `lmk-key`, `address1`, `postcode`, etc.
  - **Stores Web Scraper Results**:
    - Address, energy rating, and validity details fetched from the scraper.
  - Caches results to improve performance and avoid redundant data retrieval.

- **Frontend**:
  - Provides a simple and user-friendly interface for entering postcodes and viewing results.

- **Dockerized**:
  - Each component runs in a separate Docker container for scalability and modularity.

---

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (via Flask templates)
- **Database**: SQLite
- **Containerization**: Docker
- **Version Control**: GitHub
- **Web Scraping**: BeautifulSoup, Requests
- **API Interaction**: Requests

---

## Workflow After User Input

1. **Input**: The user enters a postcode in the web interface.
2. **API Data Retrieval**:
   - The application queries the EPC API to fetch up to 10 addresses matching the postcode.
3. **Selection**:
   - The user selects an address to view detailed information.
   - Alternatively, the user can fetch results via the web scraper if the desired address isn’t found.
4. **Scraper Data Retrieval**:
   - The web scraper fetches all addresses for the postcode and displays them.
5. **Details Display**:
   - The application fetches and displays detailed information about the selected address.
6. **Database Caching**:
   - API and scraper results are stored in the SQLite database.
   - Old results are cleared at the start of each new session.

---

## Getting Started

### Prerequisites
1. **Install Python 3.9+**  
   Ensure `pip` is also installed.

2. **Install Docker**  
   For containerization.

3. **Install Git**  
   To clone the repository.

---

### Installation Steps

1. Clone the repository:
   ```bash
    git clone https://github.com/<your-repo>/epc-data-explorer.git
    cd epc-data-explorer
2. Create a virtual environment and activate it:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
4. Set up .env: Create a .env file in the root directory and add your API token and database URI:
    ```bash
    authentication_token=<your_epc_api_key>
    DATABASE_URI=sqlite:///epc_data.db
---

### Running Locally
1. Run the Flask server:
    ```bash
    python main.py 
2. Access the app in your browser at:
    ```bash
    http://127.0.0.1:5000
---
### Docker Setup
1. Build the Docker Image:
    ```bash
    docker build -t epc-data-explorer .

2. Run the Container:
    ```bash
    docker run -p 5000:5000 epc-data-explorer
3. Access the App:
    ```bash
   http://127.0.0.1:5000
4. Push to Docker Hub: Tag and push the image:
   ```bash
   docker tag epc-data-explorer <your-dockerhub-username>/epc-data-explorer:v1
   docker push <your-dockerhub-username>/epc-data-explorer:v1
4. Pull from Docker Hub:
   ```bash
   docker pull <your-dockerhub-username>/epc-data-explorer:v1

---
### License
This project is licensed under the MIT License.
