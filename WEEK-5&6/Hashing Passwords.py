import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import hashlib
import os

# 2. Define a Function to Hash a Password
def hash_password(password):
    """
    Hashes a password using SHA-256.
    a. The function encodes the password into bytes before applying SHA-256 hashing.
    b. hexdigest() converts the hash into a readable hexadecimal string.
    """
    return hashlib.sha256(password.encode()).hexdigest()

# 3. Define a Function to Compare Hashes
def verify_password():
    """
    a. The function retrieves user input from the GUI.
    b. It hashes the user-entered password using hash_password().
    c. Compares the hashed input with a pre-stored hash (e.g., hash of "password").
    d. If the hashes match, it displays a success message; otherwise, it shows an error message.
    """
    user_input = entry_text_var.get() # Get input from the user
    user_hash = hash_password(user_input) # Hash user input

    # Pre-stored hash of "password"
    stored_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd485fa0f7f0a89b6b5"

    if user_hash == stored_hash:
        messagebox.showinfo("Verification", "Password Matched!")
    else:
        messagebox.showerror("Verification", "Incorrect Password")

# 4. Create the GUI using Tkinter
# a. Creates the main window.
# b. Sets the title and size.
root = tk.Tk()
root.title("SHA-256 Password Hasher")
root.geometry("400x300") # Adjusted height slightly for better component fit

# 5. Add Input Field for Password
tk.Label(root, text="Enter Password:").pack(pady=5)
entry_text_var = tk.StringVar() # To hold the text from the entry widget
# a. Users enter their password in this input field.
# b. show="*" ensures that the password is hidden for security.
entry_box = tk.Entry(root, textvariable=entry_text_var, show="*", width=30)
entry_box.pack(pady=5)

# 6. Add Buttons for Hashing & Verification
# a. "Hash Password" button: Displays the SHA-256 hash of the input.
hash_button = tk.Button(root, text="Hash Password",
                        command=lambda: set_output_text(hash_password(entry_text_var.get())))
hash_button.pack(pady=5)

# b. "Verify Password" button: Checks if the input matches the pre-stored hash.
verify_button = tk.Button(root, text="Verify Password", command=verify_password)
verify_button.pack(pady=5)

# --- Scrollable Output Text Widget ---
output_frame = tk.Frame(root)
output_frame.pack(pady=5, fill='both', expand=True)
output_text = tk.Text(output_frame, wrap='word', height=8, width=40, font=("Arial", 10, "bold"), fg="blue")
output_text.pack(side='left', fill='both', expand=True)
scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side='right', fill='y')
output_text.config(yscrollcommand=scrollbar.set, state='disabled')

def set_output_text(text):
    output_text.config(state='normal')
    output_text.delete(1.0, 'end')
    output_text.insert('end', text)
    output_text.config(state='disabled')

# --- File Upload and Hashing Functionality ---
def upload_and_hash_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")],
        title="Select a .txt file to hash"
    )
    if not file_path:
        return
    try:
        file_size = os.path.getsize(file_path)
        if file_size > 3 * 1024 * 1024:  # 3MB in bytes
            messagebox.showerror("File Too Large", "File exceeds 3MB limit.")
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        hashes = [hash_password(line.rstrip('\n')) for line in lines]
        set_output_text('\n'.join(hashes))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")

# Add Upload & Hash File button
upload_btn = tk.Button(root, text="Upload & Hash File", command=upload_and_hash_file, width=20)
upload_btn.pack(pady=2)

# 8. Run the GUI
# a. Keeps the GUI active until the user closes the window.
if __name__ == "__main__":
    root.mainloop()
