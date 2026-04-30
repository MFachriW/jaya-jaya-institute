# Proyek Akhir: Menyelesaikan Permasalahan Dropout Mahasiswa di Jaya Jaya Institut

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan tinggi yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan dengan reputasi yang baik. Namun, di balik pencapaian tersebut, Jaya Jaya Institut menghadapi masalah serius: tingginya angka mahasiswa yang tidak menyelesaikan pendidikannya alias putus kuliah (*dropout*). Hal ini tentu berdampak buruk pada citra institut dan kesehatan finansial kampus.

### Permasalahan Bisnis
1. Bagaimana cara mengidentifikasi profil dan faktor utama yang menyebabkan mahasiswa mengambil keputusan untuk *dropout*?
2. Bagaimana cara memprediksi secara dini mahasiswa mana saja yang memiliki probabilitas tinggi untuk *dropout* agar institusi dapat melakukan intervensi penyelamatan secepatnya?

### Cakupan Proyek
1. **Eksplorasi Data (EDA) & Data Preparation**: Menganalisis *dataset* profil mahasiswa, melakukan pembersihan data, serta menyederhanakan data kategorik.
2. **Pengembangan Model Machine Learning**: Membangun model prediksi klasifikasi menggunakan **Random Forest** dengan penanganan *imbalance data* (SMOTE) dan optimasi parameter (*GridSearchCV*).
3. **Pembuatan Prototype (Early Warning System)**: Membuat antarmuka *web* interaktif menggunakan Streamlit untuk memprediksi risiko *dropout* baik secara individu maupun massal (*batch*).
4. **Pembuatan Business Dashboard**: Mengembangkan *dashboard* BI (Business Intelligence) untuk memonitor metrik akademik dan finansial mahasiswa.

### Persiapan

Sumber data: [Dataset Student Performance Dicoding](https://github.com/dicodingacademy/dicoding_dataset/raw/refs/heads/main/students_performance/data.csv)

Setup environment:
```bash
# Membuat virtual environment (opsional)
python -m venv env
source env/bin/activate  # Untuk Linux/Mac
env\Scripts\activate     # Untuk Windows

# Instalasi library yang dibutuhkan
pip install -r requirements.txt
```

## Business Dashboard
*Dashboard* bisnis ini dibuat untuk memberikan visibilitas penuh kepada manajemen kampus terkait kondisi demografi, status finansial, dan performa akademik mahasiswa. Fokus utama dari visualisasi ini adalah melihat perbandingan karakteristik antara mahasiswa yang berhasil lulus dan mahasiswa yang mengalami *dropout*.

**Akses Dashboard:**
*   Link Dashboard: [Dashboard Google Data Studio (Looker Studio)](https://datastudio.google.com/reporting/d9bf5973-30b8-405d-a403-37c869c8ff89)

## Menjalankan Sistem Machine Learning
Sistem *Machine Learning* ini dibungkus menggunakan antarmuka **Streamlit**. Aplikasi ini memiliki dua fitur: Pengecekan Satuan (*Quick Check*) menggunakan data akademik inti, dan Pengecekan Massal (*Batch*) menggunakan file CSV.

Aplikasi ini sudah di-*deploy* dan dapat diakses secara langsung melalui tautan berikut:
**Link Prototype:** https://dropout-dicoding.streamlit.app/

**Cara Menjalankan Secara Lokal:**
```bash
# Pastikan berada di direktori proyek submission
cd submission

# Jalankan aplikasi streamlit
streamlit run app.py
```

## Conclusion
Berdasarkan analisis pemodelan *Machine Learning*, dapat ditarik kesimpulan teknis dan bisnis sebagai berikut:
1. **Variabel Penentu Utama (Semester 2 Approved)**: Jumlah mata kuliah yang berhasil diluluskan di semester kedua memiliki bobot tertinggi dalam memicu *dropout*. Kegagalan di tahap ini merupakan prediktor terkuat.
2. **Hambatan Administratif (Tuition Fees Up to Date)**: Status pembayaran biaya kuliah merupakan faktor krusial di luar performa akademik. Kendala finansial yang menunggak sering kali memblokir akses ujian mahasiswa yang pada akhirnya memaksa mereka untuk putus kuliah.
3. **Kualitas Prediksi**: Model *Random Forest* yang dikembangkan mampu memprediksi risiko *dropout* dengan sensitivitas yang sangat baik (Recall 92%).

*Catatan: Model ini sangat sensitif terhadap data performa semester kedua yang baru tersedia di akhir tahun pertama studi. Karenanya, sistem ini difungsikan sebagai instrumen monitoring berkala (Early Warning), bukan prediksi instan saat pendaftaran awal.*

### Rekomendasi Action Items
Untuk menekan angka putus kuliah, Jaya Jaya Institut direkomendasikan mengambil tindakan operasional berikut:
- **Implementasi Digital Early Warning System (EWS)**: Menggunakan aplikasi prediksi (seperti yang dibuat pada *prototype* ini) secara berkala di akhir semester satu. Mahasiswa dengan persentase risiko tinggi dan SKS lulus di bawah 50% harus segera mendapatkan notifikasi wajib bimbingan ke dosen wali dalam kurun waktu 7 hari.
- **Intervensi Akademik Terarah**: Membangun kelas remedial atau tutor sebaya khusus untuk mata kuliah di semester kedua yang secara historis menjadi batu sandungan (*bottleneck*) bagi kelulusan mahasiswa.
- **Restrukturisasi Pembayaran (Finansial)**: Mengintegrasikan EWS dengan biro keuangan. Jika model mendeteksi mahasiswa dengan IPK bagus namun probabilitas risikonya tinggi akibat tunggakan (*Tuition fees not up to date*), kampus harus proaktif menawarkan skema cicilan fleksibel atau dana bantuan darurat.
