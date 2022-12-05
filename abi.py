# ---------------------------------------------------------------------
#                        NHN Vulnerability Scanner
# ---------------------------------------------------------------------

# Menu

def menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Menu Option 1 : Check For SQL Injection")
    print("2. Menu Option 2 : Check For XSS")
    print("3. Exit")


# set loop to True
loop = True

# While loop until loop = True
while loop:
    menu()
    choice = input("Enter your choice [1-3]: ")  # Input choice

    # End Program
    if choice == '3':
        print("Exiting")
        import os

        os.system("PAUSE")

    # SQL Injection Check
    elif choice == '1':
        import requests  # Importing Libraries
        from bs4 import BeautifulSoup as bs
        from urllib.parse import urljoin
        from pprint import pprint
        from datetime import datetime
        import time

        start = time.time()
        # Set a new Session (HTTP)
        s = requests.Session()
        s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 "

        # Captures all the HTML Sources
        def get_forms(url):
            soup = bs(s.get(url).content, "html.parser")
            return soup.find_all("form")

        # Get all the information
        def get_details(form):
            details = {}
            # Start the action
            try:
                action = form.attrs.get("action").lower()
            except:
                action = None
            # POST & GET Method
            method = form.attrs.get("method", "get").lower()
            # Inputting Name and Type
            inputs = []
            for input_tag in form.find_all("input"):
                input_type = input_tag.attrs.get("type", "text")
                input_name = input_tag.attrs.get("name")
                input_value = input_tag.attrs.get("value", "")
                inputs.append(
                    {"type": input_type, "name": input_name, "value": input_value})
            # Saving details into Prospective Variables
            details["action"] = action
            details["method"] = method
            details["inputs"] = inputs
            return details

        # Set the responses
        def is_vulnerable(response):
            errors = {
                # MySQL
                "you have an error in your sql syntax;",
                "warning: mysql",
                # SQL Server
                "unclosed quotation mark after the character string",
                # Oracle
                "quoted string not properly terminated",
            }
            for error in errors:
                # If error is found, then
                if error in response.content.decode().lower():
                    return True
            # If error is not found, then
            return False

        # scan the URL
        def scan_sql(url):

            print("____________________________________________________")
            print("                       Report                       ")
            print("____________________________________________________")

            print("The url is:", url)
            print("\nscanning...")
            print("            .....")
            print("                   searching....")
            print("                                 Connecting!!!!!\n")
            for c in "\"'":
                # Adding quotes in URL
                new_url = f"{url}{c}"
                print("[!] Trying", new_url)
                # HTTP request creation
                res = s.get(new_url)
                if is_vulnerable(res):
                    # SQL Injection detected
                    print("[+] SQL Injection vulnerability detected, link:", new_url)
                    print("\n\n____________________________________________________")
                    print("                       Mitigation                     ")
                    print("____________________________________________________")
                    print("You Must check the following:")
                    print("1. Input validation")
                    print("2. Parametrized queries")
                    print("3. Stored procedures")
                    print("4. Escaping")
                    print("5. Avoiding administrative privileges")
                    print("6. Web application firewall")

                    print("____________________________________________________")
                    now = datetime.now()
                    # dd/mm/YY H:M:S
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("\nScanned at =", dt_string)
                    end = time.time()
                    print(f"Time taken {end - start}")
                    return

            # SQL IInjection Test
            forms = get_forms(url)
            print(f"[+] Detected {len(forms)} forms on {url}.")
            for form in forms:
                form_details = get_details(form)
                for c in "\"'":
                    # Submission of data
                    data = {}
                    for input_tag in form_details["inputs"]:
                        if input_tag["type"] == "hidden" or input_tag["value"]:
                            # any input form = hidden or = value
                            try:
                                data[input_tag["name"]] = input_tag["value"] + c
                            except:
                                pass
                        elif input_tag["type"] != "submit":
                            # Search some other tags
                            data[input_tag["name"]] = f"test{c}"
                    # Join URL + details
                    url = urljoin(url, form_details["action"])
                    if form_details["method"] == "post":
                        res = s.post(url, data=data)
                    elif form_details["method"] == "get":
                        res = s.get(url, params=data)
                    # If vulnerability exist
                    if is_vulnerable(res):
                        print(
                            "[+] SQL Injection vulnerability detected, link:", url)
                        print("[+] Form:")
                        pprint(form_details)
                        break

        if __name__ == "__main__":
            print("Enter URL to scan:")  # input URL to scan
            url = input()
            scan_sql(url)
            import sys
            # x = open("SQL_Report.txt", 'w')
            # sys.stdout = x
            # scan_sql(url)
            # x.close()
            import os
            os.system("PAUSE")

    # Xxs Check
    elif choice == '2':
        import requests                  # Importing Libraries
        from bs4 import BeautifulSoup as bs
        from urllib.parse import urljoin
        from pprint import pprint
        from datetime import datetime
        import time

        start = time.time()

        # Captures all the HTML Sources
        def get_forms(url):
            soup = bs(requests.get(url).content, "html.parser")
            return soup.find_all("form")

        # Get all the information
        def get_details(form):
            details = {}
            # Start the action
            action = form.attrs.get("action").lower()
            # POST & GET Method
            method = form.attrs.get("method", "get").lower()
            # Inputting Name and Type
            inputs = []
            for input_tag in form.find_all("input"):
                input_type = input_tag.attrs.get("type", "text")
                input_name = input_tag.attrs.get("name")
                inputs.append({"type": input_type, "name": input_name})
            # Saving details into Prospective Variables
            details["action"] = action
            details["method"] = method
            details["inputs"] = inputs
            return details

        # Get all the information
        def submit_form(form_details, url, value):
            # Url + Details
            target_url = urljoin(url, form_details["action"])
            # get the inputs
            inputs = form_details["inputs"]
            data = {}
            for input in inputs:
                # change text and search = `value`
                if input["type"] == "text" or input["type"] == "search":
                    input["value"] = value
                input_name = input.get("name")
                input_value = input.get("value")
                if input_name and input_value:
                    # if input name and value exist, add it in form
                    data[input_name] = input_value

            if form_details["method"] == "post":
                return requests.post(target_url, data=data)
            else:
                # Capture Requests
                return requests.get(target_url, params=data)

        # scan the Url
        def scan_xss(url):
            print("____________________________________________________")
            print("                       Report                       ")
            print("____________________________________________________")

            print("The url is:", url)
            print("\nscanning...")
            print("            .....")
            print("                   searching....")
            print("                                 Connecting!!!!!\n")

            forms = get_forms(url)
            print(f"[+] Detected {len(forms)} forms on {url}.")
            js_script = "<Script>alert('hi')</scripT>"
            # returning value
            is_vulnerable = False
            # for All forms
            for form in forms:
                form_details = get_details(form)
                content = submit_form(
                    form_details, url, js_script).content.decode()
                if js_script in content:
                    print(f"[+] XSS Detected on {url}")
                    print(f"[*] Form details:")
                    pprint(form_details)
                    is_vulnerable = True
                    print("\n\n____________________________________________________")
                    print("                       RISKS                            ")
                    print("________________________________________________________")
                    print("1. Impersonate or masquerade as the victim user.")
                    print("2. Carry out any action that the user is able to perform")
                    print("3. Capture the user's login credentials")
                    print("4. Perform virtual defacement of the web site")
                    print("5. Inject trojan functionality into the web site")

                    print("____________________________________________________")
                    now = datetime.now()
                    # dd/mm/YY H:M:S
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("\nScanned at =", dt_string)
                    end = time.time()
                    print(f"Time taken {end - start}")
            return is_vulnerable

        if __name__ == "__main__":
            print("Enter URL to scan:")
            url = input()
            print(bool(scan_xss(url)))
            import sys
            x = open("XSS_Report.txt", 'w')
            sys.stdout = x
            print(bool(scan_xss(url)))
            x.close()  # File Close
            import os
            os.system("PAUSE")
