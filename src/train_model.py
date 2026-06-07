import joblib
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor


def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, {}


def train_random_forest(X_train, y_train):
    gs = GridSearchCV(
        RandomForestRegressor(random_state=42),
        {"n_estimators": [100, 200], "max_depth": [10, 20, None],
         "min_samples_split": [2, 5]},
        cv=3, scoring="r2", n_jobs=-1,
    )
    gs.fit(X_train, y_train)
    return gs.best_estimator_, gs.best_params_


def train_xgboost(X_train, y_train):
    gs = GridSearchCV(
        XGBRegressor(random_state=42, verbosity=0),
        {"n_estimators": [100, 200], "max_depth": [4, 6],
         "learning_rate": [0.05, 0.1], "subsample": [0.8, 1.0]},
        cv=3, scoring="r2", n_jobs=-1,
    )
    gs.fit(X_train, y_train)
    return gs.best_estimator_, gs.best_params_


def train_svr(X_train, y_train):
    gs = GridSearchCV(
        SVR(kernel="rbf"),
        {"C": [10, 100], "gamma": ["scale", "auto"], "epsilon": [0.1, 1.0]},
        cv=3, scoring="r2", n_jobs=-1,
    )
    gs.fit(X_train, y_train)
    return gs.best_estimator_, gs.best_params_


def save_model(model, path: str):
    joblib.dump(model, path)
    print(f"Saved -> {path}")
