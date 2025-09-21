
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import date, datetime, timedelta
import logging
import time
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeatherETL:
    def __init__(self, api_key, pg_conn_string):
        self.api_key = api_key
        self.pg_conn_string = pg_conn_string
        self.engine = create_engine(pg_conn_string)

    def create_table_if_not_exists(self):
        """Create weather table if it doesn't exist"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather (
            id SERIAL PRIMARY KEY,
            weather_date DATE NOT NULL,
            city VARCHAR(100) NOT NULL,
            temp_c DECIMAL(5,2),
            humidity INTEGER,
            description VARCHAR(255),
            pressure DECIMAL(7,2),
            wind_speed DECIMAL(5,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(weather_date, city)
        );
        """
        with self.engine.connect() as conn:
            conn.execute(text(create_table_query))
            conn.commit()
            logger.info("Weather table created/verified")

    def fetch_current_weather(self, city):
        """Fetch current weather data from OpenWeatherMap API"""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            weather_data = {
                'weather_date': date.today(),
                'city': city,
                'temp_c': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed']
            }

            logger.info(f"Successfully fetched weather data for {city}")
            return weather_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data for {city}: {e}")
            return None

    def store_weather_data(self, weather_data):
        """Store weather data in PostgreSQL database"""
        if not weather_data:
            return False

        try:
            df = pd.DataFrame([weather_data])
            df.to_sql('weather', self.engine, if_exists='append', index=False, method='multi')
            logger.info(f"Weather data stored successfully for {weather_data['city']}")
            return True

        except Exception as e:
            if "duplicate key" in str(e).lower():
                logger.warning(f"Weather data for {weather_data['city']} on {weather_data['weather_date']} already exists")
                return True
            else:
                logger.error(f"Error storing weather data: {e}")
                return False

    def generate_sample_data(self, city, days=30):
        """Generate sample historical weather data for testing"""
        logger.info(f"Generating {days} days of sample data for {city}")

        # Get current weather as baseline
        current_weather = self.fetch_current_weather(city)
        if not current_weather:
            logger.error("Cannot generate sample data without current weather reference")
            return

        base_temp = current_weather['temp_c']
        base_humidity = current_weather['humidity']

        sample_data = []
        for i in range(days, 0, -1):
            # Create realistic variations
            temp_variation = np.random.normal(0, 3)  # ±3°C variation
            humidity_variation = np.random.randint(-10, 11)  # ±10% variation

            sample_date = date.today() - timedelta(days=i)
            sample_weather = {
                'weather_date': sample_date,
                'city': city,
                'temp_c': round(base_temp + temp_variation, 2),
                'humidity': max(0, min(100, base_humidity + humidity_variation)),
                'description': np.random.choice(['clear sky', 'few clouds', 'scattered clouds', 'broken clouds', 'overcast clouds', 'light rain']),
                'pressure': round(1013 + np.random.normal(0, 10), 2),
                'wind_speed': round(np.random.uniform(0, 10), 2)
            }
            sample_data.append(sample_weather)

        # Store all sample data
        success_count = 0
        for data in sample_data:
            if self.store_weather_data(data):
                success_count += 1

        logger.info(f"Generated and stored {success_count}/{len(sample_data)} sample weather records")

    def run_etl(self, cities, generate_sample=False):
        """Run the complete ETL process"""
        logger.info("Starting Weather ETL Process")

        # Create table if needed
        self.create_table_if_not_exists()

        # Generate sample data if requested
        if generate_sample:
            import numpy as np
            for city in cities:
                self.generate_sample_data(city, 30)

        # Fetch and store current weather for all cities
        for city in cities:
            weather_data = self.fetch_current_weather(city)
            self.store_weather_data(weather_data)
            time.sleep(1)  # Rate limiting

        logger.info("Weather ETL Process completed")

def main():
    # Configuration - Replace with your actual values
    API_KEY = "e8d7a1e7181f327c2470638bd07ff0a1"  # Replace with your API key
    PG_CONN_STRING = "postgresql+psycopg2://postgres:Pranav%401072@localhost:5432/sales_weatherinfo_db"
    CITIES = ["Patna", "Delhi", "Mumbai", "Bangalore"]

    # Initialize ETL
    etl = WeatherETL(API_KEY, PG_CONN_STRING)

    # Run ETL with sample data generation for testing
    etl.run_etl(CITIES, generate_sample=True)

if __name__ == "__main__":
    main()
