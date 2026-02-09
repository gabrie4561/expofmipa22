import streamlit as st
import numpy as np
import pandas as pd

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

scale_map = {
    "Sama penting": 1,
    "Sedikit lebih penting": 3,
    "Lebih penting": 5,
    "Jauh lebih penting": 7,
    "Sangat jauh lebih penting": 9
}

# ==============================
# AHP FUNCTION
# ==============================
def run_ahp(user_input):
    n = len(criteria)
    ahp = pd.DataFrame(np.ones((n,n)), index=criteria, columns=criteria)

    for (A,B), val in user_input.items():
        ahp.loc[A,B] = val
        ahp.loc[B,A] = 1/val

    norm = ahp / ahp.sum()
    weights = norm.mean(axis=1)

    

    return weights.to_dict()

# ==============================
# FUZZY TOPSIS FUNCTION
# ==============================
def run_fuzzy_topsis(weights):
    alternatives = ["GO","GR","SF"]

    fuzzy_data = {
import numpy as np
import pandas as pd

print("🔷 CELL 4 — FUZZY TOPSIS (TANPA NORMALISASI)")
print("="*70)

# =================================================
# 1️⃣ ALTERNATIF
# =================================================
alternatives = ["GO", "GR", "SF"]

# =================================================
# 2️⃣ MATRIKS KEPUTUSAN FUZZY (AWAL)
#    C1=HP, C2=P, C3=KP, C4=HO, C5=KR, C6=KM, C7=KK
# =================================================
fuzzy_data = {
    "HP": [(0.544414,0.765,0.8812), (0.53831,0.76335,0.89047), (0.54761,0.7683,0.87581)],
    "P":  [(0.55789,0.77971,0.88227), (0.54298,0.76459,0.87977), (0.55344,0.78012,0.894)],
    "KP": [(0.49492,0.712,0.8528), (0.49237,0.71289,0.86127), (0.50876,0.73038,0.86712)],
    "HO": [(0.55334,0.77443,0.88013), (0.52525,0.74663,0.87220), (0.53063,0.75545,0.88478)],
    "KR": [(0.56464,0.79017,0.89541), (0.52824,0.7521,0.88549), (0.52284,0.74196,0.86457)],
    "KM": [(0.57075,0.79256,0.88192), (0.56015,0.78093,0.87761), (0.56296,0.78897,0.89365)],
    "KK": [(0.50063,0.72037,0.86675), (0.47474,0.69039,0.84050), (0.48461,0.70308,0.85206)]
}

fuzzy_df = pd.DataFrame(fuzzy_data, index=alternatives)
print("\n1️⃣ Matriks Keputusan Fuzzy")
display(fuzzy_df)

# =================================================
# 3️⃣ MATRIKS KEPUTUSAN FUZZY TERBOBOT (AHP USER)
# =================================================
weighted_fuzzy = {}

for c in fuzzy_df.columns:
    w = user_weights[c]
    weighted_fuzzy[c] = [(l*w, m*w, u*w) for l,m,u in fuzzy_df[c]]

weighted_df = pd.DataFrame(weighted_fuzzy, index=alternatives)
print("\n2️⃣ Matriks Keputusan Fuzzy Terbobot")
display(weighted_df)

# =================================================
# 4️⃣ DEFUZZIFIKASI (CENTROID / GMI)
#    M = (l + 4m + u) / 6
# =================================================
def defuzzify(tfn):
    l, m, u = tfn
    return (l + 4*m + u) / 6

crisp_df = weighted_df.applymap(defuzzify)
print("\n3️⃣ Matriks Defuzzifikasi (Crisp)")
display(crisp_df)

# =================================================
# 5️⃣ FPIS & FNIS (PERHATIKAN COST & BENEFIT)
# =================================================
cost_criteria = ["HP", "HO"]
benefit_criteria = ["P", "KP", "KR", "KM", "KK"]

FPIS = {}
FNIS = {}

for c in crisp_df.columns:
    if c in benefit_criteria:
        FPIS[c] = crisp_df[c].max()
        FNIS[c] = crisp_df[c].min()
    else:  # cost
        FPIS[c] = crisp_df[c].min()
        FNIS[c] = crisp_df[c].max()

print("\n4️⃣ FPIS")
display(pd.Series(FPIS))

print("\n5️⃣ FNIS")
display(pd.Series(FNIS))

# =================================================
# 6️⃣ JARAK D+ & D-
# =================================================
D_pos = {}
D_neg = {}

for alt in alternatives:
    D_pos[alt] = np.sqrt(((crisp_df.loc[alt] - pd.Series(FPIS))**2).sum())
    D_neg[alt] = np.sqrt(((crisp_df.loc[alt] - pd.Series(FNIS))**2).sum())

distance_df = pd.DataFrame({
    "D+": D_pos,
    "D-": D_neg
})

print("\n6️⃣ Jarak ke FPIS & FNIS")
display(distance_df)

# =================================================
# 7️⃣ CLOSENESS COEFFICIENT & RANKING
# =================================================
CC = distance_df["D-"] / (distance_df["D+"] + distance_df["D-"])
ranking_df = CC.sort_values(ascending=False).to_frame("Closeness Coefficient")

print("\n7️⃣ RANKING AKHIR ALTERNATIF")
display(ranking_df)
    }

    df = pd.DataFrame(fuzzy_data, index=alternatives)

    weighted = {}
    for c in df.columns:
        w = weights[c]
        weighted[c] = [(l*w,m*w,u*w) for l,m,u in df[c]]

    wdf = pd.DataFrame(weighted, index=alternatives)
    crisp = wdf.applymap(lambda x:(x[0]+4*x[1]+x[2])/6)

    cost = ["HP","HO"]
    benefit = ["P","KP","KR","KM","KK"]

    FPIS, FNIS = {},{}
    for c in crisp.columns:
        if c in benefit:
            FPIS[c]=crisp[c].max()
            FNIS[c]=crisp[c].min()
        else:
            FPIS[c]=crisp[c].min()
            FNIS[c]=crisp[c].max()

    Dp,Dn={},{}
    for a in alternatives:
        Dp[a]=np.sqrt(((crisp.loc[a]-pd.Series(FPIS))**2).sum())
        Dn[a]=np.sqrt(((crisp.loc[a]-pd.Series(FNIS))**2).sum())

    CC = {a:Dn[a]/(Dp[a]+Dn[a]) for a in alternatives}
    best = max(CC, key=CC.get)

    return best, CC, crisp

def format_result(best, scores, crisp):
    app_full_name = {
        "GO": "GoFood (Gojek)",
        "GR": "GrabFood (Grab)",
        "SF": "ShopeeFood (Shopee)"
    }

    criteria_full_name = {
        "HP": "Harga Produk",
        "HO": "Harga Ongkir",
        "P":  "Promo",
        "KP": "Kecepatan Pengantaran",
        "KR": "Kelengkapan Restoran dan Menu",
        "KM": "Keadaan Makanan",
        "KK": "Keramahan Kurir"
    }

    # Nilai preferensi akhir
    best_score = scores[best]

    # Kontribusi relatif
    raw_scores = crisp.loc[best]
    contribution_ratio = raw_scores / raw_scores.sum()

    top_criteria = (
        contribution_ratio
        .sort_values(ascending=False)
        .head(3)
    )

    return {
        "best_app": app_full_name[best],
        "best_score": best_score,
        "top_criteria": {
            criteria_full_name[k]: v * 100
            for k, v in top_criteria.items()
        }
    }

# ==============================
# STREAMLIT UI
# ==============================
st.title("🍽️ Sistem Rekomendasi Aplikasi Pemesanan Makanan")

st.write("Silakan isi preferensi Anda berdasarkan perbandingan berikut:")

user_input = {}

for i, (A, B) in enumerate(questions, start=1):

    st.markdown(f"### Pertanyaan {i}")
    st.write("Menurut Anda, mana yang lebih penting?")
    st.markdown(f"**{criteria_full[A]}** dibandingkan **{criteria_full[B]}**")

    options = [
        f"{A} dan {B} sama penting",
        f"{A} sedikit lebih penting dari {B}",
        f"{A} lebih penting dari {B}",
        f"{A} jauh lebih penting dari {B}",
        f"{A} sangat jauh lebih penting dari {B}",
        f"{B} sedikit lebih penting dari {A}",
        f"{B} lebih penting dari {A}",
        f"{B} jauh lebih penting dari {A}",
        f"{B} sangat jauh lebih penting dari {A}"
    ]

    choice = st.selectbox(
        label="Jawaban:",
        options=options,
        key=f"q_{i}"
    )

    if choice == f"{A} dan {B} sama penting":
        val = 1
    elif choice == f"{A} sedikit lebih penting dari {B}":
        val = 3
    elif choice == f"{A} lebih penting dari {B}":
        val = 5
    elif choice == f"{A} jauh lebih penting dari {B}":
        val = 7
    elif choice == f"{A} sangat jauh lebih penting dari {B}":
        val = 9
    elif choice == f"{B} sedikit lebih penting dari {A}":
        val = 1 / 3
    elif choice == f"{B} lebih penting dari {A}":
        val = 1 / 5
    elif choice == f"{B} jauh lebih penting dari {A}":
        val = 1 / 7
    elif choice == f"{B} sangat jauh lebih penting dari {A}":
        val = 1 / 9

    user_input[(A, B)] = val


if st.button("🔍 Lihat Rekomendasi"):
    weights = run_ahp(user_input)
    best, scores, crisp = run_fuzzy_topsis(weights)

    result = format_result(best, scores, crisp)

    st.markdown("## 🍽️ HASIL REKOMENDASI APLIKASI PEMESANAN MAKANAN")
    st.markdown("---")

    st.success("✅ **Rekomendasi terbaik untuk Anda adalah:**")
    st.markdown(f"### 👉 {result['best_app']}")

    st.markdown(f"📊 **Nilai preferensi akhir:** `{result['best_score']:.4f}`")

    st.markdown("### 🔍 Alasan utama rekomendasi ini:")
    for crit, val in result["top_criteria"].items():
        st.markdown(f"- **{crit}**, berkontribusi sekitar **{val:.1f}%**")

    st.info(
        "💡 **Catatan:**\n\n"
        "Persentase menunjukkan kontribusi relatif setiap kriteria "
        "terhadap skor akhir alternatif yang direkomendasikan."
    )
