# Proyek Analisis Data: Air Quality Dataset

## Setup dengan uv
```bash
uv init .
uv add pandas matplotlib seaborn streamlit jupyter nbformat
```

## Menjalankan notebook
```bash
uv run jupyter notebook
```

## Menjalankan dashboard Streamlit
```bash
uv run streamlit run dashboard/dashboard.py
```

## Deploy ke Streamlit Cloud
1. Push repository ini ke GitHub.
2. Buat app baru di Streamlit Cloud.
3. Pilih repository dan branch yang berisi proyek ini.
4. Gunakan entrypoint `dashboard/dashboard.py`.
5. Pastikan dependensi diambil dari `pyproject.toml` atau `requirements.txt`.
