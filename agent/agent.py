from core import beacon_and_execute
import time

def main():
    while True:
        beacon_and_execute()
        time.sleep(60)

if __name__ == "__main__":
    main()