"""Entrenamiento de un modelo de regresión usando sklearn.

```bash
$ python3 src/model/train.py --help
usage: train.py [-h] [--max_features MAX_FEATURES] [--cv CV] [--max_neighbors MAX_NEIGHBORS]

House Prices Model Training

optional arguments:
  -h, --help            show this help message and exit
  --max_features MAX_FEATURES
                        Max number of features to use
  --cv CV               Number of cross-validation folds
  --max_neighbors MAX_NEIGHBORS
                        Max number of neighbors to use

                        
python src/model/train.py --max_features 7 --cv 5 --max_neighbors 10                        
                        
                        
```






"""

import argparse
import json
import logging
import os
import pickle

import pandas as pd
import pkg_resources
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------


CONFIG_FILE = "config.json"

if not pkg_resources.resource_exists(__name__, CONFIG_FILE):
    raise FileNotFoundError(f"File {CONFIG_FILE} not found")

with pkg_resources.resource_stream(__name__, CONFIG_FILE) as f:
    config = json.load(f)

logging.basicConfig(
    filename=os.path.join(config["logs_dir"], config["train_model_log"]),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


# -----------------------------------------------------------------------------
# Model definition
# -----------------------------------------------------------------------------


def make_pipeline(estimator):
    """Create a pipeline with a given estimator"""

    return Pipeline(
        [
            ("standarscaler", StandardScaler()),
            ("selectkbest", SelectKBest(score_func=f_regression)),
            ("estimator", estimator),
        ]
    )


def make_gridsearch(pipeline, param_grid, cv):
    """Create a gridsearch with a given pipeline and parameters"""

    return GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=cv,
    )


def make_linear_regressor(max_features, cv):
    """Create a gridsearch with a given pipeline and parameters"""

    model = LinearRegression()
    param_grid = {
        "selectkbest__k": range(1, max_features + 1),
    }
    pipeline = make_pipeline(model)
    gridsearch = make_gridsearch(pipeline, param_grid, cv=cv)
    return gridsearch


def make_knn_regressor(max_features, cv, max_neighbors):
    """Create a gridsearch with a given pipeline and parameters"""

    model = KNeighborsRegressor()
    param_grid = {
        "selectkbest__k": range(1, max_features),
        "estimator__n_neighbors": range(1, max_neighbors + 1),
    }
    pipeline = make_pipeline(model)
    gridsearch = make_gridsearch(pipeline, param_grid, cv=cv)
    return gridsearch


# -----------------------------------------------------------------------------
# Model metrics
# -----------------------------------------------------------------------------


def compute_metrics(y_true, y_pred):
    """Evaluate the model using mse, mae and r2"""

    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return mse, mae, r2


def report_metrics(estimator, mse, mae, r2):
    """Print the metrics of the model"""

    print(estimator, ":", sep="")
    print(f"  MSE: {mse}")
    print(f"  MAE: {mae}")
    print(f"   R2: {r2}")


# -----------------------------------------------------------------------------
# Model management
# -----------------------------------------------------------------------------


def load_model_from_disk():
    """Load the model from the disk"""

    path = os.path.join(config["models_dir"], config["house_prices_model"])
    if os.path.exists(path):
        model = pd.read_pickle(path)
    else:
        model = None

    return model


def save_model_to_disk(model):
    """Save the model to the disk"""

    path = os.path.join(config["models_dir"], config["house_prices_model"])
    with open(path, "wb") as file:
        pickle.dump(model, file)


def compare_saved_model_with_new_model(saved_model, new_model):
    """Compare the current model with the new model"""

    if saved_model is None:
        return new_model

    if new_model.best_score_ > saved_model.best_score_:
        return new_model

    return saved_model


# -----------------------------------------------------------------------------
# Data management
# -----------------------------------------------------------------------------


def load_train_and_test_datasets():
    """Load data from the datalake"""

    selected_columns = [
        "bedrooms",
        "bathrooms",
        "sqft_living",
        "sqft_lot",
        "floors",
        "waterfront",
        "condition",
    ]

    train_file_path = os.path.join(config["downsampled_dir"], config["train_dataset"])
    train_df = pd.read_csv(train_file_path)
    x_train = train_df[selected_columns]
    y_train = train_df["price"]

    test_file_path = os.path.join(config["downsampled_dir"], config["test_dataset"])
    test_df = pd.read_csv(test_file_path)
    x_test = test_df[selected_columns]
    y_test = test_df["price"]

    return x_train, x_test, y_train, y_test


def get_args_from_command_line():
    """Get the arguments from the command line"""

    parser = argparse.ArgumentParser(description="House Prices Model Training")

    parser.add_argument(
        "--max_features",
        type=int,
        default=7,
        help="Max number of features to use",
    )

    parser.add_argument(
        "--cv",
        type=int,
        default=5,
        help="Number of cross-validation folds",
    )
    parser.add_argument(
        "--max_neighbors",
        type=int,
        default=10,
        help="Max number of neighbors to use",
    )

    args = parser.parse_args()

    return args


def main():
    """Main function"""

    args = get_args_from_command_line()
    x_train, x_test, y_train_true, y_test_true = load_train_and_test_datasets()

    regressors = [
        #
        make_linear_regressor(
            max_features=args.max_features,
            cv=args.cv,
        ),
        #
        make_knn_regressor(
            max_features=args.max_features,
            cv=args.cv,
            max_neighbors=args.max_neighbors,
        ),
    ]

    for regressor in regressors:
        regressor.fit(x_train, y_train_true)

    best_model = load_model_from_disk()

    for new_model in regressors:
        best_model = compare_saved_model_with_new_model(best_model, new_model)
        save_model_to_disk(best_model)

    y_test_pred = best_model.predict(x_test)
    mse, mae, r2 = compute_metrics(y_test_true, y_test_pred)
    report_metrics(best_model, mse, mae, r2)


if __name__ == "__main__":
    main()