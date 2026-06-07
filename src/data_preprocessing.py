import pandas as pd

BOOL_COLS = [
    "fuel_Diesel", "fuel_Electric", "fuel_LPG", "fuel_Petrol",
    "seller_type_Individual", "seller_type_Trustmark Dealer",
    "transmission_Manual",
]


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for c in BOOL_COLS:
        if c in df.columns:
            df[c] = df[c].astype(int)
    return df


def split_features_target(df: pd.DataFrame, target: str = "selling_price"):
    return df.drop(columns=[target]), df[target]
