# MongoDB Weather Data Aggregation & Storage (Experiment 5.1)

## Overview
This project fetches live weather data for multiple cities via the OpenWeatherMap API, stores daily records in a MongoDB collection, and demonstrates aggregation queries for temperature analytics. All ETL logic, upsert methodology, and aggregation queries are handled in Python using the requests and pymongo libraries.

## Files
- `Exp5.1.ipynb`: Jupyter notebook containing the complete workflow, including fetching weather data, storing in MongoDB, ensuring indexes, and running aggregation queries.
- `salesweatherinfodb.weather`: MongoDB collection that holds daily weather documents per city.

## Weather Document Structure

| Field        | Type        | Example              | Description                                     |
|--------------|-------------|----------------------|-------------------------------------------------|
| city         | string      | "London"             | City name                                       |
| weatherdate  | date (UTC)  | 2025-09-21T00:00:00Z | Date of record (UTC, always midnight)            |
| tempc        | float       | 14.54                | Temperature in Celsius                          |
| humidity     | integer     | 83                   | Humidity percent                                |
| description  | string      | "mist", "clear sky"  | Weather description from the API                 |
| fetchedat    | date (UTC)  | 2025-09-21T11:15:34Z | Timestamp when the data was retrieved            |
| source       | string      | "openweather"        | Source identifier                               |

## Main Steps

1. **Setup**
   - Install packages: requests, pymongo, pandas, numpy.
   - Load your OpenWeatherMap API key and set MongoDB URI to localhost (127.0.0.1:27017).

2. **Data Ingestion**
   - Fetch daily weather for cities such as London, Mumbai, New York, Tokyo, Sydney.
   - Upsert documents in MongoDB to avoid duplicates (one per city per date) and ensure correct indexing.

3. **Aggregation Query**
   - Run MongoDB pipeline to aggregate temperature stats grouped by city and date:
     - Calculate `min_temp`, `avg_temp`, and `max_temp` using `$group`.

#### Example Aggregation Output

| city      | min_temp | avg_temp | max_temp |
|-----------|----------|----------|----------|
| London    | 14.54    | 14.54    | 14.54    |
| Mumbai    | 27.99    | 27.99    | 27.99    |
| New York  | 15.63    | 15.63    | 15.63    |
| Tokyo     | 25.38    | 25.38    | 25.38    |
| Sydney    | 15.98    | 15.98    | 15.98    |

#### Example Document

{
"city": "London",
"weatherdate": "2025-09-21T00:00:00Z",
"tempc": 14.54,
"humidity": 83,
"description": "mist",
"fetchedat": "2025-09-21T11:15:34Z",
"source": "openweather"
}

text

## Requirements

- Python 3.x
- MongoDB server (tested on v6.x)
- OpenWeatherMap API key
- Libraries: pymongo, requests, pandas, numpy

## How to Run

1. Put your API key and update the city list in `Exp5.1.ipynb`.
2. Run notebook cells to ingest and aggregate data.
3. Use MongoDB Compass to review stored documents and aggregation output in `salesweatherinfodb.weather`.

## Notes

- Unique index on `(weatherdate, city)` ensures one document per city per day.
- Aggregation is flexible and can be extended for more metrics or other weather fields.

---

*This notebook is a practical demonstration in Python for ETL, MongoDB schema design, and aggregation analytics using real-world weather data.*