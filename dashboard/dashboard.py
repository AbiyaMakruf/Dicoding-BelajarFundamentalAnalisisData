# NAMA  : Muhammad Abiya Makruf
# Username  : abiyamf

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper functions untuk membuat dataframe baru
def create_rain_frequency_df(df):
    rain_frequency = df.groupby(['year', 'month'])['RAIN'].sum().reset_index()
    return rain_frequency

# Helper functions untuk membuat dataframe baru
def create_temp_summary_df(df):
    temp_summary = df.groupby(['year', 'month'])['TEMP'].agg(['min', 'max']).reset_index()
    temp_summary['max'] = temp_summary['max'].round(2)
    return temp_summary

# Load data
df = pd.read_csv('all_data.csv')

# Membuat sidebar
dfCopy = df.copy()
dfCopy['year'] = pd.to_datetime(df['year'], format='%Y')

min_date = dfCopy["year"].min()
max_date = dfCopy["year"].max()
min_year = min_date.year
max_year = max_date.year

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://i.ibb.co/PDRjwTK/1-Converted-01.png")

    # # Mengambil start_date & end_date dari date_input
    # start_date, end_date = st.date_input(
    #     label='Rentang Waktu',min_value=min_date,
    #     max_value=max_date,
    #     value=[min_date, max_date]
    # )

    start_year, end_year = st.slider(
    label='Rentang Tahun',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
    )

# Filter Dataset
main_df = df[(df["year"] >= int(str(start_year)[:4])) & (df["year"] <= int(str(end_year)[:4]))]

# Membuat dataframe baru
rain_frequency_df = create_rain_frequency_df(main_df)
temp_summary_df = create_temp_summary_df(main_df)

# Judul Dashboard
st.header('Rain and Temperature Dashboard :sparkles:')

# Menampilkan visualisasi data untuk rain frequency
st.subheader('Rain Frequency')
 
col1, col2 = st.columns(2)
 
with col1:
    # Mengelompokkan data berdasarkan tahun dan bulan, dan menghitung jumlah hujan setiap bulan untuk setiap tahun
    rain_frequency = rain_frequency_df.groupby(['year', 'month'])['RAIN'].sum().reset_index()

    # Menemukan bulan dengan jumlah hujan tertinggi untuk setiap tahun
    most_rainy_month_per_year = rain_frequency.loc[rain_frequency.groupby('year')['RAIN'].idxmax()]

    # Add a new column "nomor" to represent the index of the DataFrame
    most_rainy_month_per_year['nomor'] = most_rainy_month_per_year.index + 1

    # Print result as a table using Streamlit
    st.write("Most Rainy Month Per Year:")
    st.dataframe(most_rainy_month_per_year[['nomor', 'year', 'month']])
 

# Membuat visualisasi dengan bar plot
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'lime', 'brown', 'pink']  # Warna yang berbeda untuk setiap bulan
for i, month in enumerate(range(1, 13)):
    month_data = rain_frequency_df[rain_frequency_df['month'] == month]
    ax.bar(month_data['year'], month_data['RAIN'], color=colors[i % len(colors)], label=f'Month {month}')

ax.set_xlabel('Year')
ax.set_ylabel('Rainfall Count')
ax.set_title('Monthly Rainfall Count for Each Year')
ax.set_xticks(rain_frequency_df['year'].unique())
ax.legend(title='Month', loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Menampilkan plot menggunakan Streamlit
st.pyplot(fig)

# Menampilkan visualisasi data untuk temp summary
st.subheader('Temperature')
 
col1, col2 = st.columns(2)
 
with col1:
    # Menampilkan data temperatur minimum dan maksimum per bulan untuk setiap tahun
    st.write('Temperature Summary:')
    min_temp = temp_summary_df.groupby('year')['min'].min().reset_index()
    max_temp = temp_summary_df.groupby('year')['max'].max().reset_index()
    temp_summary = pd.merge(min_temp, max_temp, on='year')
    temp_summary.columns = ['Year', 'Min Temperature', 'Max Temperature']
    st.dataframe(temp_summary)

# Create a figure and axis object
fig, ax = plt.subplots(figsize=(10, 6))

# Loop through unique years in the DataFrame
for year in temp_summary_df['year'].unique():
    year_data = temp_summary_df[temp_summary_df['year'] == year]
    ax.scatter(year_data['month'], year_data['min'], label=f'Min Temperature ({year})', marker='o')
    ax.scatter(year_data['month'], year_data['max'], label=f'Max Temperature ({year})', marker='x')

# Set labels and title
ax.set_xlabel('Month')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Min and Max Temperature per Month')
ax.set_xticks(range(1, 13))
ax.legend()
ax.grid(True)
plt.tight_layout()

# Display plot using Streamlit
st.pyplot(fig)