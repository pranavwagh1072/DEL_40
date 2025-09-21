# MongoDB Weather Data Ingestion (Experiment 5)

## Overview
This project demonstrates fetching live weather data from the OpenWeatherMap API using Python and storing results in a MongoDB collection. The workflow includes defining useful schemas, ensuring index integrity, and upserting weather data for robust, analytical access.

## Files
- `Experiment-5.ipynb`: Jupyter notebook containing all code for API interaction and MongoDB operations.
- `sales_weatherinfo_db.weather`: MongoDB collection that stores daily weather data.

## Weather Document Structure

| Field         | Type             | Example Value               | Description                      |
|-------------- |------------------|-----------------------------|-----------------------------------|
| _id           | ObjectId         | (auto-generated)            | Unique MongoDB identifier         |
| city          | string           | "London"                    | City name                         |
| weather_date  | date (UTC)       | 2025-08-26T00:00:00.000Z    | Weather record date at UTC midnight|
| description   | string           | "overcast clouds"           | Weather description               |
| fetched_at    | date (UTC)       | 2025-08-26T06:41:00.666Z    | Exact fetch timestamp             |
| humidity      | integer          | 72                          | Humidity percentage               |
| source        | string           | "openweather"               | Data source label                 |
| temp_c        | float            | 16.18                       | Temperature in Celsius            |

## Main Steps

1. **Environment Setup**
   - Install Python packages: `requests`, `pymongo`, `pandas`.

2. **API and MongoDB Configuration**
   - Store your OpenWeather API key.
   - Set `MONGO_URI` and select database/collection (`sales_weatherinfo_db.weather`).

3. **Indexing and Upsert Logic**
   - Ensure compound index on `weather_date` and `city` for uniqueness.
   - Use `update_one(..., upsert=True)` for inserting or updating documents.

4. **Fetch and Store Workflow**
   - Python script fetches weather using `requests`.
   - Document assembled with proper UTC date and timestamp.
   - Document upserted in MongoDB collection.

5. **Result Example**

{
"city": "London",
"weather_date": "2025-08-26T00:00:00.000Z",
"description": "overcast clouds",
"fetched_at": "2025-08-26T06:41:00.666Z",
"humidity": 72,
"source": "openweather",
"temp_c": 16.18
}

text

## Requirements

- Python 3.x
- MongoDB server (tested with 6.x)
- OpenWeatherMap API key
- Libraries: `pymongo`, `requests`, `pandas`

## How to Run

1. Put your API key in the notebook.
2. Run the notebook cells; this will fetch live weather for the given city and store the result.
3. Use MongoDB Compass or CLI to verify the document in `sales_weatherinfo_db.weather`.

## Notes

- Indexes ensure only one weather record per city per date.
- Extendable to multiple cities, periodic data collection, or analytic queries.

---

*This project shows a robust workflow for live weather data integration with MongoDB using Python and the OpenWeatherMap API.*