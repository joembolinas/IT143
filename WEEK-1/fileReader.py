import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox


def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                text_area.config(state=tk.NORMAL)
                text_area.delete('1.0', tk.END)
                text_area.insert(tk.END, content)
                text_area.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")


def search_keyword():
    keyword = keyword_entry.get()
    if keyword:
        text_area.tag_remove("highlight", '1.0', tk.END)
        content = text_area.get('1.0', tk.END)
        start_index = '1.0'
        while True:
            start_index = text_area.search(keyword, start_index, stopindex=tk.END, nocase=True)
            if not start_index:
                break
            end_index = f"{start_index}+{len(keyword)}c"
            text_area.tag_add("highlight", start_index, end_index)
            start_index = end_index
        text_area.tag_config("highlight", background="yellow")


window = tk.Tk()
window.title("File Reader and Keyword Search")


open_button = tk.Button(window, text="Open File", command=open_file)
open_button.pack(pady=10)


text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=20)
text_area.pack(padx=10, pady=10)
text_area.config(state=tk.DISABLED)


keyword_label = tk.Label(window, text="Enter Keyword:")
keyword_label.pack(pady=5)


keyword_entry = tk.Entry(window)
keyword_entry.pack(padx=10, pady=5)


search_button = tk.Button(window, text="Search", command=search_keyword)
search_button.pack(pady=10)


window.mainloop()
