import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Layout Wide
st.set_page_config(page_title="Jaya Jaya Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #000428 0%, #004e92 100%); padding: 1.5rem; border-radius: 10px; text-align: center; margin-bottom: 1.5rem; color: white;">
    <h1 style="color: white; margin: 0; font-size: 2rem;">📊 Jaya Jaya Institut: Data Center</h1>
    <p style="color: white; margin: 0;">Dashboard Analisis Historis Faktor Dropout Mahasiswa</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('Data Mahasiswa Jaya Jaya Institut.csv', delimiter=';')
    
    # Membuang 'Enrolled' karena nasib akhirnya belum diketahui
    df = df[df['Status'] != 'Enrolled'].copy()
    
    df['Target_Label'] = df['Status']
    dict_yes_no = {1: 'Ya', 0: 'Tidak', 1.0: 'Ya', 0.0: 'Tidak'}
    df['Debtor'] = df['Debtor'].replace(dict_yes_no)
    df['Scholarship_holder'] = df['Scholarship_holder'].replace(dict_yes_no)
    df['Tuition_fees_up_to_date'] = df['Tuition_fees_up_to_date'].replace({1: 'Lunas', 0: 'Menunggak'})
    df['Gender'] = df['Gender'].replace({1: 'Pria', 0: 'Wanita', 1.0: 'Pria', 0.0: 'Wanita'})
    df['Marital_status'] = df['Marital_status'].replace({1: 'Single', 2: 'Menikah', 3: 'Duda/Janda', 4: 'Cerai', 5: 'Facto Union', 6: 'Pisah Hukum'})
    
    # Tambahan: Tipe Kelas
    df['Daytime_evening_attendance'] = df['Daytime_evening_attendance'].replace({1: 'Pagi/Siang', 0: 'Malam', 1.0: 'Pagi/Siang', 0.0: 'Malam'})
    
    # Nama Jurusan Lengkap
    df['Course'] = df['Course'].replace({
        33: 'Biofuel Production Technologies', 171: 'Animation and Multimedia Design', 
        8014: 'Social Service (Evening)', 9003: 'Agronomy', 
        9070: 'Communication Design', 9085: 'Veterinary Nursing',
        9119: 'Informatics Engineering', 9130: 'Equinculture', 
        9147: 'Management', 9238: 'Social Service', 
        9254: 'Tourism', 9500: 'Nursing',
        9556: 'Oral Hygiene', 9670: 'Advertising and Marketing Mgmt', 
        9773: 'Journalism and Communication', 9853: 'Basic Education', 
        9991: 'Management (Evening)'
    })
    
    return df

try:
    df_dash = load_data()
    color_map = {'Graduate': '#2ecc71', 'Dropout': '#e74c3c'}
    
    def compact_layout(fig):
        fig.update_traces(cliponaxis=False)
        fig.update_layout(
            margin=dict(l=10, r=10, t=60, b=90),
            height=360, 
            legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5, title=None)
        )
        return fig

    # ==========================================
    # FILTER JURUSAN
    # ==========================================
    st.markdown("### 🔍 Filter Data")
    daftar_jurusan = ["Semua Jurusan"] + sorted(df_dash['Course'].unique().tolist())
    pilihan_jurusan = st.selectbox("Pilih Jurusan untuk dianalisis:", daftar_jurusan)
    
    if pilihan_jurusan != "Semua Jurusan":
        df_filtered = df_dash[df_dash['Course'] == pilihan_jurusan].copy()
    else:
        df_filtered = df_dash.copy()

    st.markdown("---")

    if len(df_filtered) == 0:
        st.warning("Tidak ada data untuk filter yang dipilih.")
    else:
        # ==========================================
        # ZONA 1: SCORECARDS (Label diperjelas agar tidak misleading)
        # ==========================================
        total_students = len(df_filtered)
        total_grad = len(df_filtered[df_filtered['Target_Label'] == 'Graduate'])
        total_drop = len(df_filtered[df_filtered['Target_Label'] == 'Dropout'])
        
        c1, c2, c3 = st.columns(3)
        c1.metric(f"Total Data (Selesai Studi | {pilihan_jurusan if pilihan_jurusan != 'Semua Jurusan' else 'Seluruh Prodi'})", f"{total_students}")
        c2.metric("Total Lulus", f"{total_grad}", f"{(total_grad/total_students)*100:.1f}%" if total_students > 0 else "0%", delta_color="normal")
        c3.metric("Total Dropout", f"{total_drop}", f"{(total_drop/total_students)*100:.1f}%" if total_students > 0 else "0%", delta_color="inverse")
        st.caption("*Catatan: Data mahasiswa berstatus 'Enrolled' (masih aktif) tidak diikutsertakan dalam kalkulasi dashboard ini agar rasio Dropout historis akurat.")
        
        st.markdown("---")
        
        # ==========================================
        # ZONA 2: FAKTOR UTAMA (Top 6 Predictors)
        # ==========================================
        st.markdown("### 📚 6 Faktor Utama Penentu Dropout (Top Predictors)")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            df_sks = df_filtered.groupby('Target_Label')[['Curricular_units_1st_sem_approved', 'Curricular_units_2nd_sem_approved']].mean().reset_index()
            df_sks_melt = df_sks.melt(id_vars='Target_Label', var_name='Semester', value_name='Avg_SKS')
            df_sks_melt['Semester'] = df_sks_melt['Semester'].replace({'Curricular_units_1st_sem_approved': 'Sem 1', 'Curricular_units_2nd_sem_approved': 'Sem 2'})
            fig_sks = px.bar(df_sks_melt, x='Semester', y='Avg_SKS', color='Target_Label', barmode='group', color_discrete_map=color_map, title="SKS Lulus (Top 1 & 2)", text_auto='.1f')
            fig_sks.update_xaxes(title=None); fig_sks.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_sks), use_container_width=True)

        with col2:
            df_ipk = df_filtered.groupby('Target_Label')[['Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_grade']].mean().reset_index()
            df_ipk_melt = df_ipk.melt(id_vars='Target_Label', var_name='Semester', value_name='Avg_IPK')
            df_ipk_melt['Semester'] = df_ipk_melt['Semester'].replace({'Curricular_units_1st_sem_grade': 'Sem 1', 'Curricular_units_2nd_sem_grade': 'Sem 2'})
            fig_ipk = px.bar(df_ipk_melt, x='Semester', y='Avg_IPK', color='Target_Label', barmode='group', color_discrete_map=color_map, title="Nilai/IPK (Top 3 & 4)", text_auto='.1f')
            fig_ipk.update_xaxes(title=None); fig_ipk.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_ipk), use_container_width=True)
            
        with col3:
            fig_spp = px.histogram(df_filtered, x='Tuition_fees_up_to_date', color='Target_Label', barnorm='percent', text_auto='.1f', color_discrete_map=color_map, title="Status SPP (Top 5)")
            fig_spp.update_xaxes(title=None); fig_spp.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_spp), use_container_width=True)

        with col4:
            df_eval = df_filtered.groupby('Target_Label')[['Curricular_units_1st_sem_evaluations', 'Curricular_units_2nd_sem_evaluations']].mean().reset_index()
            df_eval_melt = df_eval.melt(id_vars='Target_Label', var_name='Semester', value_name='Avg_Eval')
            df_eval_melt['Semester'] = df_eval_melt['Semester'].replace({'Curricular_units_1st_sem_evaluations': 'Sem 1', 'Curricular_units_2nd_sem_evaluations': 'Sem 2'})
            fig_eval = px.bar(df_eval_melt, x='Semester', y='Avg_Eval', color='Target_Label', barmode='group', color_discrete_map=color_map, title="Jml Evaluasi (Top 6)", text_auto='.1f')
            fig_eval.update_xaxes(title=None); fig_eval.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_eval), use_container_width=True)

        st.markdown("---")

        # ==========================================
        # ZONA 3: PROFIL DEMOGRAFI (Format 3x2 agar lebih lega)
        # ==========================================
        st.markdown("### 👥 Analisis Demografi & Latar Belakang Mahasiswa")
        
        # Baris 1 Demografi
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            fig_schol = px.histogram(df_filtered, x='Scholarship_holder', color='Target_Label', barnorm='percent', text_auto='.1f', color_discrete_map=color_map, title="Penerima Beasiswa")
            fig_schol.update_xaxes(title=None); fig_schol.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_schol), use_container_width=True)

        with col_b:
            fig_debt = px.histogram(df_filtered, x='Debtor', color='Target_Label', barnorm='percent', text_auto='.1f', color_discrete_map=color_map, title="Status Hutang")
            fig_debt.update_xaxes(title=None); fig_debt.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_debt), use_container_width=True)

        with col_c:
            fig_gender = px.histogram(df_filtered, x='Gender', color='Target_Label', barnorm='percent', text_auto='.1f', color_discrete_map=color_map, title="Jenis Kelamin")
            fig_gender.update_xaxes(title=None); fig_gender.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_gender), use_container_width=True)
            
        # Baris 2 Demografi
        col_d, col_e, col_f = st.columns(3)
        with col_d:
            fig_marital = px.histogram(df_filtered, x='Marital_status', color='Target_Label', barnorm='percent', text_auto='.1f', color_discrete_map=color_map, title="Status Pernikahan")
            fig_marital.update_xaxes(title=None, tickangle=35); fig_marital.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_marital), use_container_width=True)
            
        with col_e:
            fig_att = px.histogram(df_filtered, x='Daytime_evening_attendance', color='Target_Label', barnorm='percent', text_auto='.1f', color_discrete_map=color_map, title="Tipe Kelas")
            fig_att.update_xaxes(title=None); fig_att.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_att), use_container_width=True)
            
        with col_f:
            df_age = df_filtered.groupby('Target_Label')['Age_at_enrollment'].mean().reset_index()
            fig_age = px.bar(df_age, x='Target_Label', y='Age_at_enrollment', color='Target_Label', text_auto='.1f', color_discrete_map=color_map, title="Rata-rata Usia Mendaftar")
            fig_age.update_xaxes(title=None); fig_age.update_yaxes(title=None)
            st.plotly_chart(compact_layout(fig_age), use_container_width=True)
            
except Exception as e:
    st.error(f"Error loading dashboard: {e}")