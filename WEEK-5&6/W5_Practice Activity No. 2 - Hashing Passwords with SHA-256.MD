# Practice Activity No. 2: Hashing Passwords with SHA-256

Passwords are critical to digital security, but storing them in plain text is a major security risk! Instead, secure systems hash passwords before storing them, making it difficult for attackers to retrieve the original password.

In this activity, you'll build a GUI-based Python application that:

* Takes a user's password as input.
* Hashes it using the SHA-256 algorithm.
* Compares the hashed password with a stored hash to verify if they match.

To carry out this assignment, follow the instructions below:

1. Open your Python IDE and prepare the required libraries.
2. Write a Python script that:
   a.  Takes a user's password as input.
   b.  Hashes it using SHA-256.
   c.  Compares the hash with a stored hash.

**Sample Output:**

**1. Import Required Libraries**

```
App.py •
C: > Users > MeLbe > OneDrive > Desktop > App.py > verify_password
1 import tkinter as tk # GUI creation
2 import hashlib # SHA-256 hashing
3 from tkinter import messagebox # Pop-up notifications
4
```

a.  `tkinter` is used to create a simple user interface.
b.  `hashlib` provides SHA-256 hashing functions.
c.  `messagebox` is used to show alerts and messages in the GUI.

**2. Define a Function to Hash a Password**

```python
4
5 def hash_password(password):
6     return hashlib.sha256(password.encode()).hexdigest()
7
```

a.  The function encodes the password into bytes before applying SHA-256 hashing.
b.  `hexdigest()` converts the hash into a readable hexadecimal string.

**3. Define a Function to Compare Hashes**

```python
7
8 def verify_password():
9     user_input = entry_text.get() # Get input from the user
10    user_hash = hash_password(user_input) # Hash user input
11    stored_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd485fa0f7f0a89b6b5" # Pre-stored hash of "password"
12
13    if user_hash == stored_hash:
14        messagebox.showinfo("Verification", "Password Matched!")
15    else:
16        messagebox.showerror("Verification", "Incorrect Password")
17
```

a.  The function retrieves user input from the GUI.
b.  It hashes the user-entered password using `hash_password()`.
c.  Compares the hashed input with a pre-stored hash (e.g., hash of "password").
d.  If the hashes match, it displays a success message, otherwise, it shows an error message.

**4. Create the GUI using Tkinter**

```python
17
18 # Initialize GUI window
19 root = tk.Tk()
20 root.title("SHA-256 Password Hasher")
21 root.geometry("400x250")
22
```

a.  Creates the main window.
b.  Sets the title and size.

**5. Add Input Field for Password**

```python
22
23 # Input Label & Entry Box
24 tk.Label(root, text="Enter Password:").pack(pady=5)
25 entry_text = tk.StringVar()
26 entry_box = tk.Entry(root, textvariable=entry_text, show="*", width=30) # Mask input
27 entry_box.pack(pady=5)
28
```

a.  Users enter their password in this input field.
b.  `show="*"` ensures that the password is hidden for security.

**6. Add Buttons for Hashing & Verification**

```python
28
29 # Hashing Button
30 tk.Button(root, text="Hash Password", command=lambda: output_text.set(hash_password(entry_text.get()))).pack(pady=5)
31
32 # Verify Button
33 tk.Button(root, text="Verify Password", command=verify_password).pack(pady=5)
34
```

a.  "Hash Password" button: Displays the SHA-256 hash of the input.
b.  "Verify Password" button: Checks if the input matches the pre-stored hash.

**7. Display Output for Hashed Password**

```python
34
35 # Output Display
36 output_text = tk.StringVar()
37 tk.Label(root, text="Hashed Password:").pack(pady=5)
38 output_label = tk.Label(root, textvariable=output_text, fg="blue", font=("Arial", 10, "bold"), wraplength=350)
39 output_label.pack(pady=5)
40
```

a.  Displays the hashed password output.
b.  Text wraps to prevent long hash values from breaking the layout.

**8. Run the GUI**

```python
40
41 # Run the application
42 root.mainloop()
43
```

a.  Keeps the GUI active until the user closes the window.

**9. Test the Application** - run the code in your IDE and test its features with your input:

---

**Sample GUI Application Screenshot:**

The screenshot on page 3 shows a GUI window titled "SHA-256 Password Hasher".
It contains:

* A label "Enter Password:".
* A text input field showing asterisks (`*****`) for hidden input.
* A "Hash Password" button.
* A "Verify Password" button.
* A label "Hashed Password:".
* An output display area showing a long hexadecimal string (the hashed password) in blue, bold text. The example hash shown is: `dcc3a22a248e8c849fc5e135663564f8994402b29a807320360043fb14a5b411`
