# Hourly Temperature Comparison Tool

A robust tool for comparing historical hourly temperature data between cities over time. This application automates the collection, storage, and visualization of temperature data, providing insights into temperature differences between locations.

## Features

- **Data Collection**
  - Automated download of 10 years of historical hourly temperature data
  - Station metadata extraction and storage
  - Robust error handling for network and missing data scenarios

- **Data Storage**
  - SQLite database with PostgreSQL-compatible schema
  - Efficient storage of hourly temperature records
  - Organized station metadata management

- **Visualization Dashboard**
  - Compare temperature trends between two cities
  - Customizable date range selection
  - 24-hour temperature curve visualization
  - Min/max difference analysis
  - Average hourly difference calculations

## Technical Stack

- **Backend**
  - Python 3.10+
  - pandas for data manipulation
  - SQLite for data storage
  - Flask for API endpoints

- **Frontend**
  - React for dashboard UI
  - Chart.js/Recharts for visualizations

- **Infrastructure**
  - Docker for containerization
  - GitHub Actions for CI/CD
  - pytest for testing

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd hourly-temp-comparison
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Build and start the application:
```bash
docker-compose up --build
```

4. Initialize the database:
```bash
docker-compose exec app python scripts/init_db.py
```

5. Download and process initial data:
```bash
docker-compose exec app python scripts/download_data.py
docker-compose exec app python scripts/process_metadata.py
docker-compose exec app python scripts/populate_db.py
```

### Usage

1. Access the dashboard at `http://localhost:3000`
2. Select two cities from the dropdown menus
3. Choose your desired date range (default: last 10 years)
4. View the temperature comparison visualizations

## Project Structure
