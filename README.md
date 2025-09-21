# Weather Data ETL with MySQL

## Overview
This project fetches real-time weather data for multiple cities from the OpenWeatherMap API and stores it in a MySQL database table using Python. The process includes table creation, API calls, and bulk insertions for analytics and reporting.

## Files
- `Experiment-3.ipynb`: Jupyter notebook with all code and workflow steps.
- `sales_weatherinfo_db`: MySQL database created for storing weather records.

## Table Structure

| Column Name   | Data Type     | Description                        |
|:--------------|:-------------|:-----------------------------------|
| weather_date  | DATE         | Date of weather measurement        |
| city          | VARCHAR(100) | Name of the city                   |
| temp_c        | DECIMAL(5,2) | Temperature in Celsius             |
| humidity      | INT          | Humidity percentage                |
| description   | VARCHAR(255) | Weather description (e.g., clouds) |

## Workflow

1. **Setup and Installation**
   - Install dependencies: `requests`, `pandas`, `sqlalchemy`, and `pymysql`.
   - Define API key, city list, and MySQL credentials.

2. **Database Initialization**
   - Creates the database `sales_weatherinfo_db` and ensures the `weather` table exists.

3. **Fetching Data**
   - Weather data for cities such as London, Pune, Las Vegas, Cairo, Yakutsk, Tawang, Mehkar is collected using OpenWeatherMap API.

4. **Storing Data**
   - Each fetched weather record is appended into the MySQL `weather` table using SQLAlchemy and pandas integration.

5. **Result Verification**
   - Use SELECT queries in MySQL Workbench to verify stored weather information.

## Example Table Data

| weather_date | city     | temp_c | humidity | description     |
|--------------|----------|--------|----------|----------------|
| 2025-08-26   | London   | 15.70  | 79       | overcast clouds|
| 2025-08-26   | Pune     | 25.84  | 82       | broken clouds  |
| 2025-08-26   | Las Vegas| 27.57  | 39       | overcast clouds|
| 2025-08-26   | Cairo    | 27.38  | 60       | clear sky      |
| 2025-08-26   | Yakutsk  | 25.03  | 32       | clear sky      |
| 2025-08-26   | Tawang   | 22.56  | 60       | overcast clouds|
| 2025-08-26   | Mehkar   | 27.81  | 70       | broken clouds  |

## Requirements

- Python 3.x
- MySQL server (tested with MySQL 8+)
- OpenWeatherMap API key
- Libraries: pandas, requests, sqlalchemy, pymysql

## How to Run

1. Review and modify credentials and city names in `Experiment-3.ipynb` as needed.
2. Run the notebook cells to create the table and store each city's weather data.
3. Use MySQL Workbench or CLI to confirm weather data is stored in the `weather` table.

## Notes

- The ETL pipeline is extendable to additional cities and weather metrics as required.
- Designed for daily weather logging, supporting future analytics and visualization.

---

*This project demonstrates a complete pipeline from external data extraction (API) to structured database ingestion for analytics and integration in Python and MySQL.*
