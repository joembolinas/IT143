import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, Frame, END, RIGHT, Y, BOTH, messagebox, StringVar, OptionMenu
from urllib.parse import urljoin

# --- Extraction Modes ---
EXTRACTION_MODES = [
    "Title & Links",
    "All Text",
    "Raw HTML"
]

# 1. Function to parse the website
def parse_website():
    url = url_entry.get()
    mode = extraction_mode.get()
    if not url:
        messagebox.showerror("Error", "URL field cannot be empty.")
        return
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        content_type = response.headers.get('Content-Type', '')
        if 'html' not in content_type:
            result_box.delete(1.0, END)
            result_box.insert(END, f"The URL did not return HTML content. Content-Type: {content_type}\n")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        result_box.delete(1.0, END)
        if mode == "Title & Links":
            title = soup.title.string if soup.title else "No title found"
            links = soup.find_all('a', href=True)
            result_box.insert(END, f"Title of the Website:\n{title}\n\n")
            result_box.insert(END, "Hyperlinks Found:\n")
            if links:
                for i, link_tag in enumerate(links, 1):
                    href = link_tag['href']
                    if not href.startswith(('http://', 'https://')) and not href.startswith('#'):
                        href = urljoin(url, href)
                    result_box.insert(END, f"{i}. {href}\n")
            else:
                result_box.insert(END, "No hyperlinks found.\n")
        elif mode == "All Text":
            text = soup.get_text(separator='\n', strip=True)
            result_box.insert(END, text if text else "No text content found.")
        elif mode == "Raw HTML":
            result_box.insert(END, response.text)
        else:
            result_box.insert(END, "Unknown extraction mode selected.")
    except requests.exceptions.Timeout:
        result_box.delete(1.0, END)
        result_box.insert(END, f"Error: The request timed out while trying to fetch {url}\n")
    except requests.exceptions.HTTPError as http_err:
        result_box.delete(1.0, END)
        result_box.insert(END, f"HTTP error occurred: {http_err}\nStatus Code: {response.status_code if 'response' in locals() else 'N/A'}\n")
    except requests.exceptions.RequestException as e:
        result_box.delete(1.0, END)
        result_box.insert(END, f"Error fetching URL: {str(e)}\n")
    except Exception as e:
        result_box.delete(1.0, END)
        result_box.insert(END, f"An error occurred during parsing: {str(e)}\n")

# 2. Set Up the Main Tkinter GUI
root = Tk()
root.title("Web Parser")
root.geometry("700x500")

Label(root, text="Enter URL:", font=("Arial", 12)).pack(pady=5)
url_entry = Entry(root, width=70, font=("Arial", 12))
url_entry.pack(pady=5, padx=10)
url_entry.insert(0, "https://about.google/")

Label(root, text="Extraction Mode:", font=("Arial", 12)).pack(pady=2)
extraction_mode = StringVar(root)
extraction_mode.set(EXTRACTION_MODES[0])
OptionMenu(root, extraction_mode, *EXTRACTION_MODES).pack(pady=2)

Button(root, text="Parse Website", command=parse_website,
       font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

results_frame = Frame(root)
results_frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

scrollbar = Scrollbar(results_frame, orient='vertical')
result_box = Text(results_frame, wrap='word', yscrollcommand=scrollbar.set, font=("Arial", 10), height=18)

scrollbar.config(command=result_box.yview)
scrollbar.pack(side=RIGHT, fill=Y)
result_box.pack(side=RIGHT, fill=BOTH, expand=True)

root.mainloop()
