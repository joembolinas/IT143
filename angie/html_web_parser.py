import tkinter as tk
from tkinter import scrolledtext, messagebox
from bs4 import BeautifulSoup

# --- Define the extract_content Function ---
def extract_content():
    html_content = html_text.get("1.0", tk.END)
    if not html_content.strip():
        messagebox.showerror("Error", "Please enter some HTML content.")
        return
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        paragraph_text = "\n\n".join(paragraphs) if paragraphs else "No paragraphs found."
        links = [link["href"] for link in soup.find_all('a', href=True)]
        link_text = "\n".join(links) if links else "No links found."
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Title:\n{title}\n\n")
        result_text.insert(tk.END, f"Paragraphs:\n{paragraph_text}\n\n")
        result_text.insert(tk.END, f"Links:\n{link_text}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract content:\n{e}")

# --- Add UI Elements ---
app = tk.Tk()
app.title("HTML Content Extractor")
app.geometry("800x600")

html_label = tk.Label(app, text="Enter HTML Content:", font=("Arial", 12))
html_label.pack(pady=5)

html_text = scrolledtext.ScrolledText(app, font=("Arial", 12), wrap=tk.WORD, width=80, height=10)
html_text.pack(pady=5)

extract_button = tk.Button(app, text="Extract Content", font=("Arial", 12), command=extract_content)
extract_button.pack(pady=10)

result_text = scrolledtext.ScrolledText(app, font=("Arial", 12), wrap=tk.WORD, width=80, height=25)
result_text.pack(pady=10)

app.mainloop()
