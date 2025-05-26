# Practice Activity No. 1: Secret Message Encoder

Ever wanted to create your secret code? In this activity, you'll build a Python GUI application to encode messages using a randomly shuffled alphabet! This means every letter in your message will replace another one, creating a hidden code only you can decode.

By completing this activity, you'll practice working with:

* Graphical User Interfaces (GUIs) using Tkinter (or another library of your choice).
* String manipulation to replace letters with their shuffled equivalents.
* Randomization to create a unique alphabet mapping for encryption.

Follow the instructions below to complete this assignment:

1. Open your Python IDE. Import the necessary libraries (tkinter, random, and string).
2. Write a GUI-based Python program to scramble user string input and display the results.

**Sample Output:**

**1. Import Required Libraries**

```
App.py •
C: > Users > MeLbe > OneDrive > Desktop > App.py > generate_cipher
1 import tkinter as tk
2 from tkinter import messagebox
3 import random
4 import string
5
```

a.  `tkinter` is for creating a user-friendly Graphical User Interface (GUI).
b.  The `random` module is used to shuffle the alphabet for encryption.
c.  `string.ascii_uppercase` provides all uppercase letters (A-Z) to create the cipher.

**2. Generate a Randomized Alphabet Mapping**

```python
6 def generate_cipher():
7     original_alphabet = list(string.ascii_uppercase)
8     shuffled_alphabet = original_alphabet.copy()
9     random.shuffle(shuffled_alphabet)
10
11    # Create two dictionaries:
12    # 1. Cipher Map: Maps normal letters to encoded letters
13    # 2. Reverse Map: Maps encoded letters back to normal letters
14    return dict(zip(original_alphabet, shuffled_alphabet)), dict(zip(shuffled_alphabet, original_alphabet))
15
```

a.  A list of uppercase letters (A-Z) is created.
b.  A shuffled copy is generated to serve as the encoded alphabet.
c.  Two dictionaries (lookup tables) are created:
d.  `Cipher_map` maps original letters to their encoded counterparts.
e.  `reverse_map` maps encoded letters back to their original form.

**3. Define Encoding & Decoding Functions**

**a. Encoding Function**

```python
16
17 def encode_message():
18     global cipher_map
19     text = entry_text.get().upper()
20     encoded_text = ''.join(cipher_map.get(char, char) for char in text)
21     output_text.set(encoded_text)
22
```

* Fetch user input from the GUI.
* Convert it to uppercase to ensure consistency.
* Replace each letter with its encoded equivalent using `cipher_map`.
* It remains unchanged if a character is not found in the cipher map (e.g., numbers, spaces, punctuation).

**b. Decoding Function**

```python
22
23 def decode_message():
24     global reverse_map
25     text = entry_text.get().upper()
26     decoded_text = ''.join(reverse_map.get(char, char) for char in text)
27     output_text.set(decoded_text)
28
```

* Uses `reverse_map` to restore the original message.
* Follows the same logic as encoding but in reverse.

**4. Set Up the GUI using Tkinter**

```python
28
29 # Initialize main window
30 root = tk.Tk()
31 root.title("Secret Message Encoder")
32 root.geometry("400x300")
33
```

a.  `tk.Tk()` creates the main window for our GUI.
b.  `title()` sets the window title.
c.  `geometry()` defines the size of the application window.

**5. Generate Cipher Mapping**

```python
33
34 # Generate new cipher mapping
35 cipher_map, reverse_map = generate_cipher()
36
```

a.  Calls `generate_cipher()` to create a new cipher each time the program runs.

**6. Create Input Field for Message**

```python
36
37 # Input Label & Entry Box
38 tk.Label(root, text="Enter Message:").pack(pady=5)
39 entry_text = tk.StringVar()
40 entry_box = tk.Entry(root, textvariable=entry_text, width=30)
41 entry_box.pack(pady=5)
42
```

a.  Creates a label and text entry box for the user to input their message.

**7. Add Buttons for Encoding & Decoding**

```python
42
43 # Encode Button
44 tk.Button(root, text="Encode", command=encode_message).pack(pady=5)
45
46 # Decode Button
47 tk.Button(root, text="Decode", command=decode_message).pack(pady=5)
48
```

a.  The "Encode" button calls `encode_message()`.
b.  The "Decode" button calls `decode_message()`.

**8. Display the Output**

```python
48
49 # Output Display
50 output_text = tk.StringVar()
51 tk.Label(root, text="Output:").pack(pady=5)
52 output_label = tk.Label(root, textvariable=output_text, fg="blue", font=("Arial", 12, "bold"))
53 output_label.pack(pady=5)
54
```

a.  A label and output field are created to display the encoded/decoded message.

**9. Run the GUI**

```python
54
55 # Run the GUI
56 root.mainloop()
57
```

a.  `root.mainloop()` keeps the GUI running until the user closes the window.

**10. Test the Application**
Test the application by running the code in your IDE and enter your input.

---

**Sample GUI Application Screenshot:**

The screenshot on page 4 shows a GUI window titled "Secret Message Encoder".
It contains:

* A label "Enter Message:".
* A text input field where "Hello MMDC" is typed.
* An "Encode" button.
* A "Decode" button.
* A label "Output:".
* An output display area showing "BDFFP NNAG!" in blue, bold text.
