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
Berdasarkan analisis pemodelan *Machine Learning*, dapat ditarik kesimpulan teknis dan bisnis sebagai berikut:
1. **Variabel Penentu Utama (Semester 2 Approved)**: Jumlah mata kuliah yang berhasil diluluskan di semester kedua memiliki bobot tertinggi dalam memicu *dropout*. Kegagalan di tahap ini merupakan prediktor terkuat.
2. **Hambatan Administratif (Tuition Fees Up to Date)**: Status pembayaran biaya kuliah merupakan faktor krusial di luar performa akademik. Kendala finansial yang menunggak sering kali memblokir akses ujian mahasiswa yang pada akhirnya memaksa mereka untuk putus kuliah.
3. **Kualitas Prediksi**: Model *Random Forest* yang dikembangkan mampu memprediksi risiko *dropout* dengan performa klasifikasi yang sangat baik dan stabil (Recall > 90% pada evaluasi).

*Catatan: Model ini sangat sensitif terhadap data performa semester kedua. Karenanya, sistem ini difungsikan sebagai instrumen monitoring berkala (Early Warning), bukan prediksi instan saat pendaftaran awal.*

### Rekomendasi Action Items
Untuk menekan angka putus kuliah, Jaya Jaya Institut direkomendasikan mengambil tindakan operasional berikut:
- **Implementasi Digital Early Warning System (EWS)**: Menggunakan aplikasi prediksi ini secara berkala di pertengahan dan akhir tahun studi. Mahasiswa dengan persentase risiko tinggi (>70%) dan SKS lulus di bawah standar harus segera mendapatkan notifikasi bimbingan wajib dengan dosen wali.
- **Intervensi Akademik Terarah**: Membangun kelas remedial atau tutor sebaya khusus untuk mata kuliah di semester pertama dan kedua yang secara historis menjadi batu sandungan (*bottleneck*) bagi kelulusan.
- **Restrukturisasi Pembayaran (Finansial)**: Mengintegrasikan EWS dengan biro keuangan. Jika model mendeteksi mahasiswa dengan IPK baik namun berisiko tinggi akibat tunggakan SPP, kampus harus proaktif menawarkan skema cicilan fleksibel, penundaan pembayaran, atau dana bantuan darurat.

### Limitasi & Saran Pengembangan Lanjutan
Meskipun model ini memiliki akurasi yang tinggi, data yang digunakan saat ini murni berbasis data **administratif dan akademik**. Padahal di dunia nyata, *dropout* sering dipicu oleh faktor di luar kampus. Untuk pengembangan selanjutnya, disarankan agar Jaya Jaya Institut mulai mendata variabel psikososial seperti:
* Tingkat stres dan kesehatan mental mahasiswa (via survei berkala).
* Keterlibatan mahasiswa dalam organisasi/sosial kampus.
* Beban jam kerja eksternal (*part-time job*) mahasiswa.

Penggabungan data administratif dengan data psikososial akan menghasilkan sistem EWS yang jauh lebih komprehensif dan suportif.

### 📂 Sumber Data & Acknowledgements
Dataset yang digunakan dalam proyek ini adalah **"Students' Performance"**, yang berisi data komprehensif dari sebuah institusi pendidikan tinggi (mencakup jalur akademik, demografi, faktor sosial-ekonomi, dan performa akademik mahasiswa di akhir semester 1 dan 2). 

Data ini telah diunduh dan disimpan secara lokal di dalam repositori ini (`Data Mahasiswa Jaya Jaya Institut.csv`) untuk memastikan stabilitas *deployment* aplikasi.

**Sitasi Asli Dataset:**
> Realinho, Valentim, Vieira Martins, Mónica, Machado, Jorge, and Baptista, Luís. (2021). Predict students' dropout and academic success. UCI Machine Learning Repository. https://doi.org/10.24432/C5MC89.
