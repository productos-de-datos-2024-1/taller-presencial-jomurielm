"""Autograding script"""

import os

# test code files
assert os.path.exists("src/7b_docker_client/config.json")
assert os.path.exists("src/7b_docker_client/app.py")
assert os.path.exists("src/7b_docker_client/Dockerfile")
assert os.path.exists("src/7b_docker_client/templates/index.html")


# test run
assert os.path.exists("datalake/logs/docker_api_client.log")
