#
# Usage from command line:
#
#
import requests


def make_request():
    """Make a request to the API server"""

    url = "http://127.0.0.1:5001"

    data = {
        "bathrooms": "2",
        "bedrooms": "3",
        "sqft_living": "1800",
        "sqft_lot": "2200",
        "floors": "1",
        "waterfront": "1",
        "condition": "3",
    }

    response = requests.post(url, json=data, timeout=5)

    print(response.text)


if __name__ == "__main__":
    make_request()