import tkinter as tk
# The random library is no longer needed.
# import random

# The function is now clean and predictable.
def do_something(x, y):
    return x * y

# The main logic is now clear.
def check_result():
    value1 = 5
    value2 = 3
    # This will now reliably equal 15.
    result = do_something(value1, value2)

    # The conditions that are now relevant.
    if result > 20:
        output_label.config(text="Try Again")
    else:
        output_label.config(text="Almost There")

    if 10 <= result <= 20:
        hidden_flag_label.config(text="You found something... But is it the real flag? 🤔")

    # This is the winning condition. It is now reachable.
    if result == 15:
        secret_flag_label.config(text="FLAG{GUI_Debug_Success}")

# --- GUI Setup Code ---
root = tk.Tk()
root.title("Trace the Code Challenge")
root.geometry("400x300")
title_label = tk.Label(root, text="Debug the Code to Find the Flag!", font=("Arial", 12, "bold"))
title_label.pack(pady=10)
check_button = tk.Button(root, text="Run Code", command=check_result)
check_button.pack(pady=5)
output_label = tk.Label(root, text="", font=("Arial", 10))
output_label.pack(pady=5)
hidden_flag_label = tk.Label(root, text="", font=("Arial", 10, "italic"), fg="gray")
hidden_flag_label.pack(pady=5)
secret_flag_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="green")
secret_flag_label.pack(pady=10)
root.mainloop()