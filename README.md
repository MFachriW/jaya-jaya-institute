# Proyek Akhir: Menyelesaikan Permasalahan Dropout Mahasiswa di Jaya Jaya Institut

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan tinggi yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan dengan reputasi yang baik. Namun, di balik pencapaian tersebut, Jaya Jaya Institut menghadapi masalah serius: tingginya angka mahasiswa yang tidak menyelesaikan pendidikannya alias putus kuliah (*dropout*). Hal ini tentu berdampak buruk pada citra institut dan kesehatan finansial kampus.

### Permasalahan Bisnis
1. Bagaimana cara mengidentifikasi profil dan faktor utama yang menyebabkan mahasiswa mengambil keputusan untuk *dropout*?
2. Bagaimana cara memprediksi secara dini mahasiswa mana saja yang memiliki probabilitas tinggi untuk *dropout* agar institusi dapat melakukan intervensi penyelamatan secepatnya?

### Cakupan Proyek
1. **Eksplorasi Data (EDA) & Data Preparation**: Menganalisis *dataset* profil mahasiswa, melakukan pembersihan data, serta menyederhanakan data kategorik.
2. **Pengembangan Model Machine Learning**: Membangun model prediksi klasifikasi menggunakan **Random Forest** dengan penanganan *imbalance data* (SMOTE) dan optimasi parameter (*GridSearchCV*).
3. **Pembuatan Prototype (Early Warning System)**: Membuat antarmuka *web* interaktif menggunakan Streamlit dengan arsitektur *Dual-Model* untuk memprediksi risiko *dropout* baik secara individu maupun massal.
4. **Pembuatan Business Dashboard**: Mengembangkan *dashboard* analitik interaktif untuk memonitor metrik akademik, finansial, dan demografi mahasiswa.

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
*Dashboard* analitik ini dibangun secara interaktif (menggunakan Streamlit & Plotly) untuk memberikan visibilitas penuh kepada manajemen kampus terkait kondisi demografi, status finansial, dan performa akademik mahasiswa. Dilengkapi dengan fitur *Slicer* (Filter Jurusan), manajemen dapat melihat pola spesifik *dropout* di setiap program studi.

**Akses Dashboard:**
* Link Dashboard: [Dashboard Analitik Jaya Jaya Institut](https://do-dashboard.streamlit.app/)

## Menjalankan Sistem Machine Learning (Early Warning System)
Sistem *Machine Learning* ini dibungkus menggunakan antarmuka **Streamlit**. Untuk mengoptimalkan *User Experience* dan akurasi, sistem ini dirancang menggunakan **Dual-Model Architecture**:
1. **Quick Check (Single Inference):** Menggunakan model teringkas (*8 Top Feature Importance*) agar staf dapat melakukan pengecekan risiko secara instan tanpa perlu mengisi puluhan form.
2. **Batch Check (Massal):** Menggunakan model komprehensif (*Full Features*) untuk evaluasi data massal (CSV) yang menghasilkan akurasi maksimal.

**Akses Prototype EWS:**
* Link Aplikasi: [Aplikasi EWS Jaya Jaya Institut](https://dropout-dicoding.streamlit.app/)

**Cara Menjalankan Secara Lokal:**
```bash
# Pastikan berada di direktori proyek submission
cd submission

# Jalankan dashboard analitik
streamlit run dashboard.py

# Jalankan aplikasi ML (EWS)
streamlit run app.py
```

## Conclusion

Berdasarkan hasil analisis data eksploratif (EDA) dan pengembangan model *Machine Learning*, berikut adalah kesimpulan komprehensif yang ditarik untuk Jaya Jaya Institut:

### 1. Karakteristik & Faktor yang Berkaitan dengan Dropout (Berdasarkan EDA)
Melalui analisis mendalam terhadap distribusi dan proporsi data, faktor pendorong *dropout* diklasifikasikan menjadi tiga kelompok utama:

* **Faktor Kritis (Pendorong Utama)**: 
    * **Masalah Finansial**: Mahasiswa yang menunggak biaya kuliah (*Tuition fees not up to date*), berstatus debitur, dan tidak memiliki beasiswa memiliki tingkat *dropout* sangat tinggi (80-90%).
    * **Tingkat Kesulitan Jurusan**: Terdapat pola risiko tinggi pada prodi spesifik seperti *Informatics Engineering* dan *Biofuel Production Technologies*.
    * **Latar Belakang Pendidikan**: Mahasiswa dengan data kualifikasi orang tua yang tidak terdefinisi (*Other/Unknown*) menunjukkan kerentanan lebih tinggi.
* **Faktor Kontekstual & Akademik**:
    * **Performa Awal Semester**: Terdapat perbedaan *mean* yang sangat kontras pada jumlah SKS yang lulus di semester 1 dan 2 antara kelompok Lulus dan *Dropout*.
    * **Faktor Usia**: Distribusi usia mahasiswa *dropout* bersifat *right-skewed* (menjangkau usia 25-60 tahun), menunjukkan bahwa mahasiswa dewasa memiliki risiko keberlanjutan studi yang lebih besar.
* **Faktor Tidak Signifikan**: Ditemukan bahwa nilai ujian masuk (*Admission grade*), nilai kualifikasi sebelumnya, serta indikator ekonomi makro (GDP, Inflasi) tidak memiliki korelasi langsung sebagai pembeda antara mahasiswa yang lulus dan *dropout*.

### 2. Performa Model Prediksi & Feature Importance (Berdasarkan Machine Learning)
Sistem *Early Warning System* (EWS) dikembangkan untuk mengotomatisasi deteksi risiko berdasarkan pola di atas:

* **Performa Model**: Algoritma **Random Forest** dengan optimasi SMOTE dan GridSearchCV berhasil mencapai **Recall sebesar 92%**. Skor ini menunjukkan model sangat handal dalam meminimalisir kesalahan deteksi (*false negative*) pada mahasiswa yang sebenarnya berisiko.
* **Interpretasi Model (Feature Importance)**: Berdasarkan evaluasi model, fitur yang memberikan kontribusi paling signifikan dalam kinerja prediksi adalah **jumlah SKS lulus pada semester 2 dan semester 1** (`Curricular_units_2nd_sem_approved` & `Curricular_units_1st_sem_approved`), serta status pembayaran SPP (`Tuition_fees_up_to_date`). Fitur-fitur akademik dari kedua semester awal ini menjadi informasi utama yang digunakan oleh model untuk membedakan antara mahasiswa yang berisiko *dropout* dan yang berpotensi lulus dengan akurasi tinggi.

### Rekomendasi Action Items
- **Prioritas Intervensi Finansial**: Mengingat faktor finansial adalah pendorong kritis, kampus disarankan membangun sistem otomatisasi bantuan bagi mahasiswa yang memiliki IPK baik namun terdeteksi menunggak SPP.
- **Monitoring Usia & Jurusan**: Memberikan pendampingan konseling khusus bagi mahasiswa kategori dewasa dan mahasiswa di jurusan dengan tingkat kesulitan tinggi sejak awal semester pertama.
- **Optimalisasi EWS**: Menggunakan model ini secara rutin di akhir setiap semester untuk memetakan mahasiswa "merah" yang membutuhkan intervensi akademik segera (remedial atau bimbingan dosen wali).

### Limitasi & Saran Pengembangan Lanjutan
Model saat ini sangat akurat dalam membaca data administratif, namun belum menyentuh aspek psikososial. Pengembangan ke depan disarankan mencakup:
* Integrasi data survei kesehatan mental dan tingkat stres mahasiswa.
* Data keterlibatan organisasi dan kehidupan sosial kampus (Engagement).
* Informasi beban kerja eksternal mahasiswa (*part-time job*).

Penggabungan data administratif dengan data psikososial akan menghasilkan sistem EWS yang jauh lebih komprehensif dan suportif.

### 📂 Sumber Data & Acknowledgements
Dataset yang digunakan dalam proyek ini adalah **"Students' Performance"**, yang berisi data komprehensif dari sebuah institusi pendidikan tinggi (mencakup jalur akademik, demografi, faktor sosial-ekonomi, dan performa akademik mahasiswa di akhir semester 1 dan 2). 

Data ini telah diunduh dan disimpan secara lokal di dalam repositori ini (`Data Mahasiswa Jaya Jaya Institut.csv`) untuk memastikan stabilitas *deployment* aplikasi.

**Sitasi Asli Dataset:**
> Realinho, Valentim, Vieira Martins, Mónica, Machado, Jorge, and Baptista, Luís. (2021). Predict students' dropout and academic success. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89.
