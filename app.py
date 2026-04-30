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
    <p>Sistem pendeteksi dini risiko dropout mahasiswa berbasis Machine Learning.</p>
</div>
""", unsafe_allow_html=True)

# Load model and feature columns
@st.cache_resource
def load_model():
    model = joblib.load('model/model_student_dropout_rf.joblib')
    cols = joblib.load('model/model_columns.joblib')
    return model, cols

try:
    model, model_columns = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Main Tabs
tab1, tab2 = st.tabs(["🎯 Single Prediction", "📁 Batch Prediction Dashboard"])

# ------------------------------------------
# TAB 1: SINGLE PREDICTION
# ------------------------------------------
with tab1:
    st.subheader("Cek Risiko Mahasiswa")
    
    col1, col2 = st.columns(2)
    with col1:
        sem1_approved = st.number_input("SKS Lulus (Semester 1)", min_value=0, max_value=30, value=5)
        sem1_grade = st.number_input("IPK (Semester 1)", min_value=0.0, max_value=20.0, value=12.0)
        tuition_up_to_date = st.selectbox("Status SPP", options=[1, 0], format_func=lambda x: "Lunas" if x == 1 else "Menunggak")
        
    with col2:
        sem2_approved = st.number_input("SKS Lulus (Semester 2)", min_value=0, max_value=30, value=5)
        sem2_grade = st.number_input("IPK (Semester 2)", min_value=0.0, max_value=20.0, value=12.0)
        scholarship = st.selectbox("Penerima Beasiswa", options=[1, 0], format_func=lambda x: "Ya" if x == 1 else "Tidak")
    
    if st.button("🔍 Prediksi", use_container_width=True):
        # Create base dataframe with zeros
        input_data = pd.DataFrame(0, index=[0], columns=model_columns)
        
        # Inject median values to stabilize prediction for hidden features
        baseline_numerics = {
            'Previous_qualification_grade': 133.1,
            'Admission_grade': 126.1,
            'Age_at_enrollment': 20,
            'Curricular_units_1st_sem_credited': 0,
            'Curricular_units_1st_sem_enrolled': 6,
            'Curricular_units_1st_sem_evaluations': 8,
            'Curricular_units_1st_sem_without_evaluations': 0,
            'Curricular_units_2nd_sem_credited': 0,
            'Curricular_units_2nd_sem_enrolled': 6,
            'Curricular_units_2nd_sem_evaluations': 8,
            'Curricular_units_2nd_sem_without_evaluations': 0,
            'Unemployment_rate': 11.1,
            'Inflation_rate': 1.4,
            'GDP': 0.32
        }
        
        for col, val in baseline_numerics.items():
            if col in input_data.columns:
                input_data[col] = val
        
        # Update with user inputs
        if 'Curricular_units_1st_sem_approved' in input_data.columns:
            input_data['Curricular_units_1st_sem_approved'] = sem1_approved
        if 'Curricular_units_1st_sem_grade' in input_data.columns:
            input_data['Curricular_units_1st_sem_grade'] = sem1_grade
        if 'Curricular_units_2nd_sem_approved' in input_data.columns:
            input_data['Curricular_units_2nd_sem_approved'] = sem2_approved
        if 'Curricular_units_2nd_sem_grade' in input_data.columns:
            input_data['Curricular_units_2nd_sem_grade'] = sem2_grade
        if 'Tuition_fees_up_to_date' in input_data.columns:
            input_data['Tuition_fees_up_to_date'] = tuition_up_to_date
        if 'Scholarship_holder' in input_data.columns:
            input_data['Scholarship_holder'] = scholarship
            
        # Inference
        pred_class = model.predict(input_data)[0]
        pred_proba = model.predict_proba(input_data)[0]
        
        st.markdown("---")
        if pred_class == 1:
            st.markdown(f"""
            <div class="warning-box">
                <h4>Status Mahasiswa</h4>
                <h3 style="color:#ff4b4b;">BERESIKO DROPOUT</h3>
                <div class="big-text" style="color:#ff4b4b;">{pred_proba[1] * 100:.1f}%</div>
                <p>Memerlukan intervensi pendampingan akademik atau finansial segera.</p>
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
# TAB 2: BATCH PREDICTION DASHBOARD
# ------------------------------------------
with tab2:
    st.subheader("Batch Prediction Dashboard")
    uploaded_file = st.file_uploader("Upload file CSV (Gunakan format delimiter ';')", type=['csv'])
    
    if uploaded_file is not None:
        try:
            batch_data = pd.read_csv(uploaded_file, delimiter=';')
            
            if st.button("🚀 Proses Batch Data", use_container_width=True):
                with st.spinner("Melakukan prediksi..."):
                    # Apply data simplifications matching the training phase
                    def simplify_education(code):
                        if pd.isna(code): return 'Unknown'
                        code = int(code)
                        if code in [2, 3, 4, 5, 6, 40, 41, 42, 43, 44]: return 'Higher Education'
                        elif code in [1, 9, 10, 11, 12, 13, 14, 15]: return 'Secondary Education'
                        elif code in [19, 22, 26, 27, 29, 30, 37, 38]: return 'Basic Education'
                        else: return 'Other/Unknown'
                    
                    def simplify_occupation(code):
                        if pd.isna(code): return 'Unknown'
                        code = int(code)
                        if code == 0: return 'Student'
                        elif code in [1, 2, 3]: return 'Prof/Manager'
                        elif code in [4, 5, 6, 7, 8]: return 'Clerk/Service/Sales'
                        elif code in [9, 10]: return 'Labor/Crafts'
                        else: return 'Other'
                    
                    process_data = batch_data.copy()
                    cat_cols = ['Marital_status', 'Application_mode', 'Application_order', 'Course',
                                'Previous_qualification', 'Nacionality', 'Mothers_qualification',
                                'Fathers_qualification', 'Mothers_occupation', 'Fathers_occupation']
                    
                    # Ensure columns exist before encoding
                    process_data = pd.get_dummies(process_data, columns=[c for c in cat_cols if c in process_data.columns])
                    process_data = process_data.reindex(columns=model_columns, fill_value=0)
                    
                    # Inference
                    predictions = model.predict(process_data)
                    probabilities = model.predict_proba(process_data)[:, 1]
                    
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
                    st.markdown("### Ringkasan Eksekutif")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total Data", f"{total_students} Mahasiswa")
                    m2.metric("Potensi Lulus (Aman)", f"{graduate_count}", f"{graduate_pct:.1f}%")
                    m3.metric("Beresiko Dropout", f"{dropout_count}", f"-{dropout_pct:.1f}%", delta_color="inverse")
                    
                    st.markdown("### Detail Prediksi")
                    # Reorder columns to show prediction first
                    display_cols = ['Status_Prediksi', 'Risk_Probability (%)'] + [c for c in batch_data.columns if c not in ['Status_Prediksi', 'Risk_Probability (%)']]
                    st.dataframe(batch_data[display_cols], use_container_width=True)
                    
                    csv_export = batch_data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="⬇️ Unduh Data Prediksi",
                        data=csv_export,
                        file_name="batch_predictions.csv",
                        mime="text/csv",
                    )
        except Exception as e:
            st.error(f"Error processing file: {e}")