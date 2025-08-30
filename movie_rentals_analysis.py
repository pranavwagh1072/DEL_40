
"""

Mini Project: Movie Rental Data Lifecycle

Covers Capture → Storage → Processing → Analysis → Visualization

"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import matplotlib.pyplot as plt


# 1. DATA CAPTURE & STORAGE


print("Loading data from movie_rentals.csv...")

movie_df = pd.read_csv("movie_rentals.csv")


# 2. DATA PROCESSING / CLEANING


print("--- Data Cleaning ---")
print("Checking for missing values:")
print(movie_df.isnull().sum())

# Handle missing values if any (fill with 0 for DaysRented, 0 for PricePerDay)
movie_df["DaysRented"] = movie_df["DaysRented"].fillna(0)
movie_df["PricePerDay"] = movie_df["PricePerDay"].fillna(0)


# Calculate Total amount for each rental
movie_df["Total"] = movie_df["DaysRented"] * movie_df["PricePerDay"]

print("Data after cleaning and adding Total column:")
print(movie_df.head())


# 3. DATA ANALYSIS

print("--- Data Analysis ---")
total_revenue = movie_df["Total"].sum()
print(f"Total Rental Revenue: ₹{total_revenue}")

best_movie = movie_df.groupby("Movie")["Total"].sum().idxmax()
print(f"Most Rented Movie: {best_movie}")

customer_spending = movie_df.groupby("Customer")["Total"].sum().sort_values(ascending=False)
print("Customer Spending:")
print(customer_spending)


# 4. DATA VISUALIZATION


print("--- Generating Visualizations ---")

# Movie-wise revenue bar chart
movie_sales = movie_df.groupby("Movie")["Total"].sum()
movie_sales.plot(kind="bar", title="Revenue by Movie", ylabel="Revenue (₹)", xlabel="Movie", color="lightgreen")
plt.show()

# Customer spending pie chart
customer_spending.plot(kind="pie", autopct='%1.1f%%', title="Customer Contribution to Rental Revenue")
plt.ylabel("")  # Hide y-label for better look
plt.show()

print("Pipeline Completed Successfully ✅")
