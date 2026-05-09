import streamlit as st
import pandas as pd
import joblib

# Configuration
st.set_page_config(page_title="Jaya Jaya EWS", page_icon="🎓", layout="wide")

# Custom CSS for UI adjustments
st.markdown("""
<style>
    .header-box {
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .header-box h1, .header-box p {
        color: white !important;
        margin: 0;
    }
    .warning-box {
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(255, 75, 75, 0.1);
        border: 1px solid #ff4b4b;
        text-align: center;
    }
    .safe-box {
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(75, 255, 75, 0.1);
        border: 1px solid #4bff4b;
        text-align: center;
    }
    .big-text {
        font-size: 3.5rem !important;
        font-weight: 700;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("""
<div class="header-box">
    <h1>🎓 Jaya Jaya Institut: Early Warning System</h1>
    <p>Sistem pendeteksi dini risiko dropout mahasiswa berbasis Dual-Model Architecture.</p>
</div>
""", unsafe_allow_html=True)

# Load Models (Single & Batch)
@st.cache_resource
def load_models():
    # Load model untuk form UI (8 Fitur)
    model_single = joblib.load('model/model_single.joblib')
    # Load model & struktur kolom untuk file CSV (Full Fitur)
    model_student_dropout_rf = joblib.load('model/model_student_dropout_rf.joblib')
    batch_cols = joblib.load('model/model_columns.joblib')
    return model_single, model_student_dropout_rf, batch_cols

try:
    model_single, model_student_dropout_rf, batch_cols = load_models()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# Daftar 8 fitur untuk Tab 1 (sesuai urutan training)
fitur_single = [
    'Curricular_units_2nd_sem_approved',
    'Curricular_units_1st_sem_approved',
    'Curricular_units_2nd_sem_grade',
    'Curricular_units_1st_sem_grade',
    'Tuition_fees_up_to_date',
    'Curricular_units_2nd_sem_evaluations',
    'Scholarship_holder',
    'Age_at_enrollment'
]

# Main Tabs
tab1, tab2 = st.tabs(["🎯 Single Prediction (Fast Screening)", "📁 Batch Prediction (Deep Analysis)"])

# ------------------------------------------
# TAB 1: SINGLE PREDICTION (Pakai Model Single)
# ------------------------------------------
with tab1:
    st.subheader("Cek Risiko Mahasiswa")
    st.write("Masukkan 8 metrik utama mahasiswa untuk memprediksi probabilitas dropout secara instan.")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Usia saat Mendaftar", min_value=15, max_value=80, value=20)
        sem1_approved = st.number_input("SKS Lulus (Semester 1)", min_value=0, max_value=30, value=5)
        sem1_grade = st.number_input("IPK (Semester 1)", min_value=0.0, max_value=20.0, value=12.0)
        tuition_up_to_date = st.selectbox("Status Pembayaran SPP", options=[1, 0], format_func=lambda x: "Lunas" if x == 1 else "Menunggak")
        
    with col2:
        scholarship = st.selectbox("Penerima Beasiswa", options=[1, 0], format_func=lambda x: "Ya" if x == 1 else "Tidak")
        sem2_evals = st.number_input("Jumlah Evaluasi/Ujian (Semester 2)", min_value=0, max_value=30, value=8)
        sem2_approved = st.number_input("SKS Lulus (Semester 2)", min_value=0, max_value=30, value=5)
        sem2_grade = st.number_input("IPK (Semester 2)", min_value=0.0, max_value=20.0, value=12.0)
        
    if st.button("🔍 Prediksi Instan", use_container_width=True):
        input_data = pd.DataFrame([[
            sem2_approved, sem1_approved, sem2_grade, sem1_grade,
            tuition_up_to_date, sem2_evals, scholarship, age
        ]], columns=fitur_single)
            
        pred_class = model_single.predict(input_data)[0]
        pred_proba = model_single.predict_proba(input_data)[0]
        
        st.markdown("---")
        if pred_class == 1:
            st.markdown(f"""
            <div class="warning-box">
                <h4>Status Mahasiswa</h4>
                <h3 style="color:#ff4b4b;">BERESIKO DROPOUT</h3>
                <div class="big-text" style="color:#ff4b4b;">{pred_proba[1] * 100:.1f}%</div>
                <p>Memerlukan intervensi segera berdasarkan 8 prediktor utama.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="safe-box">
                <h4>Status Mahasiswa</h4>
                <h3 style="color:#4bff4b;">AMAN (POTENSI LULUS)</h3>
                <div class="big-text" style="color:#4bff4b;">{pred_proba[0] * 100:.1f}%</div>
                <p>Berada di jalur akademik yang baik.</p>
            </div>
            """, unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: BATCH PREDICTION (Pakai Model Batch / Full Fitur)
# ------------------------------------------
with tab2:
    st.subheader("Batch Prediction Dashboard")
    st.write("Unggah dataset komprehensif. Sistem akan melakukan analisis mendalam (Deep Analysis) menggunakan seluruh fitur.")
    uploaded_file = st.file_uploader("Upload file CSV (Gunakan format delimiter ';')", type=['csv'])
    
    if uploaded_file is not None:
        try:
            batch_data = pd.read_csv(uploaded_file, delimiter=';')
            
            if st.button("🚀 Proses Batch Data", use_container_width=True):
                with st.spinner("Melakukan prediksi mendalam..."):
                    # Kembalikan fungsi simplifikasi untuk model Batch
                    def simplify_education(code):
                        if pd.isna(code): return 'Unknown'
                        code = int(code)
                        if code in [2, 3, 4, 5, 6, 40, 41, 42, 43, 44]: return 'Higher Education'
                        elif code in [1, 9, 10, 11, 12, 13, 14, 15]: return 'Secondary Education'
                        elif code in [19, 22, 26, 27, 29, 30, 37, 38]: return 'Basic Education'
                        else: return 'Other_Unknown'
                    
                    def simplify_occupation(code):
                        if pd.isna(code): return 'Unknown'
                        code = int(code)
                        if code == 0: return 'Student'
                        elif code in [1, 2, 3]: return 'Prof_Manager'
                        elif code in [4, 5, 6, 7, 8]: return 'Clerk_Service_Sales'
                        elif code in [9, 10]: return 'Labor_Crafts'
                        else: return 'Other'
                    
                    process_data = batch_data.copy()
                    
                    # Terapkan fungsi simplifikasi jika kolomnya ada
                    if 'Previous_qualification' in process_data.columns:
                        process_data['Previous_qualification'] = process_data['Previous_qualification'].apply(simplify_education)
                    if 'Mothers_qualification' in process_data.columns:
                        process_data['Mothers_qualification'] = process_data['Mothers_qualification'].apply(simplify_education)
                    if 'Fathers_qualification' in process_data.columns:
                        process_data['Fathers_qualification'] = process_data['Fathers_qualification'].apply(simplify_education)
                    if 'Mothers_occupation' in process_data.columns:
                        process_data['Mothers_occupation'] = process_data['Mothers_occupation'].apply(simplify_occupation)
                    if 'Fathers_occupation' in process_data.columns:
                        process_data['Fathers_occupation'] = process_data['Fathers_occupation'].apply(simplify_occupation)
                    
                    cat_cols = ['Marital_status', 'Application_mode', 'Application_order', 'Course',
                                'Previous_qualification', 'Nacionality', 'Mothers_qualification',
                                'Fathers_qualification', 'Mothers_occupation', 'Fathers_occupation']
                    
                    # One-Hot Encoding
                    process_data = pd.get_dummies(process_data, columns=[c for c in cat_cols if c in process_data.columns], drop_first=True)
                    
                    # Sinkronisasi kolom (Align) dengan kolom saat model batch di-training
                    process_data = process_data.reindex(columns=batch_cols, fill_value=0)
                    
                    # Inference pakai MODEL BATCH
                    predictions = model_student_dropout_rf.predict(process_data)
                    probabilities = model_student_dropout_rf.predict_proba(process_data)[:, 1]
                    
                    # Merge results
                    batch_data['Status_Prediksi'] = ["Dropout" if p == 1 else "Aman" for p in predictions]
                    batch_data['Risk_Probability (%)'] = probabilities * 100
                    
                    # Dashboard Metrics
                    total_students = len(batch_data)
                    dropout_count = len(batch_data[batch_data['Status_Prediksi'] == 'Dropout'])
                    graduate_count = total_students - dropout_count
                    
                    dropout_pct = (dropout_count / total_students) * 100
                    graduate_pct = (graduate_count / total_students) * 100
                    
                    st.markdown("---")
                    st.markdown("### Ringkasan Eksekutif (Full Model)")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total Data", f"{total_students} Mahasiswa")
                    m2.metric("Potensi Lulus (Aman)", f"{graduate_count}", f"{graduate_pct:.1f}%", delta_color="normal")
                    m3.metric("Beresiko Dropout", f"{dropout_count}", f"{dropout_pct:.1f}%", delta_color="inverse")
                    
                    st.markdown("### Detail Prediksi")
                    display_cols = ['Status_Prediksi', 'Risk_Probability (%)'] + [c for c in batch_data.columns if c not in ['Status_Prediksi', 'Risk_Probability (%)']]
                    st.dataframe(batch_data[display_cols], use_container_width=True)
                    
                    csv_export = batch_data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Unduh Data Prediksi",
                        data=csv_export,
                        file_name="batch_predictions_full_model.csv",
                        mime="text/csv",
                    )
        except Exception as e:
            st.error(f"Error processing file: {e}")
