import streamlit as st
import numpy as np
import pandas as pd

# ==============================
# KONFIGURASI HALAMAN (Wajib Paling Atas)
# ==============================
st.set_page_config(page_title="SPK Rekomendasi Makanan", page_icon="🍽️")

# ==============================
# DATA DASAR
# ==============================
criteria = ["HP","P","KP","HO","KR","KM","KK"]

criteria_full = {
    "HP": "Harga Produk",
    "HO": "Harga Ongkir",
    "P":  "Promo",
    "KP": "Kecepatan Pengantaran",
    "KR": "Kelengkapan Restoran dan Menu",
    "KM": "Keadaan Makanan",
    "KK": "Keramahan Kurir"
}

questions = [
    ("HP","P"), ("HP","KP"), ("HP","HO"), ("HP","KR"), ("HP","KM"), ("HP","KK"),
    ("KP","P"), ("KP","HO"), ("KP","KR"), ("KP","KM"), ("KP","KK"),
    ("P","HO"), ("P","KR"), ("P","KM"), ("P","KK"),
    ("HO","KR"), ("HO","KM"), ("HO","KK"),
    ("KR","KM"), ("KR","KK"),
    ("KM","KK")
]

app_name = {
    "GO": "GoFood (Gojek)",
    "GR": "GrabFood (Grab)",
    "SF": "ShopeeFood (Shopee)"
}

# ==============================
# 1. FUNGSI AHP (Menghitung Bobot)
# ==============================
def run_ahp(user_input):
    n = len(criteria)
    ahp = pd.DataFrame(np.ones((n,n)), index=criteria, columns=criteria)

    for (A,B), val in user_input.items():
        ahp.loc[A,B] = val
        ahp.loc[B,A] = 1/val

    # Normalisasi & Hitung Bobot Prioritas
    norm = ahp / ahp.sum()
    weights = norm.mean(axis=1)

    return weights.to_dict()

# ==============================
# 2. FUNGSI FUZZY TOPSIS (Perangkingan)
# ==============================
def run_fuzzy_topsis(weights):
    alternatives = ["GO","GR","SF"]

    # --- PERBAIKAN DI SINI: Data Fuzzy yang Bersih ---
    # Data ini adalah skala TFN (Triangular Fuzzy Number)
    fuzzy_data = {
    "HP": [(0.544414,0.765,0.8812), (0.53831,0.76335,0.89047), (0.54761,0.7683,0.87581)],
    "P":  [(0.55789,0.77971,0.88227), (0.54298,0.76459,0.87977), (0.55344,0.78012,0.894)],
    "KP": [(0.49492,0.712,0.8528), (0.49237,0.71289,0.86127), (0.50876,0.73038,0.86712)],
    "HO": [(0.55334,0.77443,0.88013), (0.52525,0.74663,0.87220), (0.53063,0.75545,0.88478)],
    "KR": [(0.56464,0.79017,0.89541), (0.52824,0.7521,0.88549), (0.52284,0.74196,0.86457)],
    "KM": [(0.57075,0.79256,0.88192), (0.56015,0.78093,0.87761), (0.56296,0.78897,0.89365)],
    "KK": [(0.50063,0.72037,0.86675), (0.47474,0.69039,0.84050), (0.48461,0.70308,0.85206)]
    }

    df = pd.DataFrame(fuzzy_data, index=alternatives)

    # Matriks Ternormalisasi Terbobot Fuzzy
    weighted = {}
    for c in df.columns:
        w = weights[c]
        weighted[c] = [(l*w, m*w, u*w) for l,m,u in df[c]]

    wdf = pd.DataFrame(weighted, index=alternatives)
    
    # Defuzzifikasi (Mengubah Fuzzy ke Angka Tegas)
    crisp = wdf.applymap(lambda x: (x[0] + 4*x[1] + x[2]) / 6)

    # Menentukan FPIS (Solusi Ideal Positif) & FNIS (Negatif)
    cost = ["HP","HO"] # Kriteria Biaya (makin rendah makin bagus)
    benefit = ["P","KP","KR","KM","KK"] # Kriteria Keuntungan

    FPIS, FNIS = {},{}
    for c in crisp.columns:
        if c in benefit:
            FPIS[c] = crisp[c].max()
            FNIS[c] = crisp[c].min()
        else: # Cost
            FPIS[c] = crisp[c].min()
            FNIS[c] = crisp[c].max()

    # Menghitung Jarak ke Solusi Ideal
    Dp, Dn = {}, {}
    for a in alternatives:
        Dp[a] = np.sqrt(((crisp.loc[a] - pd.Series(FPIS))**2).sum())
        Dn[a] = np.sqrt(((crisp.loc[a] - pd.Series(FNIS))**2).sum())

    # Menghitung Skor Akhir (Closeness Coefficient)
    CC = {a: Dn[a] / (Dp[a] + Dn[a]) for a in alternatives}
    
    # Mengurutkan dari skor tertinggi ke terendah
    # Hasil berupa list: [('GO', 0.85), ('SF', 0.72), ('GR', 0.65)]
    sorted_ranking = sorted(CC.items(), key=lambda item: item[1], reverse=True)

    return sorted_ranking, crisp

# ==============================
# STREAMLIT UI (Tampilan)
# ==============================
st.title("🍽️ Sistem Rekomendasi Aplikasi Makanan")
st.info("Aplikasi ini menggunakan metode Hybrid AHP (untuk bobot preferensi) dan Fuzzy TOPSIS (untuk perankingan).")

st.write("### Tentukan Preferensi Anda:")

user_input = {}

# Menggunakan Form agar halaman tidak reload setiap kali klik
with st.form("ahp_form"):
    for i, (A, B) in enumerate(questions, start=1):
        st.write(f"**{i}. {criteria_full[A]}** vs **{criteria_full[B]}**")
        
        # Opsi jawaban yang lebih mudah dipahami
        options = [
            f"Sama penting",
            f"{criteria_full[A]} sedikit lebih penting",
            f"{criteria_full[A]} lebih penting",
            f"{criteria_full[A]} mutlak lebih penting",
            f"{criteria_full[B]} sedikit lebih penting",
            f"{criteria_full[B]} lebih penting",
            f"{criteria_full[B]} mutlak lebih penting"
        ]
        
        choice = st.selectbox(f"Pilih perbandingan {i}", options, key=f"q_{i}", label_visibility="collapsed")
        
        # Logika konversi jawaban ke angka (Skala Saaty)
        val = 1
        if choice == options[1]: val = 3
        elif choice == options[2]: val = 5
        elif choice == options[3]: val = 9
        elif choice == options[4]: val = 1/3
        elif choice == options[5]: val = 1/5
        elif choice == options[6]: val = 1/9
        
        user_input[(A, B)] = val
        st.divider()

    submitted = st.form_submit_button("🔍 Hitung Rekomendasi")

if submitted:
    # 1. Jalankan Perhitungan
    weights = run_ahp(user_input)
    sorted_ranking, crisp = run_fuzzy_topsis(weights)

    # 2. Ambil Data Juara 1, 2, dan 3
    # sorted_ranking bentuknya: [('Kode', Skor), ('Kode', Skor), ...]
    rank1_code, rank1_score = sorted_ranking[0]
    rank2_code, rank2_score = sorted_ranking[1]
    rank3_code, rank3_score = sorted_ranking[2]

    # Hitung kontribusi kriteria untuk Juara 1 (sebagai alasan)
    raw_scores = crisp.loc[rank1_code]
    top_criteria = (raw_scores / raw_scores.sum()).sort_values(ascending=False).head(3)

    # ==============================
    # TAMPILAN HASIL
    # ==============================
    st.markdown("## 🏆 Hasil Perankingan")
    
    # --- JUARA 1 ---
    st.success(f"### 🥇 {app_name[rank1_code]}")
    st.markdown(f"**Skor Preferensi Tertinggi: `{rank1_score:.4f}`**")
    
    st.write("**Kenapa ini direkomendasikan?**")
    st.caption("Berdasarkan bobot preferensi Anda, aplikasi ini unggul di faktor:")
    col_alasan = st.columns(3)
    for idx, (crit, val) in enumerate(top_criteria.items()):
        col_alasan[idx].metric(label=criteria_full[crit], value=f"{val*100:.1f}%")
    
    st.markdown("---")

    # --- JUARA 2 & 3 ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"🥈 **Peringkat 2**")
        st.markdown(f"#### {app_name[rank2_code]}")
        st.write(f"Skor: `{rank2_score:.4f}`")

    with col2:
        st.warning(f"🥉 **Peringkat 3**")
        st.markdown(f"#### {app_name[rank3_code]}")
        st.write(f"Skor: `{rank3_score:.4f}`")

    st.markdown("---")
    with st.expander("Lihat Detail Bobot Kriteria Anda"):
        st.write(pd.Series(weights).rename(index=criteria_full).sort_values(ascending=False))
