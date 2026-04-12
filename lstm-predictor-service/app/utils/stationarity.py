# stationarity.py
"""
Statistical tests for time series stationarity.
Optional utilities for analyzing traffic data characteristics.
"""

from statsmodels.tsa.stattools import adfuller, kpss


def adf_test(series, name=""):
    """
    Augmented Dickey-Fuller Test
    Tests if a time series is stationary.

    H0 (null hypothesis): Series has a unit root (non-stationary)
    H1 (alternative): Series is stationary

    Args:
        series: Time series data (1D array)
        name: Label for output

    Returns:
        dict with test statistic, p-value, and interpretation
    """
    result = adfuller(series, autolag='AIC')

    return {
        'test_statistic': result[0],
        'p_value': result[1],
        'lags': result[2],
        'critical_values': result[4],
        'is_stationary': result[1] < 0.05,
        'name': name
    }


def kpss_test(series, name=""):
    """
    Kwiatkowski-Phillips-Schmidt-Shin Test
    Alternative stationarity test (inverse hypotheses to ADF).

    H0 (null hypothesis): Series is stationary
    H1 (alternative): Series has a unit root (non-stationary)

    Args:
        series: Time series data (1D array)
        name: Label for output

    Returns:
        dict with test statistic, p-value, and interpretation
    """
    result = kpss(series, regression='c', nlags='auto')

    return {
        'test_statistic': result[0],
        'p_value': result[1],
        'lags': result[2],
        'critical_values': result[3],
        'is_stationary': result[1] > 0.05,  # Note: inverse interpretation
        'name': name
    }


def test_stationarity(series, name="Traffic Density"):
    """
    Run both ADF and KPSS tests and summarize.

    Args:
        series: Time series data
        name: Label for output

    Returns:
        dict with both test results and final verdict
    """
    adf_result = adf_test(series, name)
    kpss_result = kpss_test(series, name)

    # Consensus: stationary if both agree
    consensus_stationary = adf_result['is_stationary'] and kpss_result['is_stationary']

    return {
        'adf': adf_result,
        'kpss': kpss_result,
        'consensus_stationary': consensus_stationary,
        'recommendation': "Data is stationary" if consensus_stationary else "Consider differencing or detrending"
    }
