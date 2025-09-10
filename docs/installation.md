# Instalasi dan Setup

## Persyaratan Sistem
- Python 3.8 atau lebih baru
- pip (Python package installer)
- Virtual environment (opsional tapi direkomendasikan)

## Langkah Instalasi

1. Clone repository
```bash
git clone [url-repository]
cd ecommerce_dashboard
```

2. Buat dan aktifkan virtual environment (opsional)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi
```bash
streamlit run app.py
```

## Format Data
File CSV yang diupload harus memiliki kolom-kolom berikut:
- `InvoiceNo`: Nomor invoice untuk setiap transaksi
- `StockCode`: Kode produk
- `Description`: Deskripsi produk
- `Quantity`: Jumlah item yang dibeli
- `InvoiceDate`: Tanggal dan waktu transaksi
- `UnitPrice`: Harga per unit
- `CustomerID`: ID unik customer
- `Country`: Negara tempat pengiriman

## Troubleshooting

### Memory Error saat Market Basket Analysis
Jika mengalami memory error, coba:
1. Kurangi jumlah data yang dianalisis
2. Tingkatkan threshold minimum support
3. Filter produk yang jarang muncul

### Data Format Error
1. Pastikan format tanggal sesuai
2. Pastikan tidak ada nilai negatif di Quantity
3. Pastikan CustomerID tidak null untuk analisis customer
