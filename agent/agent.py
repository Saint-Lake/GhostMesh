from identity import initialize_agent
# from core import run_beacon_loop  # hypothetical function
from config import C2_URL

def main():
    session = initialize_agent()
    jwt_token = session["jwt"]
    print(jwt_token)

    # run_beacon_loop(jwt_token)

if __name__ == "__main__":
    main()