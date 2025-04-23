## Project Brief: Hourly Temperature Comparison Tool

**Phase 1: Bulk Data Download and Storage**

**1. Core Problem:** The need to collect and store a significant volume of historical hourly temperature data and associated station metadata from specific online sources to enable future analysis and comparison.

**2. High-Level Goals:**

* Efficiently download ten years' worth of daily temperature data.
* Download and process station metadata.
* Store both the temperature data and station metadata in a structured and easily queryable database, with future portability in mind.

**3. Target Audience:** The data will be used internally for the development of the temperature comparison tool.

**4. Core Concept/Features (High-Level):**

* **Automated Daily Data Download:** Develop a process to iterate through the URLs for each day within the last ten years (from the current date).
* **Daily Data Extraction:** Extract relevant temperature information from the downloaded text files.
* **Station Metadata Download:** Download and process the zip file containing station metadata.
* **Metadata Extraction:** Extract relevant information about each meteorological station from the metadata file.
* **Database Design:** Design a database schema to store both the hourly temperature data and the station metadata, establishing relationships between them.
* **Database Storage:** Store the extracted data into a local SQLite database, architected for potential migration to PostgreSQL.

**5. MVP Scope (Phase 1):**

* **IN SCOPE for MVP:**
    * Downloading daily data files from the specified URL pattern for the period starting from April 21, 2015, to April 20, 2025.
    * Basic error handling for network issues or missing daily data files.
    * Downloading and extracting the station metadata from the provided zip file.
    * Designing a relational database schema in SQLite to store:
        * Hourly temperature data (station identifier, timestamp (date and hour), temperature).
        * Station metadata (station identifier, name, geographical coordinates, etc.).
        * Establishing a clear link between the temperature data and the corresponding station metadata.
    * Storing both datasets into the local SQLite database.
    * Structuring the database design with consideration for future migration to PostgreSQL (e.g., using standard SQL practices, avoiding SQLite-specific features where possible).
* **OUT OF SCOPE for MVP:**
    * Handling potential changes in the daily data format or metadata format over the ten-year period.
    * Implementing more robust error handling and logging.
    * Performing data cleaning or transformation beyond basic extraction.
    * User interface for initiating or monitoring the download process.
    * Automated updates of the metadata (we will assume the provided metadata is relatively static for the MVP).

**6. Initial Technical Leanings (Optional):**

* Preference for using Python for scripting the data download, metadata processing, and database interaction.
* Consider using the `requests` library for downloading files, the `zipfile` library for handling the metadata archive, and `sqlite3` for the local database.
* Adhere to standard SQL practices to facilitate potential migration to PostgreSQL in the future.

---

**Phase 2: Data Processing and Visualization**

**1. Core Problem:** Users want to understand the temperature differences between different locations over time by comparing hourly temperature variations and analyzing the average temperature difference over a user-defined historical period.

**2. High-Level Goals:**

* Enable users to compare hourly temperature data between two selected cities from the stored database.
* Allow users to define a historical period for analysis.
* Visualize the hourly temperature trends for selected cities and highlight the minimum and maximum temperature differences within a 24-hour cycle.

**3. Target Audience:** Individuals interested in analyzing historical temperature patterns across different geographical locations.

**4. Core Concept/Features (High-Level):**

* **City Selection:** Allow users to select two cities from the database for comparison.
* **Date Range Selection:** Enable users to define a start and end date for the analysis using a date picker. Default start date will be 10 years prior to the selected end date (defaulting to yesterday).
* **Data Retrieval:** Query the database to retrieve the hourly temperature data for the selected cities and date range.
* **Temperature Difference Calculation:** Calculate the temperature difference between the selected cities for each hour of the day.
* **Visualization:** Generate a plot displaying the hourly temperature curves for each selected city over a 24-hour period, along with markers indicating the minimum and maximum temperature differences.
* **Average Difference Calculation:** Calculate and display the average temperature difference between the selected cities over the chosen historical period for each hour of the day.

**5. MVP Scope (Phase 2):**

* **IN SCOPE for MVP:**
    * Ability to select exactly **two** cities from the database for comparison.
    * Ability to define a start and end date for the historical period using a date picker.
    * Default end date set to yesterday (April 20, 2025).
    * Default start date set to ten years prior to the end date (April 21, 2015).
    * Querying the local database to retrieve necessary data.
    * Calculating the hourly temperature difference between the two selected cities.
    * Generating a plot showing the 24-hour temperature curve for each of the two selected cities using a stylish pandas or seaborn template.
    * Marking the minimum and maximum temperature difference on the plot for a representative 24-hour period within the selected date range.
* **OUT OF SCOPE for MVP:**
    * Selecting more than two cities for comparison.
    * Advanced visualization options.
    * Different styling options beyond a default stylish template.
    * Saving or exporting the generated plots or data.
    * Handling missing data or data quality issues beyond what was addressed in Phase 1.
    * User authentication or account management.
    * More complex statistical analysis.

**6. Initial Technical Leanings (Optional):**

* Preference for using Python for data processing and visualization.
* Leverage the pandas library for data manipulation and seaborn for plot generation.
* Utilize the `sqlite3` library to interact with the local database created in Phase 1.
