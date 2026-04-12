# metrics.py
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


def mae(y_true, y_pred):
    """Mean Absolute Error"""
    return mean_absolute_error(y_true, y_pred)


def mse(y_true, y_pred):
    """Mean Squared Error"""
    return mean_squared_error(y_true, y_pred)


def rmse(y_true, y_pred):
    """Root Mean Squared Error"""
    return np.sqrt(mean_squared_error(y_true, y_pred))
