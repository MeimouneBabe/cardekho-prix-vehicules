import json
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import KFold, cross_val_score


def evaluate(model, X_test, y_test) -> dict:
    y_pred = model.predict(X_test)
    return {
        "r2":   round(float(r2_score(y_test, y_pred)), 4),
        "mae":  round(float(mean_absolute_error(y_test, y_pred)), 0),
        "rmse": round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 0),
    }


def cross_validate(model, X, y, n_splits: int = 5) -> dict:
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=kf, scoring="r2")
    return {
        "cv_r2_mean": round(float(scores.mean()), 4),
        "cv_r2_std":  round(float(scores.std()), 4),
    }


def compare_models(results: dict) -> pd.DataFrame:
    rows = [{"Modele": name, **m} for name, m in results.items()]
    return pd.DataFrame(rows).set_index("Modele")


def save_metrics(metrics: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False, default=float)
    print(f"Metrics saved -> {path}")
