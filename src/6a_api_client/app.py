"""Web application to deploy the model"""

import json
import logging
import os.path

import pkg_resources
import requests
from flask import Flask, render_template, request

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

CONFIG_FILE = "config.json"

if not pkg_resources.resource_exists(__name__, CONFIG_FILE):
    raise FileNotFoundError(f"File {CONFIG_FILE} not found")


with pkg_resources.resource_stream(__name__, CONFIG_FILE) as f:
    config = json.load(f)

logging.basicConfig(
    filename=os.path.join(config["logs_dir"], config["api_client_log"]),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

# -----------------------------------------------------------------------------
# Web application
# -----------------------------------------------------------------------------

app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    """Main web page"""

    if request.method == "POST":

        user_values = {}

        user_values["bedrooms"] = float(request.form["bedrooms"])
        user_values["bathrooms"] = float(request.form["bathrooms"])
        user_values["sqft_living"] = float(request.form["sqft_living"])
        user_values["sqft_lot"] = float(request.form["sqft_lot"])
        user_values["floors"] = float(request.form["floors"])

        if request.form.get("waterfront") == "Yes":
            user_values["waterfront"] = 0
        else:
            user_values["waterfront"] = 1

        if request.form.get("condition") == "1":
            user_values["condition"] = 1
        elif request.form.get("condition") == "2":
            user_values["condition"] = 2
        elif request.form.get("condition") == "3":
            user_values["condition"] = 3
        elif request.form.get("condition") == "4":
            user_values["condition"] = 4
        else:
            user_values["condition"] = 5

        logging.info("User values: %s", user_values)

        url = config["api_server_url"]
        response = requests.post(url, json=user_values, timeout=5)
        prediction = round(float(response.text), 2)

        logging.info("Prediction: %s", prediction)

    else:
        prediction = None

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    logging.info("Starting the application")
    app.run(debug=True, port=5002)
    logging.info("Starting the application")