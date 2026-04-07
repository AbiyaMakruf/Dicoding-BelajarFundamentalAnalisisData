# Checklist Kriteria Submission

## Kriteria Wajib

- [x] Menggunakan dataset yang disediakan Dicoding.
  Dataset yang dipakai adalah Air Quality Dataset pada `data/PRSA_Data_Aotizhongxin_20130301-20170228.csv`.

- [x] Melakukan seluruh proses analisis data dari pertanyaan bisnis sampai kesimpulan.
  Notebook sudah mencakup pertanyaan bisnis, data wrangling, EDA, visualisasi, analisis lanjutan, dan conclusion.

- [x] Minimal memiliki 2 pertanyaan bisnis.
  Notebook sekarang memiliki 3 pertanyaan bisnis yang eksplisit.

- [x] Minimal memiliki 2 visualisasi data.
  Notebook berisi beberapa visualisasi: hujan bulanan, temperatur bulanan, PM2.5 per musim, PM2.5 per arah angin, distribusi kategori polusi, dan komposisi kategori per tahun.

- [x] Proses analisis dibuat dalam notebook yang rapi.
  File `Proyek_Analisis_Data.ipynb` telah dirapikan, memakai path lokal proyek, markdown penjelas di setiap tahap, dan kesimpulan yang spesifik.

- [x] Membuat dashboard sederhana menggunakan Streamlit.
  Dashboard tersedia di `dashboard/dashboard.py`.

- [x] Dashboard dapat dijalankan secara lokal.
  Jalankan dengan `uv run streamlit run dashboard/dashboard.py`.

## Kriteria Tambahan untuk Nilai Tinggi

- [x] Notebook memiliki dokumentasi markdown/text cell yang menjelaskan setiap tahapan.
  Setiap bagian analisis kini memiliki markdown penjelas, bukan hanya kode.

- [x] Visualisasi dibuat lebih baik dan lebih efektif.
  Visualisasi sekarang fokus pada keterbacaan, konsistensi tema, label yang jelas, dan hubungan langsung dengan pertanyaan bisnis.

- [x] Menerapkan teknik analisis lanjutan yang relevan tanpa machine learning.
  Notebook dan dashboard memakai manual grouping/binning untuk membentuk kategori kualitas udara berbasis PM2.5.

- [x] Dashboard dibuat siap deploy ke Streamlit Cloud.
  Repository sudah memiliki `pyproject.toml`, `uv.lock`, README berbasis `uv`, dan `.streamlit/config.toml`.

- [ ] Dashboard sudah benar-benar dipublikasikan di Streamlit Cloud.
  Belum dapat diselesaikan langsung dari workspace ini karena membutuhkan proses publish ke akun Streamlit Cloud/GitHub milik Anda.

## Ringkasan

Secara teknis, seluruh kriteria wajib sudah terpenuhi dan mayoritas poin tambahan yang berada dalam kendali workspace ini sudah dikerjakan. Satu-satunya bagian yang masih memerlukan tindakan manual di luar workspace adalah publish dashboard ke Streamlit Cloud.
