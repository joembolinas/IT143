#!/usr/bin/env python3
"""
CTF Week 7: The Hidden Code - Flag Decoder
Mission: Extract hidden flags from encoded transaction data

Author: MO-IT143 Student
Date: June 20, 2025
Challenge: Cyboria's Encrypted Marketplaces
"""

import pandas as pd
import re
import base64
import binascii
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import filedialog
import os

class FlagDecoder:
    def __init__(self):
        self.df = None
        self.found_flags = []
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI for the flag decoder"""
        self.root = tk.Tk()
        self.root.title("CTF Week 7: The Hidden Code - Flag Decoder")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        
        # Title Label
        title_label = tk.Label(
            self.root, 
            text="🔍 CTF FLAG DECODER - CYBORIA'S ENCRYPTED MARKETPLACES",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack(pady=10)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg="#2c3e50")
        control_frame.pack(pady=5)
        
        # Load CSV Button
        self.load_btn = tk.Button(
            control_frame,
            text="📁 Load Transaction CSV",
            command=self.load_csv,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=5
        )
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Analyze Button
        self.analyze_btn = tk.Button(
            control_frame,
            text="🔍 Analyze & Decode",
            command=self.analyze_data,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=5,
            state=tk.DISABLED
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # Export Results Button
        self.export_btn = tk.Button(
            control_frame,
            text="💾 Export Results",
            command=self.export_results,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=5,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = tk.Label(
            self.root,
            text="Status: Ready to load CSV file",
            bg="#2c3e50",
            fg="#f39c12",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=5)
        
        # Results Text Area
        results_label = tk.Label(
            self.root,
            text="🏆 DECODED FLAGS & ANALYSIS RESULTS:",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        results_label.pack(pady=(10, 5))
        
        self.results_text = scrolledtext.ScrolledText(
            self.root,
            width=120,
            height=25,
            bg="#34495e",
            fg="#ecf0f1",
            font=("Consolas", 10),
            insertbackground="white"
        )
        self.results_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='determinate',
            length=400
        )
        self.progress.pack(pady=5)
    
    def load_csv(self):
        """Load the CSV file containing transaction data"""
        file_path = filedialog.askopenfilename(
            title="Select Leaked Transactions CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.status_label.config(text=f"✅ Loaded: {len(self.df)} transactions from {os.path.basename(file_path)}")
                self.analyze_btn.config(state=tk.NORMAL)
                
                # Display basic info
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"📊 TRANSACTION DATA LOADED\n")
                self.results_text.insert(tk.END, f"{'='*60}\n")
                self.results_text.insert(tk.END, f"Records: {len(self.df)}\n")
                self.results_text.insert(tk.END, f"Columns: {list(self.df.columns)}\n")
                self.results_text.insert(tk.END, f"File: {os.path.basename(file_path)}\n\n")
                
                # Preview first few rows
                self.results_text.insert(tk.END, "📋 DATA PREVIEW:\n")
                self.results_text.insert(tk.END, f"{'-'*60}\n")
                self.results_text.insert(tk.END, str(self.df.head()))
                self.results_text.insert(tk.END, "\n\n")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {str(e)}")
                self.status_label.config(text="❌ Error loading CSV file")
    
    def is_base64(self, s):
        """Check if string is valid Base64"""
        try:
            if len(s) % 4 != 0:
                return False
            # Check if it contains only valid Base64 characters
            if re.match(r'^[A-Za-z0-9+/]*={0,2}$', s):
                base64.b64decode(s, validate=True)
                return True
            return False
        except:
            return False
    
    def is_hex(self, s):
        """Check if string is valid hexadecimal"""
        try:
            if len(s) % 2 != 0:
                return False
            int(s, 16)
            return True
        except:
            return False
    
    def decode_base64(self, encoded_str):
        """Decode Base64 string"""
        try:
            decoded_bytes = base64.b64decode(encoded_str)
            return decoded_bytes.decode('utf-8', errors='ignore')
        except:
            return None
    
    def decode_hex(self, hex_str):
        """Decode hexadecimal string"""
        try:
            decoded_bytes = bytes.fromhex(hex_str)
            return decoded_bytes.decode('utf-8', errors='ignore')
        except:
            return None
    
    def find_flag_patterns(self, text):
        """Search for flag patterns in decoded text"""
        # Common CTF flag patterns
        flag_patterns = [
            r'flag\{[^}]+\}',           # flag{...}
            r'FLAG\{[^}]+\}',           # FLAG{...}
            r'CTF\{[^}]+\}',            # CTF{...}
            r'cyboria\{[^}]+\}',        # cyboria{...}
            r'CYBORIA\{[^}]+\}',        # CYBORIA{...}
            r'[a-zA-Z0-9_]+\{[^}]+\}',  # generic{...}
        ]
        
        flags = []
        for pattern in flag_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            flags.extend(matches)
        
        return flags
    
    def analyze_data(self):
        """Analyze the CSV data for encoded flags"""
        if self.df is None:
            messagebox.showwarning("Warning", "Please load a CSV file first")
            return
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "🔍 STARTING ENCODED FLAG ANALYSIS\n")
        self.results_text.insert(tk.END, f"{'='*70}\n\n")
        
        self.found_flags = []
        encoded_data_found = []
        total_cells = len(self.df) * len(self.df.columns)
        processed = 0
        
        self.progress['maximum'] = total_cells
        
        # Analyze each cell in the DataFrame
        for col_index, column in enumerate(self.df.columns):
            self.results_text.insert(tk.END, f"🔎 Analyzing column: {column}\n")
            self.results_text.update()
            
            for row_index, value in enumerate(self.df[column]):
                processed += 1
                self.progress['value'] = processed
                self.root.update_idletasks()
                
                if pd.isna(value):
                    continue
                
                value_str = str(value).strip()
                
                # Skip short strings
                if len(value_str) < 8:
                    continue
                
                # Check for Base64 encoding
                if self.is_base64(value_str):
                    decoded = self.decode_base64(value_str)
                    if decoded:
                        flags = self.find_flag_patterns(decoded)
                        if flags:
                            for flag in flags:
                                flag_info = {
                                    'flag': flag,
                                    'method': 'Base64',
                                    'column': column,
                                    'row': row_index,
                                    'original': value_str,
                                    'decoded': decoded
                                }
                                self.found_flags.append(flag_info)
                                self.results_text.insert(tk.END, f"🏆 FLAG FOUND! {flag} (Base64 in {column}, row {row_index})\n")
                        else:
                            encoded_data_found.append({
                                'method': 'Base64',
                                'column': column,
                                'row': row_index,
                                'original': value_str[:50] + "...",
                                'decoded': decoded[:100] + "..." if len(decoded) > 100 else decoded
                            })
                
                # Check for Hex encoding
                elif self.is_hex(value_str):
                    decoded = self.decode_hex(value_str)
                    if decoded:
                        flags = self.find_flag_patterns(decoded)
                        if flags:
                            for flag in flags:
                                flag_info = {
                                    'flag': flag,
                                    'method': 'Hexadecimal',
                                    'column': column,
                                    'row': row_index,
                                    'original': value_str,
                                    'decoded': decoded
                                }
                                self.found_flags.append(flag_info)
                                self.results_text.insert(tk.END, f"🏆 FLAG FOUND! {flag} (Hex in {column}, row {row_index})\n")
                        else:
                            encoded_data_found.append({
                                'method': 'Hexadecimal',
                                'column': column,
                                'row': row_index,
                                'original': value_str[:50] + "...",
                                'decoded': decoded[:100] + "..." if len(decoded) > 100 else decoded
                            })
        
        # Display results
        self.results_text.insert(tk.END, f"\n{'='*70}\n")
        self.results_text.insert(tk.END, f"📊 ANALYSIS COMPLETE\n")
        self.results_text.insert(tk.END, f"{'='*70}\n\n")
        
        if self.found_flags:
            self.results_text.insert(tk.END, f"🎉 SUCCESS! Found {len(self.found_flags)} FLAG(S):\n")
            self.results_text.insert(tk.END, f"{'-'*70}\n")
            
            for i, flag_info in enumerate(self.found_flags, 1):
                self.results_text.insert(tk.END, f"\n🏆 FLAG #{i}:\n")
                self.results_text.insert(tk.END, f"   Flag: {flag_info['flag']}\n")
                self.results_text.insert(tk.END, f"   Method: {flag_info['method']}\n")
                self.results_text.insert(tk.END, f"   Location: Column '{flag_info['column']}', Row {flag_info['row']}\n")
                self.results_text.insert(tk.END, f"   Original: {flag_info['original']}\n")
                self.results_text.insert(tk.END, f"   Decoded: {flag_info['decoded']}\n")
            
            self.export_btn.config(state=tk.NORMAL)
        else:
            self.results_text.insert(tk.END, "❌ No flags found in obvious patterns.\n")
        
        # Show encoded data found (but no flags)
        if encoded_data_found:
            self.results_text.insert(tk.END, f"\n📋 ENCODED DATA FOUND (No flags detected):\n")
            self.results_text.insert(tk.END, f"{'-'*70}\n")
            
            for i, data in enumerate(encoded_data_found[:10], 1):  # Show first 10
                self.results_text.insert(tk.END, f"\n{i}. {data['method']} in '{data['column']}', row {data['row']}:\n")
                self.results_text.insert(tk.END, f"   Original: {data['original']}\n")
                self.results_text.insert(tk.END, f"   Decoded: {data['decoded']}\n")
            
            if len(encoded_data_found) > 10:
                self.results_text.insert(tk.END, f"\n... and {len(encoded_data_found) - 10} more encoded entries.\n")
        
        self.status_label.config(text=f"✅ Analysis complete: {len(self.found_flags)} flags found")
        self.progress['value'] = 0
    
    def export_results(self):
        """Export the found flags to a text file"""
        if not self.found_flags:
            messagebox.showwarning("Warning", "No flags found to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Flag Results",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfilename="ctf_week7_flags.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("CTF Week 7: The Hidden Code - Flag Results\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for i, flag_info in enumerate(self.found_flags, 1):
                        f.write(f"FLAG #{i}:\n")
                        f.write(f"Flag: {flag_info['flag']}\n")
                        f.write(f"Method: {flag_info['method']}\n")
                        f.write(f"Location: Column '{flag_info['column']}', Row {flag_info['row']}\n")
                        f.write(f"Original: {flag_info['original']}\n")
                        f.write(f"Decoded: {flag_info['decoded']}\n")
                        f.write("-" * 50 + "\n\n")
                
                messagebox.showinfo("Success", f"Results exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {str(e)}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main function to run the flag decoder"""
    print("🔍 CTF Week 7: The Hidden Code - Flag Decoder")
    print("=" * 50)
    print("Mission: Extract hidden flags from encoded transaction data")
    print("Loading GUI interface...")
    
    app = FlagDecoder()
    app.run()

if __name__ == "__main__":
    main()
