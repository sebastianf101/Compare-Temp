# Hourly Temperature Comparison Tool PRD

## Status: Draft

## Intro

The Hourly Temperature Comparison Tool is designed to automate the download, extraction, and storage of ten years of historical hourly temperature data and associated station metadata from fixed online sources. The project will provide a robust backend for data collection and a user-friendly dashboard for comparing and visualizing temperature differences between cities over user-defined periods. The architecture is designed for future extensibility and migration to more scalable databases.

## Goals and Context

- **Objectives**:
  - Automate the retrieval and storage of historical hourly temperature data and station metadata.
  - Provide a dashboard for users to compare temperature trends between two cities over a selected period.
  - Ensure the system is maintainable, testable, and ready for future enhancements.

- **Measurable Outcomes**:
  - 100% of available data for the specified period is downloaded and stored.
  - Dashboard allows selection of two cities and a date range, and displays the required visualizations.
  - All core scripts and components are covered by automated tests.

- **Success Criteria**:
  - Data completeness and integrity in the local database.
  - Dashboard usability and correctness of visualizations.
  - Automated tests pass for all critical paths.

- **KPIs**:
  - Data download success rate.
  - Dashboard usage and error rates.
  - Test coverage percentage.

## Features and Requirements

- **Functional Requirements**:
  - Download daily temperature data files for the last ten years from fixed URLs.
  - Download and extract station metadata from a provided zip file.
  - Extract and store relevant data in a relational SQLite database (PostgreSQL-ready schema).
  - Provide a dashboard for:
    - Selecting two cities.
    - Selecting a date range (default: last ten years).
    - Visualizing 24-hour temperature curves and min/max differences.
  - Basic error handling for network and missing file issues.

- **Non-Functional Requirements**:
  - Containerized deployment (Docker).
  - Automated unit and integration testing.
  - Code readability and maintainability.
  - Use standard SQL practices for future migration.

- **User Experience Requirements**:
  - Simple, intuitive dashboard UI.
  - Responsive design for desktop use.
  - Clear feedback for loading, errors, and empty states.

- **Integration Requirements**:
  - Use only fixed, known data sources.
  - SQLite for MVP, with schema compatible with PostgreSQL.

- **Testing Requirements**:
  - Automated tests for data download, extraction, storage, and dashboard logic.
  - Use pytest or similar frameworks.
  - Each story must achieve at least 80% automated test coverage and all tests must pass before the story is considered complete.

## Epic Story List

**Note:** No story is complete until it has at least 80% automated test coverage and all tests are passing.

### Epic 0: Initial Project Setup & Configuration

- **Story 0.1:** Setup Project Repository
  - Subtask: Initialize Git repository.
  - Subtask: Create `.gitignore` file.
  - Subtask: Create initial `README.md`.
- **Story 0.2:** Configure Docker Environment
  - Subtask: Create `Dockerfile` for the application.
  - Subtask: Create `docker-compose.yml` for service orchestration (app, potentially db later).
  - Subtask: Create `requirements.txt`.
- **Story 0.3:** Setup Basic CI/CD Pipeline
  - Subtask: Configure GitHub Actions workflow (or similar).
  - Subtask: Add initial linting step (e.g., flake8).
  - Subtask: Add initial testing step (e.g., `pytest`).
- **Story 0.4:** Initialize Database Schema
  - Subtask: Define initial SQLite table schemas (stations, temperatures) potentially using an ORM like SQLAlchemy or plain SQL scripts.
  - Subtask: Create script (`init_db.py`) to initialize the database/tables.
- **Story 0.5:** Document Environment Setup
  - Subtask: Update `README.md` with detailed local setup instructions (Docker, dependencies, DB init).
  - Subtask: Create `.env.example` file for environment variables.

### Epic 1: Data Ingestion and Storage

- **Story 1.1:** Download Daily Temperature Data
  - Subtask: Implement URL generation logic for the specified date range (last 10 years).
  - Subtask: Implement download function using `requests`, handling potential network errors (e.g., retries, timeouts) and logging.
  - Subtask: Add basic error handling for missing daily data files.
  - Subtask: Write unit tests for URL generation and download logic (consider mocking `requests`).
- **Story 1.2:** Extract Temperature Data
  - Subtask: Implement logic to parse the downloaded text files to extract relevant hourly temperature information.
  - Subtask: Structure extracted data (e.g., list of dicts or pandas DataFrame).
  - Subtask: Write unit tests for the data extraction/parsing logic.
- **Story 1.3:** Download and Process Station Metadata
  - Subtask: Implement download function for the station metadata zip file using `requests`.
  - Subtask: Implement zip file extraction using `zipfile`.
  - Subtask: Implement logic to parse the metadata file and extract relevant station information (ID, name, coordinates).
  - Subtask: Write unit tests for metadata download, extraction, and parsing.
- **Story 1.4:** Implement Database Storage Logic
  - Subtask: Implement functions/methods (Repository pattern) to interact with the SQLite database.
  - Subtask: Implement function to insert/update station metadata.
  - Subtask: Implement function to bulk insert hourly temperature data, ensuring linkage to station ID.
  - Subtask: Ensure use of standard SQL practices suitable for potential PostgreSQL migration.
  - Subtask: Write integration tests for database insertion and querying logic.

### Epic 2: Dashboard and Visualization (Assuming Flask Backend + React Frontend)

- **Story 2.1:** Setup Dashboard Backend (Flask)
  - Subtask: Initialize basic Flask application structure.
  - Subtask: Create API endpoint (`/api/cities`) to fetch the list of available cities from the database.
  - Subtask: Implement logic to query distinct cities from the station metadata table.
  - Subtask: Write unit tests for the `/api/cities` endpoint.
- **Story 2.2:** Setup Dashboard Frontend (React)
  - Subtask: Initialize basic React application structure (e.g., using Create React App).
  - Subtask: Implement state management for selections (cities, dates).
  - Subtask: Implement UI component for selecting the first city (dropdown populated from `/api/cities`).
  - Subtask: Implement UI component for selecting the second city (dropdown populated from `/api/cities`).
  - Subtask: Implement UI component for date range selection (using a date picker library).
  - Subtask: Set default date range (10 years prior to yesterday).
  - Subtask: Write frontend unit tests for selection components (e.g., using Jest/React Testing Library).
- **Story 2.3:** Implement Data Retrieval API Endpoint
  - Subtask: Create API endpoint (`/api/temperature-comparison`) that accepts two city IDs and a date range.
  - Subtask: Implement backend logic to query the database for hourly temperature data for the selected cities and dates.
  - Subtask: Implement data processing logic (pandas) to align data and calculate hourly differences.
  - Subtask: Implement logic to find min/max differences over a representative 24h cycle.
  - Subtask: Implement logic to calculate the average hourly difference over the entire period.
  - Subtask: Structure the API response (e.g., JSON containing processed data for visualization).
  - Subtask: Write integration tests for the `/api/temperature-comparison` endpoint.
- **Story 2.4:** Implement Frontend Visualization
  - Subtask: Implement frontend logic to call the `/api/temperature-comparison` endpoint when selections change.
  - Subtask: Integrate a charting library (e.g., Chart.js, Recharts, Seaborn via backend generation if simpler).
  - Subtask: Implement component to display the 24-hour temperature curves for both cities.
  - Subtask: Implement markers/annotations on the chart for min/max differences.
  - Subtask: Display the calculated average hourly differences (e.g., in a table or text).
  - Subtask: Implement loading states and basic error handling for the API call.
  - Subtask: Write frontend tests for the visualization component.

### Epic N: Future Epic Enhancements (Beyond Scope of current PRD)

- Support for more than two cities.
- Advanced visualization and export options.
- Automated metadata updates.
- Robust error handling and logging.
- User authentication and account management.
- Migration to PostgreSQL or cloud database.

## Technology Stack

| Technology   | Version | Description                                              |
| ------------ | ------- | -------------------------------------------------------- |
| Python       | 3.10+   | Scripting, data processing, dashboard backend            |
| pandas       | latest  | Data manipulation                                        |
| seaborn      | latest  | Data visualization                                       |
| requests     | latest  | HTTP requests for data download                          |
| zipfile      | stdlib  | Handling metadata archives                               |
| sqlite3      | stdlib  | Local relational database                                |
| Docker       | latest  | Containerization                                         |
| pytest       | latest  | Automated testing                                        |
| Streamlit/Dash/Flask+React | latest | Dashboard UI (final choice to be made in architecture) |

## Project Structure

```
hourly-temp-comparison/
├── data/                  # Downloaded raw data and metadata
├── db/                    # SQLite database files
├── scripts/               # Data download and processing scripts
│   ├── download_data.py
│   ├── process_metadata.py
│   └── populate_db.py
├── dashboard/             # Dashboard UI code
│   └── app.py
├── tests/                 # Automated tests
│   ├── test_download.py
│   ├── test_db.py
│   └── test_dashboard.py
├── Dockerfile
├── requirements.txt
├── README.md
└── .env.example
```

### POST MVP / PRD Features

- Support for more than two cities in comparison.
- Advanced visualization and export (e.g., CSV, PNG).
- Automated updates and monitoring of data sources.
- Robust error handling and logging.
- User authentication and access control.
- Migration to PostgreSQL or cloud database.
- Mobile-friendly dashboard.

## Change Log

| Change               | Story ID | Description                                                   |
| -------------------- | -------- | ------------------------------------------------------------- |
| Initial draft        | N/A      | Initial draft PRD                                             | 