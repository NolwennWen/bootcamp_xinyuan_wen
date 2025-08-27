# /src/models.py
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

def fit_linear_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    y_hat = model.predict(X)
    metrics = {
        'r2': r2_score(y, y_hat),
        'mae': mean_absolute_error(y, y_hat)
    }
    return model, metrics

def save_model(model, path):
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def load_model(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def fit_and_metrics(X: np.ndarray, y: np.ndarray) -> dict:
    model = LinearRegression()
    model.fit(X, y)
    y_hat = model.predict(X)
    return {
        'slope': float(model.coef_[0]),
        'intercept': float(model.intercept_),
        'r2': float(r2_score(y, y_hat)),
        'mae': float(mean_absolute_error(y, y_hat))
    }
