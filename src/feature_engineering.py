import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

REFERENCE_YEAR = 2024
OWNER_MAP = {
    "First Owner": 1, "Second Owner": 2, "Third Owner": 3,
    "Fourth & Above Owner": 4, "Test Drive Car": 5,
}


def create_car_age(df: pd.DataFrame, reference_year: int = REFERENCE_YEAR) -> pd.DataFrame:
    df = df.copy()
    df["car_age"] = reference_year - df["year"].astype(int)
    return df


def encode_owner(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["owner_encoded"] = df["owner"].map(OWNER_MAP).fillna(1).astype(int)
    return df


def encode_brands(df: pd.DataFrame, le: LabelEncoder = None):
    df = df.copy()
    df["brand"] = df["name"].apply(lambda x: str(x).split()[0])
    if le is None:
        le = LabelEncoder()
        df["brand_encoded"] = le.fit_transform(df["brand"])
    else:
        def _safe(b):
            try:
                return int(le.transform([b])[0])
            except Exception:
                return int(le.transform(["Maruti"])[0])
        df["brand_encoded"] = df["brand"].apply(_safe)
    return df, le


def one_hot_encode(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col, prefix in [("fuel", "fuel"), ("seller_type", "seller_type"),
                         ("transmission", "transmission")]:
        if col in df.columns:
            dummies = pd.get_dummies(df[col], prefix=prefix).astype(int)
            df = pd.concat([df, dummies], axis=1).drop(columns=[col])
    return df.drop(columns=["name", "brand", "owner"], errors="ignore")


def scale_numerical(df: pd.DataFrame, cols: list, scaler: StandardScaler = None):
    df = df.copy()
    if scaler is None:
        scaler = StandardScaler()
        df[cols] = scaler.fit_transform(df[cols])
    else:
        df[cols] = scaler.transform(df[cols])
    return df, scaler
