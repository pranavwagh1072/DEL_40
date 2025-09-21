
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import logging
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherForecasting:
    def __init__(self, pg_conn_string):
        self.engine = create_engine(pg_conn_string)
        self.models = {}
        self.scalers = {}

    def fetch_training_data(self, city):
        """Fetch historical weather data for training"""
        query = query = f"""
SELECT weather_date, temp_c, humidity FROM weather WHERE city = '{city}' ORDER BY weather_date;
"""


        try:
            df = pd.read_sql(query, self.engine)
            logger.info(f"Fetched {len(df)} training records for {city}")
            return df
        except Exception as e:
            logger.error(f"Error fetching training data: {e}")
            return pd.DataFrame()

    def prepare_features(self, df):
        """Prepare features for ML models"""
        if df.empty:
            return np.array([]), np.array([])

        # Convert dates to ordinal numbers
        df['date_ordinal'] = pd.to_datetime(df['weather_date']).apply(lambda x: x.toordinal())

        # Create lag features (previous day values)
        df['temp_lag1'] = df['temp_c'].shift(1)
        df['humidity_lag1'] = df['humidity'].shift(1)

        # Create moving averages
        df['temp_ma3'] = df['temp_c'].rolling(window=3).mean()
        df['temp_ma7'] = df['temp_c'].rolling(window=7).mean()

        # Create time-based features
        df['day_of_year'] = pd.to_datetime(df['weather_date']).dt.dayofyear
        df['month'] = pd.to_datetime(df['weather_date']).dt.month

        # Select features (handle missing values)
        feature_columns = ['date_ordinal', 'humidity', 'day_of_year', 'month']

        # Add lag features if available
        if 'temp_lag1' in df.columns and not df['temp_lag1'].isna().all():
            feature_columns.extend(['temp_lag1', 'humidity_lag1'])

        # Add pressure and wind if available
        if 'pressure' in df.columns and not df['pressure'].isna().all():
            feature_columns.append('pressure')
        if 'wind_speed' in df.columns and not df['wind_speed'].isna().all():
            feature_columns.append('wind_speed')

        # Add moving averages if available
        if len(df) >= 7:
            feature_columns.extend(['temp_ma3', 'temp_ma7'])

        # Drop rows with NaN values
        df_clean = df.dropna(subset=feature_columns + ['temp_c'])

        if df_clean.empty:
            logger.warning("No clean data available after feature preparation")
            return np.array([]), np.array([])

        X = df_clean[feature_columns].values
        y = df_clean['temp_c'].values

        logger.info(f"Prepared features: {feature_columns}")
        logger.info(f"Training data shape: X{X.shape}, y{y.shape}")

        return X, y, feature_columns, df_clean

    def train_models(self, X, y, city):
        """Train multiple ML models"""
        if len(X) == 0 or len(y) == 0:
            logger.error("No training data available")
            return

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        self.scalers[city] = scaler

        # Initialize models
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }

        # Train models
        trained_models = {}
        model_scores = {}

        for name, model in models.items():
            try:
                model.fit(X_scaled, y)

                # Make predictions on training data
                y_pred = model.predict(X_scaled)

                # Calculate metrics
                mae = mean_absolute_error(y, y_pred)
                mse = mean_squared_error(y, y_pred)
                r2 = r2_score(y, y_pred)

                trained_models[name] = model
                model_scores[name] = {'MAE': mae, 'MSE': mse, 'R2': r2}

                logger.info(f"{name} - MAE: {mae:.2f}, MSE: {mse:.2f}, R2: {r2:.3f}")

            except Exception as e:
                logger.error(f"Error training {name}: {e}")

        self.models[city] = trained_models
        return model_scores

    def generate_forecasts(self, city, days=7):
        """Generate weather forecasts"""
        if city not in self.models or not self.models[city]:
            logger.error(f"No trained models available for {city}")
            return None

        # Fetch latest data
        df = self.fetch_training_data(city)
        if df.empty:
            return None

        # Prepare features
        result = self.prepare_features(df)
        if len(result) != 4:
            return None

        X, y, feature_columns, df_clean = result

        if len(X) == 0:
            return None

        # Get the latest record
        latest_record = df_clean.iloc[-1]
        last_date = latest_record['weather_date']

        # Generate forecast dates
        forecast_dates = [last_date + timedelta(days=i) for i in range(1, days + 1)]

        forecasts = {}

        for model_name, model in self.models[city].items():
            predictions = []

            for i, forecast_date in enumerate(forecast_dates):
                # Create features for forecast
                date_ordinal = forecast_date.toordinal()
                day_of_year = forecast_date.timetuple().tm_yday
                month = forecast_date.month

                # Use latest available values for other features
                humidity = latest_record['humidity'] if 'humidity' in latest_record else 50

                # Build feature vector
                feature_vector = [date_ordinal, humidity, day_of_year, month]

                # Add other features if they were used in training
                if 'temp_lag1' in feature_columns:
                    temp_lag = latest_record['temp_c'] if i == 0 else predictions[-1]
                    feature_vector.extend([temp_lag, humidity])

                if 'pressure' in feature_columns:
                    feature_vector.append(latest_record.get('pressure', 1013))

                if 'wind_speed' in feature_columns:
                    feature_vector.append(latest_record.get('wind_speed', 5))

                if 'temp_ma3' in feature_columns:
                    feature_vector.extend([latest_record.get('temp_ma3', latest_record['temp_c']),
                                         latest_record.get('temp_ma7', latest_record['temp_c'])])

                # Ensure feature vector has correct length
                feature_vector = feature_vector[:len(feature_columns)]
                if len(feature_vector) < len(feature_columns):
                    # Pad with mean values if needed
                    feature_vector.extend([0] * (len(feature_columns) - len(feature_vector)))

                # Scale and predict
                feature_vector = np.array(feature_vector).reshape(1, -1)
                feature_vector_scaled = self.scalers[city].transform(feature_vector)
                prediction = model.predict(feature_vector_scaled)[0]
                predictions.append(round(prediction, 2))

            forecasts[model_name] = predictions

        return {
            'dates': forecast_dates,
            'forecasts': forecasts,
            'historical_data': df_clean[['weather_date', 'temp_c']].tail(10)
        }

    def plot_forecasts(self, city, forecast_results):
        """Plot historical data and forecasts"""
        if not forecast_results:
            logger.error("No forecast results to plot")
            return

        plt.figure(figsize=(14, 8))

        # Plot historical data
        hist_data = forecast_results['historical_data']
        plt.plot(hist_data['weather_date'], hist_data['temp_c'], 
                'o-', label='Historical', linewidth=2, markersize=5)

        # Plot forecasts
        forecast_dates = forecast_results['dates']
        colors = ['red', 'green', 'blue', 'orange']

        for i, (model_name, predictions) in enumerate(forecast_results['forecasts'].items()):
            plt.plot(forecast_dates, predictions, 
                    '--', label=f'{model_name} Forecast', 
                    linewidth=2, color=colors[i % len(colors)], marker='s', markersize=4)

        plt.title(f'Weather Forecast - {city}', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Temperature (°C)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot
        plot_filename = f'{city}_weather_forecast.png'
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        plt.show()

        return plot_filename

    def run_forecasting_pipeline(self, city="Patna", forecast_days=7):
        """Run complete forecasting pipeline"""
        logger.info(f"Starting weather forecasting for {city}")

        # Fetch and prepare data
        df = self.fetch_training_data(city)
        if df.empty:
            logger.error(f"No training data available for {city}")
            return None

        result = self.prepare_features(df)
        if len(result) != 4:
            logger.error("Failed to prepare features")
            return None

        X, y, feature_columns, df_clean = result

        if len(X) == 0:
            logger.error("No valid training data after feature preparation")
            return None

        # Train models
        model_scores = self.train_models(X, y, city)

        # Generate forecasts
        forecast_results = self.generate_forecasts(city, forecast_days)

        if forecast_results:
            # Plot results
            plot_file = self.plot_forecasts(city, forecast_results)

            # Print forecast summary
            print(f"\n=== WEATHER FORECAST FOR {city.upper()} ===")
            print(f"Forecast Period: {forecast_results['dates'][0]} to {forecast_results['dates'][-1]}")

            for model_name, predictions in forecast_results['forecasts'].items():
                avg_temp = np.mean(predictions)
                print(f"\n{model_name}:")
                print(f"  Average Forecasted Temperature: {avg_temp:.1f}°C")
                print(f"  Temperature Range: {min(predictions):.1f}°C - {max(predictions):.1f}°C")

            print(f"\n=== MODEL PERFORMANCE ===")
            if model_scores:
                for model_name, scores in model_scores.items():
                    print(f"{model_name}: MAE={scores['MAE']:.2f}°C, R²={scores['R2']:.3f}")

            return {
                'forecast_results': forecast_results,
                'model_scores': model_scores,
                'plot_file': plot_file
            }

        return None

def main():
    # Configuration
    PG_CONN_STRING = "postgresql+psycopg2://postgres:Pranav%401072@localhost:5432/sales_weatherinfo_db"

    # Create forecasting instance
    forecaster = WeatherForecasting(PG_CONN_STRING)

    # Run forecasting pipeline
    results = forecaster.run_forecasting_pipeline("Patna", 7)

    if results:
        logger.info("Weather forecasting completed successfully")
    else:
        logger.error("Weather forecasting failed")

if __name__ == "__main__":
    main()
