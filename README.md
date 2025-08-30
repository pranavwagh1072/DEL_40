# Movie Rental Data Lifecycle

## Overview
This mini project demonstrates the lifecycle of data handling in a retail/movie rental context, covering the stages of capture, storage, processing, analysis, and visualization.

## Dataset
The project uses a CSV file named `movie_rentals.csv` containing rental transactions with the following columns:
- RentalID: Unique identifier for each rental transaction
- Date: Date of rental
- Customer: Name of the customer
- Movie: Movie rented
- DaysRented: Number of days the movie was rented
- PricePerDay: Rental price per day

## Project Structure
- **Data Capture & Storage:** Loading the data from the CSV file.
- **Data Processing / Cleaning:** Checking for missing values and calculating the total rental amount for each transaction.
- **Data Analysis:** 
  - Calculating total rental revenue.
  - Identifying the most rented movie.
  - Calculating total spending per customer.
- **Data Visualization:**
  - Bar chart showing revenue by movie.
  - Pie chart showing customer contributions to rental revenue.

## Usage
1. Ensure you have Python installed with `pandas` and `matplotlib` libraries.
2. Place `movie_rentals.csv` and `movie_rentals_analysis.py` in the same folder.
3. Run the script:
python movie_rentals_analysis.py
4. Review console output for analysis results and visualizations.

## Dependencies
- pandas
- matplotlib

## Credits
Developed as a sample project illustrating a data lifecycle process for retail/movies rentals.

---

Pipeline completes with a confirmation message indicating successful execution.
