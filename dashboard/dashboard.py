from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

sns.set_theme(style="whitegrid", palette="deep")

BASE_DIR = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = Path(__file__).resolve().parent
CLEAN_DATA_PATH = DASHBOARD_DIR / "all_data.csv"
RAW_DATA_PATH = BASE_DIR / "data" / "PRSA_Data_Aotizhongxin_20130301-20170228.csv"

NUMERIC_COLUMNS = [
    "PM2.5",
    "PM10",
    "SO2",
    "NO2",
    "CO",
    "O3",
    "TEMP",
    "PRES",
    "DEWP",
    "RAIN",
    "WSPM",
]

POLLUTION_LABELS = [
    "Baik",
    "Sedang",
    "Tidak Sehat untuk Sensitif",
    "Tidak Sehat",
    "Sangat Tidak Sehat",
]

SEASON_MAP = {
    12: "Winter",
    1: "Winter",
    2: "Winter",
    3: "Spring",
    4: "Spring",
    5: "Spring",
    6: "Summer",
    7: "Summer",
    8: "Summer",
    9: "Autumn",
    10: "Autumn",
    11: "Autumn",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    data_path = CLEAN_DATA_PATH if CLEAN_DATA_PATH.exists() else RAW_DATA_PATH
    df = pd.read_csv(data_path)

    df[NUMERIC_COLUMNS] = df[NUMERIC_COLUMNS].interpolate(limit_direction="both")
    df["wd"] = df["wd"].fillna(df["wd"].mode()[0])
    df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
    df["season"] = df["month"].map(SEASON_MAP)
    df["pollution_category"] = pd.cut(
        df["PM2.5"],
        bins=[-1, 35, 75, 115, 150, np.inf],
        labels=POLLUTION_LABELS,
    )

    return df


def filter_data(df: pd.DataFrame, year_range: tuple[int, int], seasons: list[str]) -> pd.DataFrame:
    filtered = df[df["year"].between(year_range[0], year_range[1])].copy()
    if seasons:
        filtered = filtered[filtered["season"].isin(seasons)]
    return filtered


def build_monthly_weather(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby(["year", "month"], as_index=False)
        .agg(total_rain=("RAIN", "sum"), avg_temp=("TEMP", "mean"), avg_pm25=("PM2.5", "mean"))
        .sort_values(["year", "month"])
    )
    monthly["avg_temp"] = monthly["avg_temp"].round(2)
    monthly["avg_pm25"] = monthly["avg_pm25"].round(2)
    return monthly


def build_season_pollution(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("season", as_index=False)
        .agg(avg_pm25=("PM2.5", "mean"), avg_pm10=("PM10", "mean"), avg_rain=("RAIN", "mean"))
        .round(2)
    )


def build_wind_pollution(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("wd", as_index=False)
        .agg(avg_pm25=("PM2.5", "mean"), observations=("wd", "size"))
        .query("observations >= 500")
        .sort_values("avg_pm25", ascending=False)
        .round(2)
    )


def build_yearly_mix(df: pd.DataFrame) -> pd.DataFrame:
    mix = (
        df.groupby(["year", "pollution_category"], observed=False)
        .size()
        .rename("count")
        .reset_index()
    )
    mix["share_pct"] = (
        mix["count"] / mix.groupby("year")["count"].transform("sum") * 100
    ).round(2)
    return mix


df = load_data()

min_year = int(df["year"].min())
max_year = int(df["year"].max())
season_options = ["Spring", "Summer", "Autumn", "Winter"]

with st.sidebar:
    st.title("Filter Dashboard")
    selected_years = st.slider(
        "Rentang tahun",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
    selected_seasons = st.multiselect(
        "Pilih musim",
        options=season_options,
        default=season_options,
    )
    st.caption(
        "Catatan: data tahun 2017 hanya tersedia sampai Februari, sehingga interpretasinya perlu lebih hati-hati."
    )

main_df = filter_data(df, selected_years, selected_seasons)
monthly_weather = build_monthly_weather(main_df)
season_pollution = build_season_pollution(main_df)
wind_pollution = build_wind_pollution(main_df)
yearly_mix = build_yearly_mix(main_df)

dominant_category = (
    main_df["pollution_category"].value_counts().idxmax()
    if not main_df.empty
    else "-"
)

st.title("Dashboard Analisis Kualitas Udara Aotizhongxin")
st.caption(
    "Dashboard ini merangkum pola hujan, temperatur, musim, arah angin, dan kategori kualitas udara berbasis PM2.5."
)

if main_df.empty:
    st.warning("Filter saat ini tidak menghasilkan data. Ubah rentang tahun atau musim.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata PM2.5", f"{main_df['PM2.5'].mean():.2f}")
col2.metric("Rata-rata PM10", f"{main_df['PM10'].mean():.2f}")
col3.metric("Total Curah Hujan", f"{main_df['RAIN'].sum():.1f}")
col4.metric("Kategori Dominan", str(dominant_category))

st.markdown("### Pertanyaan 1: Pola Hujan dan Temperatur")

fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
sns.lineplot(
    data=monthly_weather,
    x="month",
    y="total_rain",
    hue="year",
    marker="o",
    palette="Blues",
    ax=axes[0],
)
axes[0].set_title("Total Curah Hujan Bulanan per Tahun")
axes[0].set_xlabel("Bulan")
axes[0].set_ylabel("Total Curah Hujan")
axes[0].set_xticks(range(1, 13))
axes[0].legend(title="Tahun", ncol=3)

sns.lineplot(
    data=monthly_weather,
    x="month",
    y="avg_temp",
    hue="year",
    marker="o",
    palette="flare",
    ax=axes[1],
    legend=False,
)
axes[1].set_title("Rata-rata Temperatur Bulanan per Tahun")
axes[1].set_xlabel("Bulan")
axes[1].set_ylabel("Temperatur Rata-rata")
axes[1].set_xticks(range(1, 13))

plt.tight_layout()
st.pyplot(fig)

peak_rain = monthly_weather.loc[monthly_weather.groupby("year")["total_rain"].idxmax()].copy()
peak_rain["total_rain"] = peak_rain["total_rain"].round(2)
st.dataframe(
    peak_rain.rename(
        columns={"year": "Tahun", "month": "Bulan Puncak Hujan", "total_rain": "Total Curah Hujan"}
    ),
    width="stretch",
)

st.markdown("### Pertanyaan 2: Musim dan Arah Angin yang Berkaitan dengan Polusi")

col_left, col_right = st.columns(2)

with col_left:
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(
        data=season_pollution,
        x="season",
        y="avg_pm25",
        order=season_options,
        color="#d95f02",
        ax=ax,
    )
    ax.set_title("Rata-rata PM2.5 per Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata PM2.5")
    st.pyplot(fig)

with col_right:
    fig, ax = plt.subplots(figsize=(7, 5))
    top_wind_pollution = wind_pollution.head(8)
    sns.barplot(
        data=top_wind_pollution,
        x="wd",
        y="avg_pm25",
        palette="crest",
        ax=ax,
    )
    ax.set_title("8 Arah Angin dengan PM2.5 Tertinggi")
    ax.set_xlabel("Arah Angin")
    ax.set_ylabel("Rata-rata PM2.5")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)

st.dataframe(
    wind_pollution.head(10).rename(
        columns={"wd": "Arah Angin", "avg_pm25": "Rata-rata PM2.5", "observations": "Jumlah Observasi"}
    ),
    width="stretch",
)

st.markdown("### Analisis Lanjutan: Manual Grouping / Binning Kategori PM2.5")

category_share = (
    main_df["pollution_category"].value_counts(normalize=True).mul(100).round(2).reindex(POLLUTION_LABELS)
)
category_pivot = (
    yearly_mix.pivot(index="year", columns="pollution_category", values="share_pct")
    .reindex(columns=POLLUTION_LABELS)
    .fillna(0)
)

col_left, col_right = st.columns(2)

with col_left:
    fig, ax = plt.subplots(figsize=(7, 5))
    category_share.reset_index().rename(
        columns={"index": "pollution_category", "pollution_category": "share_pct"}
    )
    category_share.plot(
        kind="bar",
        color=["#2a9d8f", "#8ab17d", "#e9c46a", "#f4a261", "#e76f51"],
        ax=ax,
    )
    ax.set_title("Distribusi Kategori PM2.5")
    ax.set_xlabel("Kategori")
    ax.set_ylabel("Persentase (%)")
    ax.tick_params(axis="x", rotation=30)
    st.pyplot(fig)

with col_right:
    fig, ax = plt.subplots(figsize=(9, 5))
    category_pivot.plot(
        kind="bar",
        stacked=True,
        color=["#2a9d8f", "#8ab17d", "#e9c46a", "#f4a261", "#e76f51"],
        ax=ax,
    )
    ax.set_title("Komposisi Kategori PM2.5 per Tahun")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Persentase (%)")
    ax.legend(title="Kategori", bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig)

unhealthy_share = category_share.loc[
    ["Tidak Sehat untuk Sensitif", "Tidak Sehat", "Sangat Tidak Sehat"]
].sum()

st.info(
    f"Proporsi gabungan kondisi udara yang berisiko mencapai {unhealthy_share:.2f}% pada filter yang sedang dipilih."
)
