
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import numpy as np
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherVisualization:
    def __init__(self, pg_conn_string):
        self.engine = create_engine(pg_conn_string)

    def fetch_weather_data(self, city, days=30):
        """Fetch weather data for last N days"""
        query = f"""
        SELECT weather_date, temp_c, humidity, description, pressure, wind_speed 
        FROM weather 
        WHERE city = '{city}' 
        AND weather_date >= CURRENT_DATE - INTERVAL '{days} days'
        ORDER BY weather_date;
        """
        try:
            df = pd.read_sql(query, self.engine)
            logger.info(f"Fetched {len(df)} records for {city}")
            return df
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return pd.DataFrame()

    def plot_temperature_trend(self, df, city):
        """Create temperature trend visualization"""
        plt.figure(figsize=(12, 6))
        plt.plot(df['weather_date'], df['temp_c'], marker='o', linewidth=2, markersize=4)
        plt.title(f'Temperature Trend - {city} (Last 30 Days)', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Temperature (°C)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Add trend line
        if len(df) > 1:
            z = np.polyfit(range(len(df)), df['temp_c'], 1)
            p = np.poly1d(z)
            plt.plot(df['weather_date'], p(range(len(df))), "--", alpha=0.8, color='red', label='Trend')
            plt.legend()

        plt.savefig(f'{city}_temperature_trend.png', dpi=300, bbox_inches='tight')
        plt.show()

        return f'{city}_temperature_trend.png'

    def plot_weather_dashboard(self, df, city):
        """Create comprehensive weather dashboard"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Weather Dashboard - {city} (Last 30 Days)', fontsize=16, fontweight='bold')

        # Temperature plot
        axes[0,0].plot(df['weather_date'], df['temp_c'], 'b-', marker='o', markersize=3)
        axes[0,0].set_title('Temperature Trend')
        axes[0,0].set_ylabel('Temperature (°C)')
        axes[0,0].grid(True, alpha=0.3)
        axes[0,0].tick_params(axis='x', rotation=45)

        # Humidity plot
        axes[0,1].plot(df['weather_date'], df['humidity'], 'g-', marker='s', markersize=3)
        axes[0,1].set_title('Humidity Levels')
        axes[0,1].set_ylabel('Humidity (%)')
        axes[0,1].grid(True, alpha=0.3)
        axes[0,1].tick_params(axis='x', rotation=45)

        # Pressure plot (if available)
        if 'pressure' in df.columns and not df['pressure'].isna().all():
            axes[1,0].plot(df['weather_date'], df['pressure'], 'r-', marker='^', markersize=3)
            axes[1,0].set_title('Atmospheric Pressure')
            axes[1,0].set_ylabel('Pressure (hPa)')
        else:
            axes[1,0].text(0.5, 0.5, 'Pressure data\nnot available', 
                          ha='center', va='center', transform=axes[1,0].transAxes)
            axes[1,0].set_title('Atmospheric Pressure')
        axes[1,0].grid(True, alpha=0.3)
        axes[1,0].tick_params(axis='x', rotation=45)

        # Weather descriptions frequency
        if not df['description'].empty:
            desc_counts = df['description'].value_counts().head(5)
            axes[1,1].bar(range(len(desc_counts)), desc_counts.values, 
                         color=plt.cm.Set3(np.linspace(0, 1, len(desc_counts))))
            axes[1,1].set_title('Weather Conditions Frequency')
            axes[1,1].set_ylabel('Days')
            axes[1,1].set_xticks(range(len(desc_counts)))
            axes[1,1].set_xticklabels(desc_counts.index, rotation=45, ha='right')

        plt.tight_layout()
        plt.savefig(f'{city}_weather_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()

        return f'{city}_weather_dashboard.png'

    def generate_weather_summary(self, df, city):
        """Generate statistical summary"""
        if df.empty:
            return f"No data available for {city}"

        summary = {
            'City': city,
            'Date Range': f"{df['weather_date'].min()} to {df['weather_date'].max()}",
            'Average Temperature': f"{df['temp_c'].mean():.1f}°C",
            'Max Temperature': f"{df['temp_c'].max():.1f}°C",
            'Min Temperature': f"{df['temp_c'].min():.1f}°C",
            'Average Humidity': f"{df['humidity'].mean():.1f}%",
            'Most Common Weather': df['description'].mode().iloc[0] if not df['description'].empty else 'N/A',
            'Total Records': len(df)
        }

        return summary

    def create_visualizations(self, city="Patna"):
        """Create all visualizations for a city"""
        logger.info(f"Creating visualizations for {city}")

        # Fetch data
        df = self.fetch_weather_data(city, 30)

        if df.empty:
            logger.warning(f"No data found for {city}")
            return None

        # Generate visualizations
        temp_plot = self.plot_temperature_trend(df, city)
        dashboard_plot = self.plot_weather_dashboard(df, city)

        # Generate summary
        summary = self.generate_weather_summary(df, city)

        logger.info("Visualizations created successfully")

        return {
            'data': df,
            'summary': summary,
            'temperature_plot': temp_plot,
            'dashboard_plot': dashboard_plot
        }

def main():
    # Configuration
    PG_CONN_STRING = "postgresql+psycopg2://postgres:Pranav%401072@localhost:5432/sales_weatherinfo_db"

    # Create visualization instance
    viz = WeatherVisualization(PG_CONN_STRING)

    # Generate visualizations for Patna
    results = viz.create_visualizations("Patna")

    if results:
        print("\n=== WEATHER SUMMARY ===")
        for key, value in results['summary'].items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
