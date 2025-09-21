# Weather Data Ingestion to PostgreSQL

## Overview
This project demonstrates how to fetch real-time weather data from the OpenWeatherMap API for a specific city (Patna) and store it in a PostgreSQL database using Python. The workflow consists of creating the database schema, fetching weather information, and appending it to a `weather` table through SQLAlchemy.

## Files
- `Experiment4-PostgreSQL.ipynb`: Jupyter notebook containing the complete code and step-by-step explanation.
- (Database) **sales_weatherinfo_db**: PostgreSQL database shown in the screenshots, containing the `weather` table for storing records.

## Table Structure

| Column Name   | Data Type        | Description                      |
|:--------------|:----------------|:---------------------------------|
| weather_date  | date            | Date of the weather record       |
| city          | text            | City name (e.g., Patna)          |
| temp_c        | double precision| Temperature in Celsius           |
| humidity      | bigint          | Humidity percentage              |
| description   | text            | Weather description (e.g., haze) |

## Main Steps

1. **API Configuration**
   - Set the OpenWeatherMap API key and the city of interest.

2. **Database Connection**
   - Define the PostgreSQL connection string using SQLAlchemy.

3. **Fetch and Store Data**
   - Fetch weather data via Python using the requests library.
   - Structure the response including date, city, temperature, humidity, and weather description.
   - Store the results into the PostgreSQL `weather` table.

4. **Result Verification**
   - Querying the `weather` table in pgAdmin confirms successful data entry.

## Example Output

| weather_date | city  | temp_c | humidity | description |
|--------------|-------|--------|----------|-------------|
| 2025-09-21   | Patna | 30.96  | 74       | haze        |

## Requirements

- Python 3.x
- pandas
- SQLAlchemy
- psycopg2
- requests
- PostgreSQL 12+ (tested on PostgreSQL 17)
- OpenWeatherMap API Key

## How to Run

1. Update the `API_KEY` and database connection string as needed in the notebook.
2. Open and run the cells in `Experiment4-PostgreSQL.ipynb` inside Jupyter or VS Code.
3. After execution, verify in pgAdmin that the weather data appears in the `public.weather` table.

## Notes

- The code is easily adaptable to any other city by changing the `CITY` variable.
- The structure supports daily ingestion for time series weather analysis.

---

*This project shows end-to-end data ETL (Extract, Transform, Load) from an external API into a PostgreSQL table, with all logic in Python and analysis-ready output in SQL.* 
