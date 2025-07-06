#!/usr/bin/env python3
# Test script to check if all required modules can be imported

print("Testing imports...")

try:
    import tkinter as tk
    print("✓ tkinter imported successfully")
except ImportError as e:
    print(f"✗ tkinter import failed: {e}")

try:
    from tkinter import filedialog, ttk, messagebox, scrolledtext
    print("✓ tkinter submodules imported successfully")
except ImportError as e:
    print(f"✗ tkinter submodules import failed: {e}")

try:
    import json
    print("✓ json imported successfully")
except ImportError as e:
    print(f"✗ json import failed: {e}")

try:
    import re
    print("✓ re imported successfully")
except ImportError as e:
    print(f"✗ re import failed: {e}")

try:
    import pandas as pd
    print("✓ pandas imported successfully")
except ImportError as e:
    print(f"✗ pandas import failed: {e}")

try:
    import requests
    print("✓ requests imported successfully")
except ImportError as e:
    print(f"✗ requests import failed: {e}")

try:
    import matplotlib.pyplot as plt
    print("✓ matplotlib imported successfully")
except ImportError as e:
    print(f"✗ matplotlib import failed: {e}")

try:
    import seaborn as sns
    print("✓ seaborn imported successfully")
except ImportError as e:
    print(f"✗ seaborn import failed: {e}")

print("\nAll imports tested!")
print("Starting HAR Analyzer Application...")

# Now try to import and run the main application
try:
    import sys
    import os
    
    # Add WEEK-8 directory to path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'WEEK-8'))
    
    # Create GUI
    root = tk.Tk()
    
    # Simple test GUI to verify tkinter works
    label = tk.Label(root, text="HAR Analyzer - All modules loaded successfully!", 
                    font=("Arial", 14), fg="green")
    label.pack(pady=20)
    
    button = tk.Button(root, text="Close", command=root.quit, 
                      font=("Arial", 12), bg="red", fg="white")
    button.pack(pady=10)
    
    root.title("Import Test Success")
    root.geometry("400x150")
    
    print("✓ GUI created successfully - showing test window")
    root.mainloop()
    
except Exception as e:
    print(f"✗ Error creating GUI: {e}")
