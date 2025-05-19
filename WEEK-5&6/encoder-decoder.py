import tkinter as tk
from tkinter import messagebox # Though not explicitly used in the functions from the image, it's good practice to import if needed
from tkinter import filedialog
import random
import string
import os

# --- Global variables for cipher maps ---
cipher_map = {}
reverse_map = {}

# 2. Generate a Randomized Alphabet Mapping
def generate_cipher():
    global cipher_map, reverse_map # To modify the global maps
    original_alphabet = list(string.ascii_uppercase)
    shuffled_alphabet = original_alphabet.copy()
    random.shuffle(shuffled_alphabet)

    # Create two dictionaries:
    # 1. Cipher Map: Maps normal letters to encoded letters
    # 2. Reverse Map: Maps encoded letters back to normal letters
    cipher_map = dict(zip(original_alphabet, shuffled_alphabet))
    reverse_map = dict(zip(shuffled_alphabet, original_alphabet))
    # The function in the doc returns them, but the call in step 5 assigns them globally directly.
    # To match step 5, we modify globals. If we were to return, step 5 would be:
    # cipher_map, reverse_map = generate_cipher()

# 3. Define Encoding & Decoding Functions
# a. Encoding Function
def encode_message():
    global cipher_map # Use the globally defined cipher_map
    text = entry_text_var.get().upper() # Fetch user input from the GUI, convert to uppercase
    # Replace each letter with its encoded equivalent using cipher_map.
    # It remains unchanged if a character is not found in the cipher map (e.g., numbers, spaces, punctuation).
    encoded_list = [cipher_map.get(char, char) for char in text]
    encoded_text = "".join(encoded_list)
    set_output_text(encoded_text) # Set the output in the GUI

# b. Decoding Function
def decode_message():
    global reverse_map # Use the globally defined reverse_map
    text = entry_text_var.get().upper() # Fetch user input from the GUI, convert to uppercase
    # Uses reverse_map to restore the original message.
    # Follows the same logic as encoding but in reverse.
    decoded_list = [reverse_map.get(char, char) for char in text]
    decoded_text = "".join(decoded_list)
    set_output_text(decoded_text) # Set the output in the GUI

# --- File Upload Functionality ---
def upload_file_and_process(mode):
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")],
        title="Select a .txt file to process"
    )
    if not file_path:
        return  # User cancelled
    try:
        file_size = os.path.getsize(file_path)
        if file_size > 1.5 * 1024 * 1024:  # 1.5MB in bytes
            messagebox.showerror("File Too Large", "File exceeds 1.5MB limit.")
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.upper()
        if mode == 'encode':
            result = ''.join(cipher_map.get(char, char) for char in content)
        else:
            result = ''.join(reverse_map.get(char, char) for char in content)
        set_output_text(result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")

# --- Main Application Setup ---

# 4. Set Up the GUI using Tkinter
# a. tk.Tk() creates the main window for our GUI.
root = tk.Tk()
# b. title() sets the window title.
root.title("Secret Message Encoder")
# c. geometry() defines the size of the application window.
root.geometry("400x300") # As per document

# 5. Generate Cipher Mapping
# a. Calls generate_cipher() to create a new cipher each time the program runs.
generate_cipher() # This will populate the global cipher_map and reverse_map

# 6. Create Input Field for Message
# a. Creates a label and text entry box for the user to input their message.
tk.Label(root, text="Enter Message:").pack(pady=5)
entry_text_var = tk.StringVar() # For the Entry widget
entry_box = tk.Entry(root, textvariable=entry_text_var, width=30, font=("Arial", 12))
entry_box.pack(pady=5)

# 7. Add Buttons for Encoding & Decoding
# a. The "Encode" button calls encode_message().
encode_button = tk.Button(root, text="Encode", command=encode_message, width=10)
encode_button.pack(pady=5)

# b. The "Decode" button calls decode_message().
decode_button = tk.Button(root, text="Decode", command=decode_message, width=10)
decode_button.pack(pady=5)

# c. Add Upload File buttons for encoding and decoding
upload_encode_btn = tk.Button(root, text="Upload & Encode File", command=lambda: upload_file_and_process('encode'), width=20)
upload_encode_btn.pack(pady=2)
upload_decode_btn = tk.Button(root, text="Upload & Decode File", command=lambda: upload_file_and_process('decode'), width=20)
upload_decode_btn.pack(pady=2)

# 8. Display the Output
# a. A label and output field are created to display the encoded/decoded message.
tk.Label(root, text="Output:").pack(pady=5)

# Create a frame to hold the Text widget and scrollbar
txt_frame = tk.Frame(root)
txt_frame.pack(pady=5, fill='both', expand=True)

output_text = tk.Text(txt_frame, wrap='word', height=8, width=40, font=("Arial", 12), fg="blue")
output_text.pack(side='left', fill='both', expand=True)

scrollbar = tk.Scrollbar(txt_frame, command=output_text.yview)
scrollbar.pack(side='right', fill='y')
output_text.config(yscrollcommand=scrollbar.set)

def set_output_text(text):
    output_text.config(state='normal')
    output_text.delete(1.0, 'end')
    output_text.insert('end', text)
    output_text.config(state='disabled')

# 9. Run the GUI
# a. root.mainloop() keeps the GUI running until the user closes the window.
if __name__ == "__main__":
    root.mainloop()
