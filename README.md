# Submission Dicoding "Belajar Analisis Data dengan Python" Bangkit 2024

## Deskripsi
Submission ini bertujuan untuk menganalisis data **E-Commerce Public Dataset** sebagai bagian dari program **Bangkit 2024**. Analisis ini mencakup eksplorasi data dan visualisasi untuk memberikan wawasan yang bermanfaat tentang perilaku e-commerce, performa penjualan, dan distribusi pelanggan.

## Struktur Direktori
```
/Dataset
    └── Berisi file data dalam format .csv yang digunakan untuk analisis.

/Dashboard
    └── dashboard.py - Berisi script untuk membuat dashboard interaktif menggunakan Streamlit.

/.ipynb_checkpoints
    └── Notebook.ipynb - Jupyter Notebook yang digunakan untuk melakukan analisis data dan visualisasi.
```

## Setup Environment
Untuk menjalankan proyek ini baik di **Google Colab** maupun **Streamlit**, ikuti langkah-langkah berikut:

### 1. Google Colab
#### a. Mount Google Drive:
Pertama, mount Google Drive Anda untuk menyimpan dan mengakses file yang diperlukan:

```python
from google.colab import drive
drive.mount('/content/drive')
```

#### b. Install Streamlit:
Streamlit harus diinstall di lingkungan Google Colab untuk menjalankan dashboard.

```bash
!pip install streamlit -q
```

#### c. Jalankan Streamlit:
Jalankan Streamlit dan buat tunneling untuk mengakses aplikasi di browser.

```bash
!streamlit run dashboard.py & npx localtunnel --port 8501
```

Tunggu hingga link lokal yang dihasilkan muncul, lalu klik untuk mengakses dashboard interaktif Anda.
