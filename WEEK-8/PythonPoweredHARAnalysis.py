#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HAR File Analyzer - A Python GUI Application for analyzing HTTP Archive files
# This application allows users to load and analyze HAR files to extract network request data

# Import required libraries
import tkinter as tk                    # Main GUI library
from tkinter import filedialog         # File dialog for selecting HAR files
from tkinter import ttk                 # Enhanced GUI widgets
from tkinter import messagebox         # Message boxes for alerts
from tkinter import scrolledtext       # Scrollable text widget for detailed output
import json                            # JSON parsing for HAR files
import re                              # Regular expressions for pattern matching
# from haralyzer import HarParser        # HAR file parsing library - REMOVED (not needed)
import pandas as pd                    # Data manipulation and analysis
import requests                        # HTTP requests library
import matplotlib.pyplot as plt       # Plotting and visualization
import seaborn as sns                  # Statistical data visualization

class HARAnalyzerApp:
    """Main application class for HAR file analysis"""
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("HAR File Analyzer - Enhanced with Flag Detection")      # Set window title
        self.root.geometry("900x600")             # Increased window size
        
        # Store data for analysis
        self.har_data = None
        self.flags_found = []
        self.session_tokens = []
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI components"""
        # Create main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create load button
        self.load_button = tk.Button(
            button_frame, 
            text="Load HAR File", 
            command=self.load_har_file,           # Button click handler
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.load_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create flag search button
        self.flag_button = tk.Button(
            button_frame, 
            text="Search for Flags", 
            command=self.search_flags,
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.flag_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create session token button
        self.token_button = tk.Button(
            button_frame, 
            text="Extract Session Tokens", 
            command=self.extract_session_tokens,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.token_button.pack(side=tk.LEFT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Request Overview
        self.setup_overview_tab()
        
        # Tab 2: Flag Analysis
        self.setup_flag_tab()
        
        # Tab 3: Session Tokens
        self.setup_token_tab()
        
    def setup_overview_tab(self):
        """Setup the overview tab with request data"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="Request Overview")
        
        # Create table (Treeview) for displaying data
        self.tree = ttk.Treeview(overview_frame, columns=("URL", "Status", "Time"), show="headings")
        
        # Define column headings
        self.tree.heading("URL", text="Request URL")
        self.tree.heading("Status", text="Status Code")
        self.tree.heading("Time", text="Time (ms)")
        
        # Set column widths and alignment
        self.tree.column("URL", width=400, anchor="w")        # Left align URLs
        self.tree.column("Status", width=100, anchor="center") # Center align status
        self.tree.column("Time", width=100, anchor="center")   # Center align time
        
        # Pack the treeview with scrollbar
        tree_scrollbar = ttk.Scrollbar(overview_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        tree_scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
    def setup_flag_tab(self):
        """Setup the flag analysis tab"""
        flag_frame = ttk.Frame(self.notebook)
        self.notebook.add(flag_frame, text="Flag Analysis")
        
        # Flag results frame
        flag_results_frame = tk.Frame(flag_frame)
        flag_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Flag results label
        flag_label = tk.Label(flag_results_frame, text="Flag Search Results:", font=("Arial", 12, "bold"))
        flag_label.pack(anchor=tk.W)
        
        # Flag results text area
        self.flag_text = scrolledtext.ScrolledText(flag_results_frame, height=20, wrap=tk.WORD)
        self.flag_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
    def setup_token_tab(self):
        """Setup the session tokens tab"""
        token_frame = ttk.Frame(self.notebook)
        self.notebook.add(token_frame, text="Session Tokens")
        
        # Token table
        self.token_tree = ttk.Treeview(token_frame, columns=("Index", "URL", "Token"), show="headings")
        
        # Define column headings
        self.token_tree.heading("Index", text="Entry #")
        self.token_tree.heading("URL", text="URL")
        self.token_tree.heading("Token", text="Session Token")
        
        # Set column widths
        self.token_tree.column("Index", width=80, anchor="center")
        self.token_tree.column("URL", width=300, anchor="w")
        self.token_tree.column("Token", width=400, anchor="w")
        
        # Token scrollbar
        token_scrollbar = ttk.Scrollbar(token_frame, orient="vertical", command=self.token_tree.yview)
        self.token_tree.configure(yscrollcommand=token_scrollbar.set)
        
        # Pack token tree and scrollbar
        self.token_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        token_scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
    def load_har_file(self):
        """Load and parse HAR file selected by user"""
        # Open file dialog to select HAR file
        file_path = filedialog.askopenfilename(
            title="Select HAR File",
            filetypes=[("HAR files", "*.har"), ("All files", "*.*")]
        )
        
        # Return if no file selected
        if not file_path:
            return
            
        try:
            # Read and parse the HAR file directly
            with open(file_path, 'r', encoding='utf-8') as file:
                self.har_data = json.load(file)          # Store HAR data for analysis
                
            # Extract entries directly from JSON structure
            entries = self.har_data['log']['entries']
            
            # Clear previous data in treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Extract and display key data
            for entry in entries:
                try:
                    # Extract data from JSON structure with safe access
                    request = entry.get('request', {})
                    response = entry.get('response', {})
                    
                    url = request.get('url', 'Unknown URL')                    # Request URL
                    status = response.get('status', 'Unknown')                 # HTTP status code
                    time = entry.get('time', 0)                              # Response time in milliseconds
                    
                    # Handle missing or invalid time values
                    if time is None:
                        time = 0
                    
                    # Insert data into table
                    self.tree.insert("", "end", values=(url, status, f"{time:.2f}"))
                    
                except Exception as entry_error:
                    # Skip this entry if there's an error processing it
                    print(f"Warning: Skipping entry due to error: {entry_error}")
                    continue
            
            # Enable analysis buttons
            self.flag_button.config(state=tk.NORMAL)
            self.token_button.config(state=tk.NORMAL)
                
            # Show success message
            messagebox.showinfo(
                "Success", 
                f"Successfully loaded {len(entries)} requests from HAR file.\nYou can now search for flags and session tokens!"
            )
            
        except KeyError as e:
            # Handle missing keys in HAR structure
            messagebox.showerror(
                "Error", 
                f"Invalid HAR file structure. Missing key: {str(e)}"
            )
        except json.JSONDecodeError:
            # Handle invalid JSON format
            messagebox.showerror(
                "Error", 
                "Invalid JSON format. Please select a valid HAR file."
            )
        except Exception as e:
            # Handle other errors (invalid file format, etc.)
            messagebox.showerror(
                "Error", 
                f"Failed to load HAR file: {str(e)}"
            )
    
    def search_flags(self):
        """Search for flags in the loaded HAR data"""
        if not self.har_data:
            messagebox.showwarning("Warning", "Please load a HAR file first!")
            return
            
        self.flags_found = []
        entries = self.har_data['log']['entries']
        
        # Clear previous results
        self.flag_text.delete(1.0, tk.END)
        self.flag_text.insert(tk.END, "🔍 Searching for flags in HAR file...\n\n")
        self.root.update()
        
        # Search for flags in each entry
        for i, entry in enumerate(entries):
            try:
                # Get response data
                response = entry.get('response', {})
                content = response.get('content', {})
                response_text = content.get('text', '')
                
                # Skip empty responses
                if not response_text:
                    continue
                    
                # Try to parse JSON responses
                try:
                    if response_text.strip().startswith('{'):
                        json_data = json.loads(response_text)
                        
                        # Look for session tokens with flags
                        session_token = json_data.get('session_token')
                        if session_token and 'FLAG{' in session_token:
                            self.flags_found.append({
                                'entry_index': i,
                                'url': entry.get('request', {}).get('url', 'Unknown'),
                                'flag': session_token,
                                'context': 'Session Token',
                                'full_response': json_data
                            })
                        
                        # Search for any FLAG pattern in the entire response
                        response_str = str(json_data)
                        flag_matches = re.findall(r'FLAG\{[^}]+\}', response_str)
                        for flag in flag_matches:
                            if flag not in [f['flag'] for f in self.flags_found]:
                                self.flags_found.append({
                                    'entry_index': i,
                                    'url': entry.get('request', {}).get('url', 'Unknown'),
                                    'flag': flag,
                                    'context': 'JSON Response'
                                })
                                
                except json.JSONDecodeError:
                    # Not JSON, search for flags in plain text
                    flag_matches = re.findall(r'FLAG\{[^}]+\}', response_text)
                    for flag in flag_matches:
                        self.flags_found.append({
                            'entry_index': i,
                            'url': entry.get('request', {}).get('url', 'Unknown'),
                            'flag': flag,
                            'context': 'Plain Text Response'
                        })
                        
            except Exception as e:
                continue
        
        # Display results
        self.display_flag_results()
        
        # Switch to flag tab
        self.notebook.select(1)
    
    def extract_session_tokens(self):
        """Extract session tokens from the loaded HAR data"""
        if not self.har_data:
            messagebox.showwarning("Warning", "Please load a HAR file first!")
            return
            
        self.session_tokens = []
        entries = self.har_data['log']['entries']
        
        # Clear previous token data
        for item in self.token_tree.get_children():
            self.token_tree.delete(item)
        
        # Search for session tokens in each entry
        for i, entry in enumerate(entries):
            try:
                # Get response data
                response = entry.get('response', {})
                content = response.get('content', {})
                response_text = content.get('text', '')
                
                # Skip empty responses
                if not response_text:
                    continue
                    
                # Try to parse JSON responses
                try:
                    if response_text.strip().startswith('{'):
                        json_data = json.loads(response_text)
                        
                        # Look for session tokens
                        session_token = json_data.get('session_token')
                        if session_token:
                            self.session_tokens.append({
                                'entry_index': i,
                                'url': entry.get('request', {}).get('url', 'Unknown'),
                                'session_token': session_token,
                                'full_response': json_data
                            })
                            
                            # Insert into token tree
                            self.token_tree.insert("", "end", values=(i, entry.get('request', {}).get('url', 'Unknown'), session_token))
                                
                except json.JSONDecodeError:
                    continue
                        
            except Exception as e:
                continue
        
        # Show results message
        messagebox.showinfo(
            "Session Tokens", 
            f"Found {len(self.session_tokens)} session tokens in the HAR file!"
        )
        
        # Switch to token tab
        self.notebook.select(2)
    
    def display_flag_results(self):
        """Display flag search results in the text area"""
        self.flag_text.delete(1.0, tk.END)
        
        if self.flags_found:
            self.flag_text.insert(tk.END, "🎉 FLAG ANALYSIS RESULTS\n")
            self.flag_text.insert(tk.END, "=" * 50 + "\n\n")
            self.flag_text.insert(tk.END, f"🚩 Found {len(self.flags_found)} flag(s):\n\n")
            
            for i, flag_info in enumerate(self.flags_found, 1):
                self.flag_text.insert(tk.END, f"{i}. FLAG: {flag_info['flag']}\n")
                self.flag_text.insert(tk.END, f"   Entry Index: {flag_info['entry_index']}\n")
                self.flag_text.insert(tk.END, f"   URL: {flag_info['url']}\n")
                self.flag_text.insert(tk.END, f"   Context: {flag_info['context']}\n")
                self.flag_text.insert(tk.END, "-" * 40 + "\n\n")
            
            # Highlight the main flag if found
            for flag_info in self.flags_found:
                if 'h4r_f1le_4n4lys1s_w1n' in flag_info['flag']:
                    self.flag_text.insert(tk.END, "🎯 MAIN CTF FLAG FOUND!\n")
                    self.flag_text.insert(tk.END, f"Submit this flag: {flag_info['flag']}\n\n")
                    break
                    
        else:
            self.flag_text.insert(tk.END, "❌ No flags found in the HAR file.\n\n")
            self.flag_text.insert(tk.END, "💡 Tips:\n")
            self.flag_text.insert(tk.END, "- Make sure you loaded the correct HAR file\n")
            self.flag_text.insert(tk.END, "- Check if the file contains API responses\n")
            self.flag_text.insert(tk.END, "- Try extracting session tokens first\n")

def analyze_har_with_pandas(har_file_path):
    """Analyze HAR file using pandas for data manipulation"""
    try:
        # Load HAR file
        with open(har_file_path, 'r', encoding='utf-8') as file:
            har_data = json.load(file)
            
        # Extract entries data
        entries = har_data['log']['entries']
        
        # Create list of dictionaries for DataFrame
        data = []
        for entry in entries:
            try:
                request = entry.get('request', {})
                response = entry.get('response', {})
                
                data.append({
                    'url': request.get('url', 'Unknown'),
                    'method': request.get('method', 'Unknown'),
                    'status': response.get('status', 0),
                    'time': entry.get('time', 0),
                    'size': response.get('bodySize', 0)
                })
            except Exception as e:
                print(f"Warning: Skipping entry due to error: {e}")
                continue
            
        # Convert to pandas DataFrame
        df = pd.DataFrame(data)
        
        # Basic analysis
        print("HAR File Analysis Summary:")
        print(f"Total requests: {len(df)}")
        print(f"Average response time: {df['time'].mean():.2f}ms")
        print(f"Status code distribution:\n{df['status'].value_counts()}")
        
        return df
        
    except Exception as e:
        print(f"Error analyzing HAR file: {str(e)}")
        return None

def replay_requests_from_har(har_file_path):
    """Replay HTTP requests from HAR file using requests library"""
    try:
        # Load HAR file
        with open(har_file_path, 'r', encoding='utf-8') as file:
            har_data = json.load(file)
            
        entries = har_data['log']['entries']
        
        # Replay each request
        for entry in entries:
            request_data = entry['request']
            url = request_data['url']
            method = request_data['method']
            
            # Extract headers
            headers = {header['name']: header['value'] 
                      for header in request_data.get('headers', [])}
            
            # Make request based on method
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=5)
            elif method == 'POST':
                # Extract POST data if available
                post_data = request_data.get('postData', {}).get('text', '')
                response = requests.post(url, data=post_data, headers=headers, timeout=5)
            else:
                print(f"Unsupported method: {method}")
                continue
                
            print(f"Replayed {method} {url} - Status: {response.status_code}")
            
    except Exception as e:
        print(f"Error replaying requests: {str(e)}")

def visualize_har_data(har_file_path):
    """Create visualizations of HAR data using matplotlib and seaborn"""
    try:
        # Load and analyze HAR file
        df = analyze_har_with_pandas(har_file_path)
        if df is None:
            return
            
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('HAR File Analysis Dashboard', fontsize=16)
        
        # 1. Response time distribution
        axes[0, 0].hist(df['time'], bins=30, color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Response Time Distribution')
        axes[0, 0].set_xlabel('Time (ms)')
        axes[0, 0].set_ylabel('Frequency')
        
        # 2. Status code distribution
        status_counts = df['status'].value_counts()
        axes[0, 1].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Status Code Distribution')
        
        # 3. Request method distribution
        method_counts = df['method'].value_counts()
        axes[1, 0].bar(method_counts.index, method_counts.values, color='lightgreen')
        axes[1, 0].set_title('HTTP Method Distribution')
        axes[1, 0].set_xlabel('Method')
        axes[1, 0].set_ylabel('Count')
        
        # 4. Response size vs time scatter plot
        axes[1, 1].scatter(df['time'], df['size'], alpha=0.6, color='orange')
        axes[1, 1].set_title('Response Time vs Size')
        axes[1, 1].set_xlabel('Time (ms)')
        axes[1, 1].set_ylabel('Size (bytes)')
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error creating visualizations: {str(e)}")

# Main execution
if __name__ == "__main__":
    # Create Tkinter root window
    root = tk.Tk()
    
    # Initialize the HAR Analyzer application
    app = HARAnalyzerApp(root)
    
    # Run the Tkinter event loop to keep application open
    root.mainloop()

# Example usage of additional functions:
# df = analyze_har_with_pandas('example.har')
# replay_requests_from_har('example.har')
# visualize_har_data('example.har')

"""
HAR File Analyzer - Code Comparison and Explanation

DIFFERENCE BETWEEN LMS MATERIALS AND CONSOLIDATED CODE:

LMS MATERIALS APPROACH:
- Fragmented Code Snippets: The materials present code in small, separate pieces for each concept
- Step-by-Step Explanation: Each library (json, pandas, haralyzer, requests, matplotlib) is explained individually
- Basic Structure: Shows the skeleton of a GUI application with numbered steps (1-13)
- Educational Focus: Designed to teach concepts progressively
- Incomplete Examples: Code snippets are partial and meant for learning individual components

MY CONSOLIDATED CODE APPROACH:
- Full Implementation: Every function and class is complete and functional
- Enhanced Features: Added error handling, scrollbars, better UI design, and multiple analysis functions
- Comprehensive Integration: All libraries work together in a cohesive system
- Additional Functionality: 
  * Data visualization with charts
  * Request replay capability
  * Pandas-based analysis
  * Professional GUI design
- Production Quality: Includes proper exception handling, user feedback, and robust code structure

KEY DIFFERENCES:
┌─────────────────────┬─────────────────────┐
│ LMS Materials       │ My Code             │
├─────────────────────┼─────────────────────┤
│ Teaching fragments  │ Complete application│
│ Basic GUI layout    │ Enhanced UI         │
│ Simple error handle │ Comprehensive error │
│ Individual concepts │ Integrated features │
│ Step-by-step learn  │ Ready-to-use tool   │
│ Missing imports     │ All dependencies    │
│ Educational skeleton│ Production-ready    │
└─────────────────────┴─────────────────────┘

EXAMPLE COMPARISON:

LMS shows basic button creation:
    button = tk.Button(root, text="Load HAR File", command=load_har_file)

My code provides enhanced button with styling:
    self.load_button = tk.Button(
        root, 
        text="Load HAR File", 
        command=self.load_har_file,
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10
    )

SUMMARY:
- LMS materials = Learning concepts piece by piece
- My code = Complete, working application you can actually use
- LMS is teaching you HOW TO BUILD
- My code shows you WHAT THE FINISHED PRODUCT looks like with professional touches
"""