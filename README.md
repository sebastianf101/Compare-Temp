# Compare-Temp

A Python application for comparing temperature data from different weather stations.

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Compare-Temp.git
cd Compare-Temp
```

### 2. Environment Setup

1. Copy the environment example file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your configuration:
   ```bash
   # Database Configuration
   DATABASE_URL=sqlite:///db/weather.db
   # For PostgreSQL:
   # DATABASE_URL=postgresql://user:password@localhost:5432/weather_db

   # Flask Configuration
   FLASK_APP=app
   FLASK_ENV=development
   FLASK_DEBUG=1

   # API Configuration
   API_KEY=your_api_key_here
   API_BASE_URL=https://api.example.com

   # Logging Configuration
   LOG_LEVEL=INFO
   LOG_FILE=logs/app.log

   # Docker Configuration
   DOCKER_NETWORK=compare-temp-network
   DOCKER_VOLUME=compare-temp-data
   ```

### 3. Docker Setup

1. Build the Docker image:
   ```bash
   docker-compose build
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. Verify the services are running:
   ```bash
   docker-compose ps
   ```

### 4. Database Setup

1. Initialize the database:
   ```bash
   docker-compose exec app python -c "from app.db import init_db; init_db()"
   ```

2. Verify the database is working:
   ```bash
   docker-compose exec app python -m pytest tests/test_db.py -v
   ```

### 5. Development Workflow

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Run linting:
   ```bash
   flake8 .
   ```

4. Start the development server:
   ```bash
   flask run
   ```

## Project Structure

```
Compare-Temp/
├── app/                    # Application code
│   ├── db/                # Database models and utilities
│   ├── api/               # API endpoints
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── data/                  # Data files
├── db/                    # Database files
├── .github/               # GitHub configuration
│   └── workflows/         # CI/CD workflows
├── .env.example           # Environment variables example
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Overview

This project automates the download, extraction, and storage of ten years of historical hourly temperature data and associated station metadata from fixed online sources. It provides a user-friendly dashboard for comparing and visualizing temperature differences between cities over user-defined periods.

## Project Structure

```
hourly-temp-comparison/
├── data/                  # Downloaded raw data and metadata
├── db/                    # SQLite database files
├── scripts/               # Data download and processing scripts
├── dashboard/             # Dashboard UI code
├── tests/                 # Automated tests
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Docker
- Git

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hourly-temp-comparison
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```

5. Run the application:
   ```bash
   python dashboard/app.py
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t temp-comparison .
   ```

2. Run the container:
   ```bash
   docker-compose up
   ```

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

3. Push your changes and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Testing

Run the test suite:
```bash
pytest
```

## License

[Add your license information here]

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
