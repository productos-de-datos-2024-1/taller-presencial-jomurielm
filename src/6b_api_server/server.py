"""API server example



Usage from command line:

```bash
$ curl http://127.0.0.1:5001 -X POST -H "Content-Type: application/json"  -d '{"bathrooms": "2", "bedrooms": "3", "sqft_living": "1800",  "sqft_lot": "2200", "floors": "1", "waterfront": "1", "condition": "3"}'
1605832.1056204173%  

curl http://127.0.0.1:5001 -X POST -H "Content-Type: application/json" -d "{\"bathrooms\": \"2\", \"bedrooms\": \"3\", \"sqft_living\": \"1800\", \"sqft_lot\": \"2200\", \"floors\": \"1\", \"waterfront\": \"1\", \"condition\": \"3\"}"

"""

import json
import logging
import os.path
import pickle

import pandas as pd
import pkg_resources
from flask import Flask, request

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------


CONFIG_FILE = "config.json"

if not pkg_resources.resource_exists(__name__, CONFIG_FILE):
    raise FileNotFoundError(f"File {CONFIG_FILE} not found")

with pkg_resources.resource_stream(__name__, CONFIG_FILE) as f:
    config = json.load(f)

logging.basicConfig(
    filename=os.path.join(config["logs_dir"], config["api_server_log"]),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


# -----------------------------------------------------------------------------
# API Server
# -----------------------------------------------------------------------------

app = Flask(__name__)
app.config["SECRET_KEY"] = "api-server-secret-key"

# Model features used for prediction
FEATURES = [
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "waterfront",
    "condition",
]


@app.route("/", methods=["POST"])
def index():
    """API function"""

    # model input
    args = request.json
    filt_args = {key: [int(args[key])] for key in FEATURES}
    df = pd.DataFrame.from_dict(filt_args)
    logging.info("User values: %s", filt_args)

    # prediction
    path = os.path.join(config["models_dir"], config["house_prices_model"])
    with open(path, "rb") as file:
        loaded_model = pickle.load(file)
    prediction = loaded_model.predict(df)
    logging.info("Prediction: %s", prediction)

    # result
    return str(prediction[0])


if __name__ == "__main__":
    app.run(debug=True, port=5001)