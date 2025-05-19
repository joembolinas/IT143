import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import re
import pyperclip # For copying extracted results

# Create main application window
root = tk.Tk()
root.title("Regex Information Extractor")
root.geometry("700x500") # 700 pixels width x 500 pixels height

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[
        ("Text files", "*.txt"),
        ("JSON files", "*.json"),
    ])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text_content = file.read()
            text_area.delete("1.0", tk.END) # Clear previous content
            text_area.insert(tk.END, text_content)
            label_status.config(text=f"Loaded: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
            label_status.config(text="Error loading file")
            
            
def extract_info():
    text_content = text_area.get("1.0", tk.END)
    selected_option = extract_option.get()

    regex_patterns = {
        "Email Addresses": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "Phone Numbers": r"\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        "Dates": r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b", # Matches MM/DD/YYYY, DD-MM-YYYY etc.
        "flagged": r"\b(?:flagged|flag)\b",
        "URLs": r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    }

    if selected_option == "Messages with flagged True (JSON)":
        import json
        try:
            data = json.loads(text_content)
            messages = []
            if isinstance(data, list):
                messages = [item["message"] for item in data if item.get("flagged") is True and "message" in item]
            elif isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, list):
                        messages.extend([item["message"] for item in v if isinstance(item, dict) and item.get("flagged") is True and "message" in item])
        except Exception as e:
            result_area.delete("1.0", tk.END)
            result_area.insert(tk.END, f"Error parsing JSON: {e}")
            return
        result_area.delete("1.0", tk.END)
        if messages:
            result_area.insert(tk.END, "\n".join(messages))
        else:
            result_area.insert(tk.END, "No flagged messages found.")
        return

    if selected_option == "Decoded FLAGs from flagged JSON (base64)":
        import json, base64, re
        try:
            data = json.loads(text_content)
            flags = []
            if isinstance(data, list):
                entries = data
            elif isinstance(data, dict):
                entries = []
                for v in data.values():
                    if isinstance(v, list):
                        entries.extend(v)
            else:
                entries = []
            for entry in entries:
                if entry.get("flagged") and "message" in entry:
                    encoded_msg = entry["message"]
                    try:
                        decoded_bytes = base64.b64decode(encoded_msg)
                        decoded_msg = decoded_bytes.decode('utf-8')
                        match = re.search(r'FLAG\{.*?\}', decoded_msg)
                        if match:
                            flags.append(match.group())
                    except Exception as e:
                        continue
        except Exception as e:
            result_area.delete("1.0", tk.END)
            result_area.insert(tk.END, f"Error parsing/decoding JSON: {e}")
            return
        result_area.delete("1.0", tk.END)
        if flags:
            result_area.insert(tk.END, "\n".join(flags))
        else:
            result_area.insert(tk.END, "No decoded FLAGs found.")
        return

    pattern = regex_patterns.get(selected_option)
    if not pattern:
        messagebox.showerror("Error", "Invalid selection.")
        return

    matches = re.findall(pattern, text_content)

    result_area.delete("1.0", tk.END) # Clear previous results
    if matches:
        result_area.insert(tk.END, "\n".join(matches))
    else:
        result_area.insert(tk.END, "No matches found.")
        
        
def copy_results():
    extracted_text = result_area.get("1.0", tk.END).strip()
    if extracted_text and extracted_text != "No matches found.":
        pyperclip.copy(extracted_text)
        messagebox.showinfo("Copied", "Extracted information copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No extracted data to copy.")
        

btn_open = tk.Button(root, text="Open File", command=open_file)
btn_open.pack(pady=5)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=12)
text_area.pack(pady=5)

if root.winfo_exists():  # Check if the root window is still active
	dropdown_label = tk.Label(root, text="Select Data Type to Extract:")
	dropdown_label.pack()

	extract_option = tk.StringVar()
	# Set default value
	extract_option.set("Email Addresses")
	options = [
        "Email Addresses",
        "Phone Numbers",
        "Dates",
        "flagged",
        "URLs",
        "Messages with flagged True (JSON)",
        "Decoded FLAGs from flagged JSON (base64)"
    ]
	dropdown_menu = ttk.Combobox(root, textvariable=extract_option, values=options, state="readonly")
	dropdown_menu.pack(pady=5)
else:
	print("The application window has been closed. Cannot create widgets.")
 
 
btn_extract = tk.Button(root, text="Extract", command=extract_info)
btn_extract.pack(pady=5)

result_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=8)
result_area.pack(pady=5)

btn_copy = tk.Button(root, text="Copy Results", command=copy_results)
btn_copy.pack(pady=5)

label_status = tk.Label(root, text="No file loaded", fg="blue")
label_status.pack(pady=5)

root.mainloop()