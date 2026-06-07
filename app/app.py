import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from cardekho_styles import ENHANCED_CSS, NAVBAR_HTML, FOOTER_HTML, HERO_HTML, result_card_html

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CarDekho — Prédiction Prix",
    page_icon=":material/directions_car:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────
# LOAD ARTIFACTS
# ─────────────────────────────────────────────────────────────────
MODELS_DIR = Path(__file__).parent.parent / "models"

@st.cache_resource
def load_artifacts():
    model_xgb  = joblib.load(MODELS_DIR / "model_xgb.pkl")
    model_rf   = joblib.load(MODELS_DIR / "model_rf.pkl")
    model_lr   = joblib.load(MODELS_DIR / "model_lr.pkl")
    model_svr  = joblib.load(MODELS_DIR / "model_svr.pkl")
    scaler_svr = joblib.load(MODELS_DIR / "scaler_svr.pkl")
    columns    = joblib.load(MODELS_DIR / "columns.pkl")
    scaler     = joblib.load(MODELS_DIR / "scaler.pkl")
    le         = joblib.load(MODELS_DIR / "label_encoder.pkl")
    with open(MODELS_DIR / "model_metrics.json", "r", encoding="utf-8") as f:
        metrics = json.load(f)
    return model_xgb, model_rf, model_lr, model_svr, scaler_svr, columns, scaler, le, metrics

model_xgb, model_rf, model_lr, model_svr, scaler_svr, columns, scaler, le, metrics = load_artifacts()

MODELS = {
    "XGBoost (Meilleur)": model_xgb,
    "Random Forest":       model_rf,
    "Régression Linéaire": model_lr,
    "SVR":                 model_svr,
}

REFERENCE_YEAR = 2024
SORTED_BRANDS  = sorted(le.classes_.tolist())

OWNER_MAP = {
    "1er propriétaire"          : 1,
    "2ème propriétaire"         : 2,
    "3ème propriétaire"         : 3,
    "4ème propriétaire et +"    : 4,
    "Véhicule de démonstration" : 5,
}
FUEL_FR_TO_EN = {
    "Essence"    : "Petrol",
    "Diesel"     : "Diesel",
    "GNV"        : "CNG",
    "GPL"        : "LPG",
    "Électrique" : "Electric",
}
SELLER_FR_TO_EN = {
    "Particulier"              : "Individual",
    "Concessionnaire"          : "Dealer",
    "Concessionnaire certifié" : "Trustmark Dealer",
}

# ─────────────────────────────────────────────────────────────────
# INJECT DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────
st.markdown(ENHANCED_CSS, unsafe_allow_html=True)
st.markdown(NAVBAR_HTML,  unsafe_allow_html=True)
st.markdown(FOOTER_HTML,  unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# HELPERS — prediction
# ─────────────────────────────────────────────────────────────────
def _predict_batch(model_name, model_obj, feat_df):
    X = scaler_svr.transform(feat_df) if "SVR" in model_name else feat_df
    return np.maximum(model_obj.predict(X), 0)

def _predict(model_name, model_obj, feat_df):
    return float(_predict_batch(model_name, model_obj, feat_df)[0])

# ─────────────────────────────────────────────────────────────────
# HELPERS — preprocessing
# ─────────────────────────────────────────────────────────────────
def preprocess_single(year, km_driven, fuel, seller_type, transmission, owner_label, brand):
    car_age       = REFERENCE_YEAR - year
    owner_encoded = OWNER_MAP.get(owner_label, 1)
    try:    brand_encoded = int(le.transform([brand])[0])
    except: brand_encoded = int(le.transform(["Maruti"])[0])
    scaled = scaler.transform(
        pd.DataFrame([{"km_driven": km_driven, "car_age": car_age, "year": year}])
    )[0]
    km_sc, age_sc, year_sc = scaled[0], scaled[1], scaled[2]
    row = {
        "year": year_sc, "km_driven": km_sc, "car_age": age_sc,
        "owner_encoded": owner_encoded,
        "fuel_Diesel":   1 if fuel == "Diesel"   else 0,
        "fuel_Electric": 1 if fuel == "Electric" else 0,
        "fuel_LPG":      1 if fuel == "LPG"      else 0,
        "fuel_Petrol":   1 if fuel == "Petrol"   else 0,
        "seller_type_Individual":       1 if seller_type == "Individual"       else 0,
        "seller_type_Trustmark Dealer": 1 if seller_type == "Trustmark Dealer" else 0,
        "transmission_Manual": 1 if transmission == "Manuel" else 0,
        "brand_encoded": brand_encoded,
    }
    return pd.DataFrame([row])[list(columns)]


def preprocess_batch(df_raw):
    df = df_raw.copy()
    if "selling_price" in df.columns:
        df = df.drop("selling_price", axis=1)
    if "car_age" in df.columns and "owner_encoded" in df.columns and "name" not in df.columns:
        for col in columns:
            if col not in df.columns: df[col] = 0
        return df[list(columns)].astype(float)
    df["car_age"] = REFERENCE_YEAR - df["year"].astype(int)
    owner_map_raw = {
        "First Owner": 1, "Second Owner": 2, "Third Owner": 3,
        "Fourth & Above Owner": 4, "Test Drive Car": 5,
    }
    df["owner_encoded"] = (
        df.get("owner", pd.Series(["First Owner"] * len(df)))
          .map(owner_map_raw).fillna(1).astype(int)
    )
    def safe_encode(b):
        try:    return int(le.transform([b])[0])
        except: return int(le.transform(["Maruti"])[0])
    if "name" in df.columns:
        df["brand"] = df["name"].apply(lambda x: str(x).split()[0])
        df["brand_encoded"] = df["brand"].apply(safe_encode)
    elif "brand_encoded" not in df.columns:
        df["brand_encoded"] = safe_encode("Maruti")
    scaled_vals = scaler.transform(df[["km_driven", "car_age", "year"]].astype(float))
    df["km_driven"] = scaled_vals[:, 0]
    df["car_age"]   = scaled_vals[:, 1]
    df["year"]      = scaled_vals[:, 2]
    fuel_col = df.get("fuel", pd.Series(["CNG"] * len(df)))
    df["fuel_Diesel"]   = (fuel_col == "Diesel").astype(int)
    df["fuel_Electric"] = (fuel_col == "Electric").astype(int)
    df["fuel_LPG"]      = (fuel_col == "LPG").astype(int)
    df["fuel_Petrol"]   = (fuel_col == "Petrol").astype(int)
    st_col = df.get("seller_type", pd.Series(["Dealer"] * len(df)))
    df["seller_type_Individual"]       = (st_col == "Individual").astype(int)
    df["seller_type_Trustmark Dealer"] = (st_col == "Trustmark Dealer").astype(int)
    tr_col = df.get("transmission", pd.Series(["Automatic"] * len(df)))
    df["transmission_Manual"] = (tr_col == "Manual").astype(int)
    for col in columns:
        if col not in df.columns: df[col] = 0
    return df[list(columns)].astype(float)

# ─────────────────────────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

# ══════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "home":

    st.markdown(HERO_HTML, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Véhicules analysés", "8 128")
    c2.metric("Algorithmes comparés", "4")
    c3.metric("Meilleur R² — XGBoost", "0.75")
    c4.metric("Variables utilisées", "~12")

    st.markdown("""
<div style="background:#F5F3EF; border:1px solid rgba(28,25,23,0.12); border-radius:6px;
            padding:10px 18px; display:flex; justify-content:space-between; align-items:center;
            font-family:'DM Mono',monospace; font-size:11px; color:#78716C; margin:8px 0 4px;">
    <span>XGBoost &nbsp;·&nbsp; Random Forest &nbsp;·&nbsp; SVR &nbsp;·&nbsp; Régression Linéaire</span>
    <span>Prédiction individuelle &amp; en masse (CSV)</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <p class="section-label">Guide d'utilisation</p>
    <h3>Comment ça fonctionne ?</h3>
    """, unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">01 — Saisir</div>
            <h4>Caractéristiques du véhicule</h4>
            <p>Renseignez la marque, l'année, le kilométrage, le carburant et la transmission.</p>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">02 — Choisir</div>
            <h4>L'algorithme de prédiction</h4>
            <p>Sélectionnez parmi XGBoost, Random Forest, Régression Linéaire ou SVR.</p>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">03 — Obtenir</div>
            <h4>L'estimation en ₹ et en €</h4>
            <p>Le prix prédit s'affiche avec la comparaison des 4 modèles.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <p class="section-label">À propos des données</p>
    <h3>Le dataset CarDekho</h3>
    """, unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        st.markdown("""
        Le dataset provient de **CarDekho**, l'une des plus grandes
        plateformes de vente de voitures d'occasion en Inde.

        Chaque annonce contient : marque, année de fabrication,
        kilométrage, type de carburant, type de vendeur, transmission
        et nombre de propriétaires précédents.
        """)
    with d2:
        st.markdown("""
        | Variable | Description |
        |---|---|
        | `car_age` | Ancienneté du véhicule |
        | `km_driven` | Kilométrage total |
        | `fuel` | Type de carburant |
        | `transmission` | Manuelle / Automatique |
        | `seller_type` | Particulier / Concessionnaire |
        | `owner` | Nombre de propriétaires |
        | `brand` | Marque du véhicule |
        """)

    st.markdown("")
    if st.button("Commencer la prédiction →", type="primary", use_container_width=True):
        st.session_state.page = "app"
        st.rerun()

    st.stop()

# ══════════════════════════════════════════════════════════════
# APP PAGE — back button + tabs
# ══════════════════════════════════════════════════════════════
if st.button("← Accueil", key="back_home"):
    st.session_state.page = "home"
    st.rerun()

tab1, tab2, tab3 = st.tabs([
    ":material/edit_note:  Saisie Manuelle",
    ":material/folder_open:  Import CSV / Excel",
    ":material/bar_chart:  Comparaison des Modèles",
])

# ══════════════════════════════════════════════════════════════
# TAB 1 — SAISIE MANUELLE
# ══════════════════════════════════════════════════════════════
with tab1:
    model_key_map = {
        "XGBoost (Meilleur)": "XGBoost",
        "Random Forest":       "Random Forest",
        "Régression Linéaire": "Régression Linéaire",
        "SVR":                 "SVR",
    }
    r2_by_name = {name: metrics[mk]["r2"] for name, mk in model_key_map.items()}

    algo_col, form_col = st.columns([1.1, 1.8])

    # ── LEFT: Algorithm selector ──────────────────────────────
    with algo_col:
        st.markdown('<p class="section-label">Algorithme</p>', unsafe_allow_html=True)

        selected_model_name = st.radio(
            "Algorithme",
            list(MODELS.keys()),
            index=0,
            label_visibility="collapsed",
            format_func=lambda x: (
                f"XGBoost  ·  MEILLEUR\nR² = {r2_by_name[x]:.4f}"
                if "XGBoost" in x
                else f"{x}\nR² = {r2_by_name[x]:.4f}"
            ),
        )
        selected_model = MODELS[selected_model_name]
        mk = model_key_map[selected_model_name]
        m  = metrics[mk]

        mae_l  = m["mae"]  / 100_000
        rmse_l = m["rmse"] / 100_000

        st.markdown(f"""
        <div class="algo-metrics-grid">
            <div class="algo-metric">
                <div class="algo-metric-label">R² Test</div>
                <div class="algo-metric-value">{m['r2']:.3f}</div>
            </div>
            <div class="algo-metric">
                <div class="algo-metric-label">CV R²</div>
                <div class="algo-metric-value">{m['cv_r2_mean']:.3f}</div>
            </div>
            <div class="algo-metric">
                <div class="algo-metric-label">MAE</div>
                <div class="algo-metric-value">{mae_l:.2f}L ₹</div>
            </div>
            <div class="algo-metric">
                <div class="algo-metric-label">RMSE</div>
                <div class="algo-metric-value">{rmse_l:.2f}L ₹</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT: Form ───────────────────────────────────────────
    with form_col:
        st.markdown('<p class="section-label">Saisie Manuelle</p>', unsafe_allow_html=True)

        fc1, fc2 = st.columns(2)
        with fc1:
            brand = st.selectbox(
                "Marque", SORTED_BRANDS,
                index=SORTED_BRANDS.index("Maruti") if "Maruti" in SORTED_BRANDS else 0,
            )
        with fc2:
            year = st.number_input(
                "Année de fabrication",
                min_value=1992, max_value=2024, value=2015, step=1,
            )

        fc3, fc4 = st.columns(2)
        with fc3:
            km_driven = st.number_input(
                "Kilomètres parcourus",
                min_value=0, max_value=500_000, value=50_000, step=1000,
            )
        with fc4:
            fuel_fr = st.selectbox("Carburant", list(FUEL_FR_TO_EN.keys()))

        fc5, fc6 = st.columns(2)
        with fc5:
            seller_type_fr = st.selectbox("Type de vendeur", list(SELLER_FR_TO_EN.keys()))
        with fc6:
            transmission = st.selectbox("Transmission", ["Manuel", "Automatique"])

        fc7, fc8 = st.columns(2)
        with fc7:
            owner_label = st.selectbox("Nombre de propriétaires", list(OWNER_MAP.keys()))
        with fc8:
            car_age_display = REFERENCE_YEAR - year
            st.metric("Âge du véhicule", f"{car_age_display} ans")

        st.markdown("")
        predict_btn = st.button(
            "Prédire le Prix", use_container_width=True, type="primary",
            key="predict_manual",
        )

        if predict_btn:
            try:
                input_df = preprocess_single(
                    year, km_driven,
                    FUEL_FR_TO_EN[fuel_fr],
                    SELLER_FR_TO_EN[seller_type_fr],
                    transmission, owner_label, brand,
                )
                pred      = _predict(selected_model_name, selected_model, input_df)
                all_preds = {mn: _predict(mn, mo, input_df) for mn, mo in MODELS.items()}

                car_label = f"{brand} · {year} · {km_driven:,} km"
                st.markdown(
                    result_card_html(pred, selected_model_name, car_label),
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Erreur lors de la prédiction : {e}")
                st.exception(e)

    # ── Full-width: comparison + raw features ─────────────────
    if predict_btn:
        try:
            st.markdown("---")
            st.markdown("#### Comparaison des prédictions")
            comp_df = pd.DataFrame([
                {"Modèle": k, "Prix prédit (₹)": f"{v:,.0f}", "Prix prédit (€)": f"{v/90:,.0f}"}
                for k, v in all_preds.items()
            ])
            st.dataframe(comp_df.set_index("Modèle"), use_container_width=True)

            with st.expander("Données envoyées au modèle (après prétraitement)"):
                st.dataframe(
                    input_df.T.rename(columns={0: "Valeur standardisée"}),
                    use_container_width=True,
                )
        except Exception:
            pass

# ══════════════════════════════════════════════════════════════
# TAB 2 — IMPORT CSV / EXCEL
# ══════════════════════════════════════════════════════════════
with tab2:
    _bkey = {
        "XGBoost (Meilleur)": "XGBoost",
        "Random Forest":       "Random Forest",
        "Régression Linéaire": "Régression Linéaire",
        "SVR":                 "SVR",
    }
    _br2 = {n: metrics[k]["r2"] for n, k in _bkey.items()}

    b_algo_col, b_content_col = st.columns([1.1, 1.8])

    # ── LEFT: Algorithm selector ──────────────────────────────
    with b_algo_col:
        st.markdown('<p class="section-label">Algorithme</p>', unsafe_allow_html=True)

        selected_batch_model_name = st.radio(
            "Algorithme batch",
            list(MODELS.keys()),
            index=0,
            label_visibility="collapsed",
            format_func=lambda x: (
                f"XGBoost  ·  MEILLEUR\nR² = {_br2[x]:.4f}"
                if "XGBoost" in x
                else f"{x}\nR² = {_br2[x]:.4f}"
            ),
            key="batch_algo_radio",
        )
        selected_batch_model = MODELS[selected_batch_model_name]
        bmk = _bkey[selected_batch_model_name]
        bm  = metrics[bmk]
        bmae_l  = bm["mae"]  / 100_000
        brmse_l = bm["rmse"] / 100_000

        st.markdown(f"""
        <div class="algo-metrics-grid">
            <div class="algo-metric">
                <div class="algo-metric-label">R² Test</div>
                <div class="algo-metric-value">{bm['r2']:.3f}</div>
            </div>
            <div class="algo-metric">
                <div class="algo-metric-label">CV R²</div>
                <div class="algo-metric-value">{bm['cv_r2_mean']:.3f}</div>
            </div>
            <div class="algo-metric">
                <div class="algo-metric-label">MAE</div>
                <div class="algo-metric-value">{bmae_l:.2f}L ₹</div>
            </div>
            <div class="algo-metric">
                <div class="algo-metric-label">RMSE</div>
                <div class="algo-metric-value">{brmse_l:.2f}L ₹</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT: Import + results ───────────────────────────────
    with b_content_col:
        st.markdown('<p class="section-label">Import de fichier</p>', unsafe_allow_html=True)

        st.markdown("""
        <div class="format-card">
            <div class="format-card-title">Formats acceptés</div>
            <div class="format-row">
                <span class="format-tag">Format A</span>
                CSV brut CarDekho &mdash; colonnes&nbsp;
                <code>name, year, km_driven, fuel, seller_type, transmission, owner</code>
            </div>
            <div class="format-row">
                <span class="format-tag">Format B</span>
                CSV déjà nettoyé &mdash; colonnes&nbsp;
                <code>car_age</code> et <code>owner_encoded</code> déjà présentes
            </div>
            <div class="format-note">La colonne <code>selling_price</code> est ignorée si présente.</div>
        </div>
        """, unsafe_allow_html=True)

        exemple_csv = pd.DataFrame([
            {"name":"Maruti Swift VXI",    "year":2015,"km_driven":50000,
             "fuel":"Petrol","seller_type":"Individual","transmission":"Manual","owner":"First Owner"},
            {"name":"Hyundai i20 Asta",    "year":2018,"km_driven":30000,
             "fuel":"Diesel","seller_type":"Dealer",    "transmission":"Manual","owner":"Second Owner"},
            {"name":"Toyota Fortuner",     "year":2020,"km_driven":20000,
             "fuel":"Diesel","seller_type":"Dealer",    "transmission":"Automatic","owner":"First Owner"},
            {"name":"Honda City ZX",       "year":2016,"km_driven":65000,
             "fuel":"Petrol","seller_type":"Individual","transmission":"Manual","owner":"First Owner"},
            {"name":"Ford EcoSport Trend", "year":2019,"km_driven":45000,
             "fuel":"Diesel","seller_type":"Dealer",    "transmission":"Manual","owner":"First Owner"},
        ])

        dl_col, up_col = st.columns([1, 1.6])
        with dl_col:
            st.download_button(
                label="Télécharger un exemple (5 véhicules)",
                data=exemple_csv.to_csv(index=False).encode("utf-8"),
                file_name="exemple_input_cardekho.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with up_col:
            uploaded_file = st.file_uploader(
                "Importer votre fichier", type=["csv", "xlsx"],
                label_visibility="collapsed",
            )

        if uploaded_file is not None:
            try:
                df_raw = (
                    pd.read_excel(uploaded_file)
                    if uploaded_file.name.endswith(".xlsx")
                    else pd.read_csv(uploaded_file)
                )
                st.markdown(f'<p class="section-label">{len(df_raw)} véhicule(s) chargé(s)</p>',
                            unsafe_allow_html=True)
                st.dataframe(df_raw.head(), use_container_width=True)

                with st.spinner("Prédictions en cours…"):
                    df_processed = preprocess_batch(df_raw)
                    preds = _predict_batch(
                        selected_batch_model_name, selected_batch_model, df_processed
                    )

                df_result = df_raw.copy()
                df_result["Prix Prédit (₹)"] = preds.round(0).astype(int)
                df_result["Prix Prédit (€)"] = (preds / 90).round(0).astype(int)

                st.markdown('<p class="section-label">Résultats</p>', unsafe_allow_html=True)
                st.dataframe(df_result, use_container_width=True)

                rc1, rc2, rc3 = st.columns(3)
                rc1.metric("Prix moyen", f"{preds.mean():,.0f} ₹")
                rc2.metric("Prix minimum", f"{preds.min():,.0f} ₹")
                rc3.metric("Prix maximum", f"{preds.max():,.0f} ₹")

                st.download_button(
                    label="Télécharger les résultats (.csv)",
                    data=df_result.to_csv(index=False).encode("utf-8"),
                    file_name="predictions_cardekho.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
                st.success(
                    f"{len(df_raw)} prédiction(s) générée(s) avec **{selected_batch_model_name}**."
                )

            except Exception as e:
                st.error(f"Erreur : {e}")
                st.exception(e)

# ══════════════════════════════════════════════════════════════
# TAB 3 — COMPARAISON DES MODÈLES
# ══════════════════════════════════════════════════════════════
with tab3:
    t3_left, t3_right = st.columns([1.1, 1.8])

    # ── LEFT: Static model summary cards ─────────────────────
    with t3_left:
        st.markdown('<p class="section-label">Résultats</p>', unsafe_allow_html=True)

        _model_order = [
            ("XGBoost",            True),
            ("Random Forest",      False),
            ("Régression Linéaire",False),
            ("SVR",                False),
        ]
        for mname, is_best in _model_order:
            m = metrics[mname]
            badge_html = '<span class="summary-badge">MEILLEUR</span>' if is_best else ""
            st.markdown(f"""
            <div class="summary-card {'summary-card--best' if is_best else ''}">
                <div class="summary-card-header">
                    <span class="summary-card-name">{mname}</span>{badge_html}
                </div>
                <div class="summary-card-r2">R² = {m['r2']:.4f}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="conclusion-card">
            <div class="conclusion-label">Conclusion</div>
            <p>XGBoost est le meilleur modèle. Variables clés&nbsp;:
            <strong>transmission</strong>, <strong>année</strong>,
            <strong>carburant (Diesel)</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT: Detailed comparison + analysis ─────────────────
    with t3_right:
        st.markdown('<p class="section-label">Comparaison des algorithmes</p>',
                    unsafe_allow_html=True)
        st.markdown("""
        4 algorithmes de régression testés, optimisés via **GridSearchCV**
        et évalués par **validation croisée K-Fold (k=5)**.
        """)

        rows = []
        for name, m in metrics.items():
            row = {
                "Modèle":      name,
                "R² Test":     m["r2"],
                "MAE (₹)":     int(m["mae"]),
                "RMSE (₹)":    int(m["rmse"]),
                "CV R² Moy.":  m["cv_r2_mean"],
                "CV R² Std":   m["cv_r2_std"],
            }
            if "best_params" in m:
                row["Hyperparamètres"] = str(m["best_params"])
            rows.append(row)

        df_cmp = pd.DataFrame(rows).set_index("Modèle")

        def highlight_best(s):
            if s.name in ("R² Test", "CV R² Moy."):
                return ["background-color:#E8F4F3;color:#0A5652" if v == s.max() else "" for v in s]
            elif s.name in ("MAE (₹)", "RMSE (₹)"):
                return ["background-color:#E8F4F3;color:#0A5652" if v == s.min() else "" for v in s]
            return [""] * len(s)

        st.dataframe(
            df_cmp.style.apply(
                highlight_best, subset=["R² Test", "MAE (₹)", "RMSE (₹)", "CV R² Moy."]
            ),
            use_container_width=True,
        )

        st.markdown("---")
        st.markdown('<p class="section-label">Analyse</p>', unsafe_allow_html=True)

        a1, a2 = st.columns(2)
        with a1:
            st.markdown("""
            <div class="analysis-card">
                <div class="analysis-card-title">Régression Linéaire</div>
                <ul>
                    <li>R² ≈ 0.59 — 59 % de variance expliquée</li>
                    <li>Modèle simple, interprétable</li>
                    <li>Sert de <em>baseline</em></li>
                </ul>
            </div>
            <div class="analysis-card">
                <div class="analysis-card-title">Random Forest</div>
                <ul>
                    <li>R² ≈ 0.73 — nette amélioration</li>
                    <li>Robuste aux valeurs aberrantes</li>
                    <li>Bonne généralisation (CV stable)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with a2:
            st.markdown("""
            <div class="analysis-card analysis-card--best">
                <div class="analysis-card-title">XGBoost — Meilleur modèle</div>
                <ul>
                    <li>R² ≈ 0.75 — meilleur score global</li>
                    <li>Gradient boosting régularisé</li>
                    <li>CV très stable (std ≈ 0.01)</li>
                </ul>
            </div>
            <div class="analysis-card">
                <div class="analysis-card-title">SVR</div>
                <ul>
                    <li>R² ≈ −0.01 — sous-performance majeure</li>
                    <li>Sensible à l'échelle des données</li>
                    <li>Non recommandé pour cette tâche</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<p class="section-label">Importance des variables — XGBoost</p>',
                    unsafe_allow_html=True)

        fi_data = {
            "transmission_Manual":          0.3163,
            "year":                         0.2613,
            "fuel_Diesel":                  0.2421,
            "brand_encoded":                0.0587,
            "seller_type_Individual":       0.0452,
            "km_driven":                    0.0267,
            "seller_type_Trustmark Dealer": 0.0213,
            "owner_encoded":                0.0162,
            "fuel_Petrol":                  0.0086,
            "fuel_LPG":                     0.0034,
            "car_age":                      0.0,
            "fuel_Electric":                0.0,
        }
        fi_max = max(fi_data.values()) or 1
        fi_rows_html = "".join(
            f'<div class="fi-row">'
            f'<div class="fi-name">{var}</div>'
            f'<div class="fi-bar-wrap"><div class="fi-bar" style="width:{imp/fi_max*100:.1f}%"></div></div>'
            f'<div class="fi-pct">{imp*100:.1f}%</div>'
            f'</div>'
            for var, imp in fi_data.items()
        )
        st.markdown(f'<div style="margin-top:8px">{fi_rows_html}</div>', unsafe_allow_html=True)
