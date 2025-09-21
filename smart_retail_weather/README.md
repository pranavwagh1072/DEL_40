# Smart Retail Insights with Weather Integration

## Project Overview

This capstone project demonstrates a complete end-to-end data pipeline that fetches live weather data, stores it in PostgreSQL, visualizes historical trends, and performs machine learning-based weather forecasting.

## 🎯 Project Objectives

1. **Data Ingestion**: Fetch live weather data from OpenWeatherMap API and store in PostgreSQL
2. **Database Design**: Create and manage PostgreSQL databases and tables
3. **Data Visualization**: Implement comprehensive weather data visualization for last 30 days
4. **Machine Learning**: Use basic ML models for weather forecasting

## 📁 Project Structure

```
smart_retail_weather/
├── etl/
│   ├── weather_etl.py          # Weather data extraction and loading
│   └── __init__.py
├── visualization/
│   ├── weather_viz.py          # Data visualization scripts
│   └── __init__.py
├── ml/
│   ├── weather_forecast.py     # ML forecasting models
│   └── __init__.py
├── data/
│   └── sample_data.sql         # Sample data for testing
├── docs/
│   └── screenshots/            # Project screenshots
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── setup_database.sql          # Database setup script
└── run_project.py             # Main project runner
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- OpenWeatherMap API key (free registration at https://openweathermap.org/)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/smart_retail_weather.git
   cd smart_retail_weather
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup PostgreSQL Database**
   ```sql
   -- Connect to PostgreSQL as superuser
   CREATE DATABASE sales_weatherinfo_db;
   CREATE USER weather_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE sales_weatherinfo_db TO weather_user;
   ```

4. **Configure API Keys and Database Connection**

   Update the following in each script:
   - `API_KEY`: Your OpenWeatherMap API key
   - `PG_CONN_STRING`: Your PostgreSQL connection string

   Example:
   ```python
   API_KEY = "your_openweathermap_api_key_here"
   PG_CONN_STRING = "postgresql+psycopg2://postgres:password@localhost:5432/sales_weatherinfo_db"
   ```

## 🔧 Usage

### 1. Data Ingestion (ETL)

Run the ETL script to fetch and store weather data:

```bash
cd etl
python weather_etl.py
```

This script will:
- Create the necessary database tables
- Fetch current weather data for specified cities
- Generate sample historical data for testing (30 days)
- Store all data in PostgreSQL

### 2. Data Visualization

Create weather visualizations:

```bash
cd visualization
python weather_viz.py
```

Generates:
- Temperature trend charts
- Weather dashboard with multiple metrics
- Statistical summaries

### 3. ML Weather Forecasting

Run weather prediction models:

```bash
cd ml
python weather_forecast.py
```

Features:
- Linear Regression and Random Forest models
- 7-day weather forecasts
- Model performance metrics
- Forecast visualization plots

## 📊 Features

### Data Pipeline
- **Real-time data ingestion** from OpenWeatherMap API
- **Automated data storage** in PostgreSQL with error handling
- **Data quality validation** and duplicate prevention
- **Sample data generation** for testing and development

### Visualizations
- **Temperature trends** over the last 30 days
- **Multi-metric dashboard** (temperature, humidity, pressure, wind)
- **Weather condition frequency** analysis
- **Statistical summaries** and insights

### Machine Learning
- **Multiple ML models**: Linear Regression, Random Forest
- **Feature engineering**: Lag features, moving averages, time-based features
- **Model evaluation**: MAE, MSE, R² scores
- **Forecast visualization** with confidence indicators

### Database Design
```sql
CREATE TABLE weather (
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
```

## 📈 Sample Outputs

### Weather Dashboard
![Weather Dashboard](docs/screenshots/weather_dashboard.png)

### Temperature Forecasting
![Weather Forecast](docs/screenshots/weather_forecast.png)

### Database Tables
![PostgreSQL Database](docs/screenshots/postgresql_tables.png)

## 🔍 Technical Details

### API Integration
- **OpenWeatherMap API**: Current weather data with 5-day forecast capability
- **Rate limiting**: Built-in delays to respect API limits
- **Error handling**: Robust exception handling and logging
- **Data validation**: Ensures data quality and completeness

### Database Management
- **PostgreSQL**: Relational database with ACID compliance
- **SQLAlchemy ORM**: Database abstraction and connection management
- **Data integrity**: Primary keys, unique constraints, foreign keys
- **Performance optimization**: Indexing on frequently queried columns

### Machine Learning Pipeline
- **Data preprocessing**: Feature scaling, missing value handling
- **Feature engineering**: Time-based features, lag variables, moving averages
- **Model training**: Automated training with performance evaluation
- **Prediction pipeline**: End-to-end forecasting with visualization

## 🛠️ Development Notes

### Configuration Management
Update the following variables in each script:
- `API_KEY`: Your OpenWeatherMap API key
- `PG_CONN_STRING`: PostgreSQL connection string
- `CITIES`: List of cities to monitor

### Extending the Project
- **Additional cities**: Modify the `CITIES` list in ETL scripts
- **More features**: Add weather parameters like UV index, visibility
- **Advanced ML**: Implement LSTM, ARIMA for time series forecasting
- **Real-time dashboard**: Create web interface using Flask/Django

### Troubleshooting

1. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check connection string format
   - Ensure database and user exist

2. **API Key Problems**
   - Verify API key is valid and active
   - Check API rate limits
   - Ensure internet connectivity

3. **Missing Dependencies**
   - Run `pip install -r requirements.txt`
   - Use virtual environment for isolation

## 📝 Project Report

For detailed project documentation, implementation details, and results analysis, refer to the complete project report: `Smart_Retail_Weather_Integration_Report.pdf`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License

## 👨‍💻 Author

**Pranav Wagh**  
B.Tech CSE Student, MIT ADT University  
Email: pranavwagh1072@gmail.com  
LinkedIn: [Pranav Wagh](https://www.linkedin.com/in/pranav-wagh-1072psw)

---

*This project demonstrates practical application of data engineering, visualization, and machine learning concepts in a real-world weather analytics scenario.*
