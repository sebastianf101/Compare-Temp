# Architecture for Hourly Temperature Comparison Tool

## Status: Draft

## Technical Summary

The Hourly Temperature Comparison Tool is designed to automate the download, extraction, and storage of ten years of historical hourly temperature data and associated station metadata from fixed online sources. The project will provide a robust backend for data collection and a user-friendly dashboard for comparing and visualizing temperature differences between cities over user-defined periods. The architecture is designed for future extensibility and migration to more scalable databases.

## Technology Table

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

## High-Level Overview

The architecture follows a modular design, with clear separation of concerns between data ingestion, storage, and visualization. The system is containerized using Docker for ease of deployment and scalability.

### Component View

- **Data Ingestion Module**: Handles downloading and extracting temperature data and station metadata.
- **Database Module**: Manages data storage and retrieval using SQLite, with a schema designed for future migration to PostgreSQL.
- **Dashboard Module**: Provides a user interface for selecting cities and date ranges, and visualizes temperature differences.

## Architectural Diagrams, Data Models, Schemas

### Data Models

#### Temperature Data Schema

```json
{
  "station_id": "string",
  "timestamp": "datetime",
  "temperature": "float"
}
```

#### Station Metadata Schema

```json
{
  "station_id": "string",
  "name": "string",
  "latitude": "float",
  "longitude": "float"
}
```

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

## Testing Requirements and Framework

- **Testing Framework**: pytest
- **Coverage Requirement**: Each story must achieve at least 80% automated test coverage and all tests must pass before the story is considered complete.

## Patterns and Standards

- **Architectural/Design Patterns**: Repository Pattern for data access, MVC for dashboard structure.
- **API Design Standards**: RESTful API design for dashboard backend.
- **Coding Standards**: PEP 8 for Python code, Airbnb JavaScript Style Guide for frontend code.
- **Error Handling Strategy**: Standardized error logging and exception handling.

## Initial Project Setup

- Set up project repository and version control.
- Create and configure Docker environment.
- Initialize SQLite database.
- Document environment setup and usage instructions.

## Infrastructure and Deployment

- **Deployment Environment**: Docker containers for local and cloud deployment.
- **CI/CD Strategy**: Automated testing and deployment using GitHub Actions or similar.

## Change Log

| Change               | Story ID | Description                                                   |
| -------------------- | -------- | ------------------------------------------------------------- |
| Initial draft        | N/A      | Initial draft architecture document                           | 