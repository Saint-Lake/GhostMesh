import os
from pathlib import Path


HOME = Path.home()
CONFIG_PATH = HOME / ".ghostmesh_id"
C2_URL = "https://127.0.0.1:8443"
REGISTER_ENDPOINT = "/agent/register"
LOGIN_ENDPOINT = "/agent/login"
BEACON_ENDPOINT = "/agent/beacon"
RESULT_ENDPOINT = "/agent/result"