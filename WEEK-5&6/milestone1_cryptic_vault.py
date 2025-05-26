import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import os

cracked_dict = {}  # Stores hash:password pairs after cracking

def load_lines(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip()]

def crack_hashes(hash_file, wordlist_file):
    hashes = set(load_lines(hash_file))
    wordlist = load_lines(wordlist_file)
    cracked = []
    for password in wordlist:
        hash_candidate = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if hash_candidate in hashes:
            cracked.append((hash_candidate, password))
    return cracked

def select_file(entry_widget, title):
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")],
        title=title
    )
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

def run_crack():
    global cracked_dict
    hash_file = hash_file_entry.get()
    wordlist_file = wordlist_file_entry.get()
    hash_output.config(state='normal')
    pass_output.config(state='normal')
    hash_output.delete(1.0, tk.END)
    pass_output.delete(1.0, tk.END)
    cracked_dict = {}
    if not os.path.isfile(hash_file) or not os.path.isfile(wordlist_file):
        hash_output.insert(tk.END, "Please select valid files.\n")
        pass_output.insert(tk.END, "Please select valid files.\n")
        hash_output.config(state='disabled')
        pass_output.config(state='disabled')
        return
    cracked = crack_hashes(hash_file, wordlist_file)
    if not cracked:
        hash_output.insert(tk.END, "No hashes were cracked.\n")
        pass_output.insert(tk.END, "No hashes were cracked.\n")
    else:
        for h, p in cracked:
            hash_output.insert(tk.END, f"{h}\n")
            pass_output.insert(tk.END, f"{p}\n")
            cracked_dict[h] = p
    hash_output.config(state='disabled')
    pass_output.config(state='disabled')

def decode_encode():
    hash_val = hash_output.get("1.0", tk.END).strip()
    pass_val = pass_output.get("1.0", tk.END).strip()
    hash_output.config(state='normal')
    pass_output.config(state='normal')
    # If hash is entered, decode to password
    if hash_val and not pass_val:
        password = cracked_dict.get(hash_val)
        if password:
            pass_output.delete(1.0, tk.END)
            pass_output.insert(tk.END, password)
        else:
            pass_output.delete(1.0, tk.END)
            pass_output.insert(tk.END, "Not found in cracked hashes.")
    # If password is entered, encode to hash
    elif pass_val and not hash_val:
        hash_candidate = hashlib.sha256(pass_val.encode('utf-8')).hexdigest()
        hash_output.delete(1.0, tk.END)
        hash_output.insert(tk.END, hash_candidate)
    # If both are empty or both have values, do nothing
    hash_output.config(state='disabled')
    pass_output.config(state='disabled')

# --- GUI Setup ---
root = tk.Tk()
root.title("CTF Cryptic Vault Cracker")
root.geometry("700x400")

tk.Label(root, text="Hashed Passwords File:").pack(pady=(10,0))
hash_file_entry = tk.Entry(root, width=60)
hash_file_entry.pack(padx=10)
tk.Button(root, text="Browse", command=lambda: select_file(hash_file_entry, "Select hashed_passwords.txt")).pack(pady=2)

tk.Label(root, text="Wordlist File:").pack(pady=(10,0))
wordlist_file_entry = tk.Entry(root, width=60)
wordlist_file_entry.pack(padx=10)
tk.Button(root, text="Browse", command=lambda: select_file(wordlist_file_entry, "Select wordlist.txt")).pack(pady=2)

tk.Button(root, text="Crack Hashes", command=run_crack, bg="blue", fg="white", font=("Arial", 12)).pack(pady=10)

# Output boxes side by side
output_frame = tk.Frame(root)
output_frame.pack(fill='both', expand=True, padx=10, pady=5)

hash_label = tk.Label(output_frame, text="Hash", font=("Arial", 10, "bold"))
hash_label.pack(side='left', padx=(0,5))
pass_label = tk.Label(output_frame, text="Password", font=("Arial", 10, "bold"))
pass_label.pack(side='right', padx=(5,0))

hash_output = tk.Text(output_frame, wrap='word', font=("Arial", 10), width=64, height=10, state='disabled')
hash_output.pack(side='left', fill='both', expand=True, padx=(0,5))
pass_output = tk.Text(output_frame, wrap='word', font=("Arial", 10), width=32, height=10, state='disabled')
pass_output.pack(side='right', fill='both', expand=True, padx=(5,0))

tk.Button(root, text="Decode/Encode", command=decode_encode, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

if __name__ == "__main__":
    root.mainloop()