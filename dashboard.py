import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def create_weather_df(df):
    weather = ["Clear, Few clouds, Partly cloudy, Partly cloudy",
           "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
           "Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
           "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog"
          ]

    weather_pivot = df.groupby('weathersit').agg({'cnt': ['mean']})
    weather_pivot.index = weather
    return weather_pivot

def create_day_df(df):
    # buat list untuk mengubah encoding day ke nama hari
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    day_pivot = df.groupby('weekday').cnt.max()
    day_pivot.index = [days[i] for i in day_pivot.index]
    return day_pivot

day_df = pd.read_csv('bike_dataset/day_clean.csv')
hour_df = pd.read_csv('bike_dataset/hour_clean.csv')

# Assess df
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])


min_date = day_df["dteday"].min()
max_date = hour_df["dteday"].max()
 
with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

main_day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

weather_pivot = create_weather_df(main_hour_df)
day_pivot = create_day_df(main_day_df)

st.header('Bike Sharing Analysis Dashboard')

# Weather part
st.header('Mean Count of Bikes Rented by Weather Situation')
fig, ax = plt.subplots(figsize=(10, 6))
weather_pivot.plot(kind='bar', ax=ax, legend=False)

plt.xlabel('Weather Situation')
plt.ylabel('Mean Count (cnt)')
plt.xticks(rotation=45, ha='right')

st.pyplot(fig)

# Display additional information
st.write("Information:")
st.write(f"- Maximum Mean Count: {weather_pivot['cnt']['mean'].max():.2f} on {weather_pivot.idxmax()[0]} weather")
st.write(f"- Minimum Mean Count: {weather_pivot['cnt']['mean'].min():.2f} on {weather_pivot.idxmin()[0]} weather")


# Based on day
st.subheader('Maximum Count of Bikes Rented by Day of the Week')
 
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['gray' if day != day_pivot.idxmax() and day != day_pivot.idxmin() else 'blue' if day == day_pivot.idxmax() else 'red' for day in day_pivot.index]
day_pivot.plot(kind='bar', ax=ax, color=colors)

plt.xlabel('Day of the Week')
plt.ylabel('Maximum Count (cnt)')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Display additional information
st.write("Information:")
st.write(f"- Highest Day: {day_pivot.idxmax()} with {day_pivot.max()} rentals")
st.write(f"- Lowest Day: {day_pivot.idxmin()} with {day_pivot.min()} rentals")