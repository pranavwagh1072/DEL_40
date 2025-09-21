
"""
Smart Retail Weather Integration - Main Project Runner

This script orchestrates the complete weather data pipeline:
1. ETL: Fetch and store weather data
2. Visualization: Generate charts and analysis
3. ML Forecasting: Predict future weather patterns

Author: Your Name
Date: September 2025
"""

import sys
import os
import logging
from datetime import datetime

# Add project directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'visualization'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weather_project.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print project banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        Smart Retail Insights with Weather Integration        ║
    ║                    Capstone Project 1                        ║
    ║                                                              ║
    ║    Weather Data Pipeline & ML Forecasting System             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"Project Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

def run_etl_pipeline():
    """Run the ETL pipeline"""
    try:
        logger.info("Starting ETL Pipeline...")

        # Import and run ETL
        import sys
        sys.path.insert(0, r'd:\DEL\Capstone_Project\smart_retail_weather\et1')
        from weather_etl import WeatherETL

        # Configuration
        API_KEY = "e8d7a1e7181f327c2470638bd07ff0a1"  # Replace with actual key
        PG_CONN_STRING = "postgresql+psycopg2://postgres:Pranav%401072@localhost:5432/sales_weatherinfo_db"
        CITIES = ["Patna", "Delhi", "Mumbai", "Bangalore"]

        # Initialize and run ETL
        etl = WeatherETL(API_KEY, PG_CONN_STRING)
        etl.run_etl(CITIES, generate_sample=True)

        logger.info("✅ ETL Pipeline completed successfully")
        return True

    except Exception as e:
        logger.error(f" ETL Pipeline failed: {e}")
        return False

def run_visualization():
    """Run data visualization"""
    try:
        logger.info("Starting Data Visualization...")

        # Import and run visualization
        from weather_viz import WeatherVisualization

        PG_CONN_STRING = "postgresql+psycopg2://postgres:Pranav%401072@localhost:5432/sales_weatherinfo_db"

        # Create visualizations
        viz = WeatherVisualization(PG_CONN_STRING)
        results = viz.create_visualizations("Patna")

        if results:
            logger.info("✅ Data Visualization completed successfully")
            return True
        else:
            logger.warning("⚠️ Data Visualization completed with warnings")
            return False

    except Exception as e:
        logger.error(f" Data Visualization failed: {e}")
        return False

def run_ml_forecasting():
    """Run ML forecasting"""
    try:
        logger.info("Starting ML Weather Forecasting...")

        # Import and run ML forecasting
        from weather_forecast import WeatherForecasting

        PG_CONN_STRING = "postgresql+psycopg2://postgres:Pranav%401072@localhost:5432/sales_weatherinfo_db"

        # Create and run forecasting
        forecaster = WeatherForecasting(PG_CONN_STRING)
        results = forecaster.run_forecasting_pipeline("Patna", 7)

        if results:
            logger.info(" ML Weather Forecasting completed successfully")
            return True
        else:
            logger.warning(" ML Weather Forecasting completed with warnings")
            return False

    except Exception as e:
        logger.error(f" ML Weather Forecasting failed: {e}")
        return False

def generate_project_summary():
    """Generate project execution summary"""
    summary = """

    ╔══════════════════════════════════════════════════════════════╗
    ║                     PROJECT EXECUTION SUMMARY                ║
    ╚══════════════════════════════════════════════════════════════╝

      Deliverables Generated:
    ├──  PostgreSQL Database: sales_weatherinfo_db
    ├──  Temperature Trend Charts
    ├──  Weather Dashboard Visualizations  
    ├──  ML Forecast Models (Linear Regression, Random Forest)
    ├──  Statistical Weather Summary
    └──  Project Logs: weather_project.log

      Files Created:
    ├── Patna_temperature_trend.png
    ├── Patna_weather_dashboard.png
    ├── Patna_weather_forecast.png
    └── weather_project.log


    
    """
    print(summary)
    logger.info("Project execution summary generated")

def main():
    """Main project execution function"""
    print_banner()

    # Track execution results
    results = {
        'etl': False,
        'visualization': False,
        'ml_forecasting': False
    }

    try:
        # Step 1: ETL Pipeline
        print("\n Step 1: Running ETL Pipeline...")
        results['etl'] = run_etl_pipeline()

        # Step 2: Data Visualization
        print("\n Step 2: Generating Visualizations...")
        results['visualization'] = run_visualization()

        # Step 3: ML Forecasting
        print("\n Step 3: Running ML Forecasting...")
        results['ml_forecasting'] = run_ml_forecasting()

        # Generate summary
        print("\n Generating Project Summary...")
        generate_project_summary()

        # Final status
        successful_steps = sum(results.values())
        total_steps = len(results)

        print(f"\n Project Execution Status: {successful_steps}/{total_steps} steps completed successfully")

        if successful_steps == total_steps:
            print(" ALL STEPS COMPLETED SUCCESSFULLY!")
            logger.info("Project completed successfully")
        else:
            print("  Some steps completed with issues. Check logs for details.")
            logger.warning("Project completed with some issues")

    except Exception as e:
        logger.error(f"Critical error in main execution: {e}")
        print(f" Critical Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
