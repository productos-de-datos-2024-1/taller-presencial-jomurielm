"""Entrenamiento de un modelo de regresión usando sklearn"""

import glob
import json
import os.path

import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

CONFIG_FILE = "config/config.json"

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = json.load(file)

path = os.path.join(config["sample_path"], "*.csv.zip")
filenames = glob.glob(path)
dfs = []
for filename in filenames:
    dfs.append(pd.read_csv(filename, sep=",", compression="zip"))
df = pd.concat(dfs, ignore_index=True)


features = df[
    [
        "bedrooms",
        "bathrooms",
        "sqft_living",
        "sqft_lot",
        "floors",
        "waterfront",
        "condition",
    ]
]

target = df["price"]


(x_train, x_test, target_train, target_test) = train_test_split(
    features,
    target,
    test_size=0.25,
)

best_model = None
best_model_r2 = None

for k in range(1, 8):

    # se crea el modelo de regresión lineal y luego lo entreno
    model = LinearRegression()

    # aca se crea un scaler de sklearn para escalar los datos
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_scaled = scaler.transform(x_train)

    # uso la funcion selectkbest de sklearn para obtener las k mejores features
    select_regressors = SelectKBest(score_func=f_regression, k=k)
    select_regressors.fit(x_scaled, target_train)
    x = select_regressors.transform(x_scaled)

    # entrenamiento del modelo y pronostico del cojunto de test
    model.fit(x, target_train)

    x_test_scaled = select_regressors.transform(scaler.transform(x_test))
    y = model.predict(x_test_scaled)

    # calculo de los errores mse, mae y r2
    linear_regresion_mse = mean_squared_error(target_test, y)
    linear_regresion_mae = mean_absolute_error(target_test, y)
    linear_regresion_r2 = r2_score(target_test, y)

    # imprime el reporte:
    print("linear_regresion :")
    print(f"  MSE: {linear_regresion_mse}")
    print(f"  MAE: {linear_regresion_mae}")
    print(f"  R2: {linear_regresion_r2}")
    print()

    if best_model is None or linear_regresion_r2 > best_model_r2:
        best_model = model
        best_model_r2 = linear_regresion_r2


#
for neighbors in range(1, 5):

    for n in range(1, 8):
        # se crea un modelo de regresión knn y se entrena
        knn = KNeighborsRegressor(n_neighbors=neighbors)

        scaler = StandardScaler()
        scaler.fit(x_train)
        x_scaled = scaler.transform(x_train)

        # uso la funcion selectkbest
        select_regressors_knn = SelectKBest(score_func=f_regression, k=n)
        select_regressors_knn.fit(x_scaled, target_train)
        x = select_regressors_knn.transform(x_scaled)

        knn.fit(x, target_train)

        x = select_regressors_knn.transform(scaler.transform(x_test))
        y = knn.predict(x)

        mse = mean_squared_error(target_test, y)
        mae = mean_absolute_error(target_test, y)
        r2 = r2_score(target_test, y)

        print(f"knn regression (k={neighbors}):")
        print(f"  MSE: {mse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")
        print()

        if best_model is None or r2 > best_model_r2:
            best_model = knn
            best_model_r2 = r2

print(f"Best model: {best_model}")
print(f"Best R2: {best_model_r2}")