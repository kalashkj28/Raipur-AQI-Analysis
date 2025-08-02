import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Load the Data ---
# Make sure your CSV file name matches what you saved it as.
try:
    df = pd.read_csv('air_quality_data.csv')
    print("File loaded successfully!")
except FileNotFoundError:
    print("Error: Could not find 'air_quality_data.csv'. Make sure it's in the same folder as the script.")
    exit()

# --- Prepare the Data ---
# 1. Convert 'DATE' column to a proper date format
# df['DATE'] = pd.to_datetime(df['DATE'])
df['DATE'] = pd.to_datetime(df['DATE'], dayfirst=True, errors='coerce')
# 2. Ensure AQI is a numeric value, changing errors to 'Not a Number'
df['AQI'] = pd.to_numeric(df['AQI'], errors='coerce')

# 3. Drop rows where AQI is missing, as we can't analyze them
df.dropna(subset=['AQI'], inplace=True)

print("\nData cleaned and prepared. Here are the first few rows:")
print(df.head())

print("\nData Information:")
df.info()



# --- Filter for Raipur and the Last Year ---
df_raipur = df[df['City'] == 'Raipur'].copy()

# Check if Raipur data exists
if df_raipur.empty:
    print("\nError: No data found for the city 'Raipur' in the dataset.")
    exit()

# Define the date for "one year ago" from our current date
one_year_ago = datetime(2024, 2, 2)
df_raipur_last_year = df_raipur[df_raipur['DATE'] >= one_year_ago].copy()


# --- Answer Our Key Questions ---

# A. What was the average AQI in Raipur over the last year?
avg_aqi_raipur = df_raipur_last_year['AQI'].mean()
print(f"\n--- Analysis for Raipur (Last 12 Months) ---")
print(f"1. Average AQI: {avg_aqi_raipur:.2f}")


# B. Which months had the highest and lowest air pollution?
# We need to set the DATE as the index to group by month
df_raipur_last_year.set_index('DATE', inplace=True)
monthly_aqi = df_raipur_last_year['AQI'].resample('M').mean()

highest_aqi_month = monthly_aqi.idxmax()
lowest_aqi_month = monthly_aqi.idxmin()

print(f"2. Highest Pollution Month: {highest_aqi_month.strftime('%B %Y')} (Avg AQI: {monthly_aqi.max():.2f})")
print(f"3. Lowest Pollution Month: {lowest_aqi_month.strftime('%B %Y')} (Avg AQI: {monthly_aqi.min():.2f})")


# # C. How does Raipur's air quality compare to other cities?
# cities_to_compare = ['Raipur', 'Delhi', 'Mumbai']
# df_comparison = df[df['City'].isin(cities_to_compare) & (df['DATE'] >= one_year_ago)]
# comparison_avg = df_comparison.groupby('City')['AQI'].mean().sort_values(ascending=False)

# print("\n--- Comparative Analysis (Avg AQI Last Year) ---")
# print(comparison_avg)







# --- Visualization 1: Raipur's Monthly AQI Trend ---
plt.figure(figsize=(12, 6))
plt.plot(monthly_aqi.index, monthly_aqi.values, marker='o', linestyle='-', color='crimson')
plt.title('Monthly Average AQI Trend in Raipur (Last 12 Months)')
plt.xlabel('Month')
plt.ylabel('Average Air Quality Index (AQI)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))
plt.tight_layout()
plt.show()


# # --- Visualization 2: City Comparison Bar Chart ---
# plt.figure(figsize=(8, 6))
# comparison_avg.plot(kind='bar', color=['#D9534F', '#5BC0DE', '#5CB85C'])
# plt.title('Average AQI Comparison (Last 12 Months)')
# plt.xlabel('City')
# plt.ylabel('Average Air Quality Index (AQI)')
# plt.xticks(rotation=0) # Keeps city names horizontal
# plt.tight_layout()
# plt.show()