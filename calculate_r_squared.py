import numpy as np
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Serializacja
X = np.array([1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000])
y = np.array([17.297, 34.666, 53.177, 72.136, 91.483, 111.434, 136.916, 167.971, 208.783, 289.611])

# Parsowanie
X_2 = np.array([100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000])
y_2 = np.array([28.901, 58.009, 87.427, 116.267, 146.931, 178.106, 207.644, 244.495, 296.662, 340.544])

def linear_regression(X, y):
    coefficients = np.polyfit(X, y, 1)
    p = np.poly1d(coefficients)
    y_pred = p(X)
    r_squared = r2_score(y, y_pred)
    return r_squared, y_pred

def polynomial_regression(X, y, degree):
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(X.reshape(-1, 1))
    model = LinearRegression().fit(X_poly, y)
    y_pred = model.predict(X_poly)
    r_squared = r2_score(y, y_pred)
    return r_squared, y_pred

def power_regression(X, y):
    log_X = np.log(X)
    log_y = np.log(y)
    coefficients = np.polyfit(log_X, log_y, 1)
    p = np.poly1d(coefficients)
    y_pred_log = p(log_X)
    y_pred = np.exp(y_pred_log)
    r_squared = r2_score(y, y_pred)
    return r_squared, y_pred

r2_linear_serialization, _ = linear_regression(X, y)
r2_quadratic_serialization, _ = polynomial_regression(X, y, 2)
r2_power_serialization, _ = power_regression(X, y)

r2_linear_parsing, _ = linear_regression(X_2, y_2)
r2_quadratic_parsing, _ = polynomial_regression(X_2, y_2, 2)
r2_power_parsing, _ = power_regression(X_2, y_2)

print(f"Serializacja: Współczynnik determinacji (R^2) dla modelu liniowego: {r2_linear_serialization:.4f}")
print(f"Serializacja: Współczynnik determinacji (R^2) dla modelu kwadratowego: {r2_quadratic_serialization:.4f}")
print(f"Serializacja: Współczynnik determinacji (R^2) dla modelu potęgowego: {r2_power_serialization:.4f}")

print(f"Parsowanie: Współczynnik determinacji (R^2) dla modelu liniowego: {r2_linear_parsing:.4f}")
print(f"Parsowanie: Współczynnik determinacji (R^2) dla modelu kwadratowego: {r2_quadratic_parsing:.4f}")
print(f"Parsowanie: Współczynnik determinacji (R^2) dla modelu potęgowego: {r2_power_parsing:.4f}")
