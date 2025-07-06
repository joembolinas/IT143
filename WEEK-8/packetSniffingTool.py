"""

"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from scapy.all import sniff, IP, TCP, UDP, conf, get_if_list

# Global variables
sniffing = False
packet_list = []

def check_interfaces():
    """Check available network interfaces"""
    print("Available network interfaces:")
    interfaces = get_if_list()
    for i, interface in enumerate(interfaces):
        print(f"{i}: {interface}")
    return interfaces

def start_sniffing():
    """Start packet sniffing"""
    global sniffing
    sniffing = True
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    
    # Run sniffing in a separate thread to keep GUI responsive
    sniff_thread = threading.Thread(target=packet_sniffing_logic)
    sniff_thread.daemon = True
    sniff_thread.start()

def stop_sniffing():
    """Stop packet sniffing"""
    global sniffing
    sniffing = False
    start_button.config(state="normal")
    stop_button.config(state="disabled")

def packet_sniffing_logic():
    """Main packet sniffing logic"""
    try:
        # Choose a valid network interface dynamically
        interface = conf.route.route("0.0.0.0")[0]
        
        # Start sniffing packets
        sniff(iface=interface, prn=process_packet, stop_filter=lambda x: not sniffing)
        
    except Exception as e:
        print(f"Error during packet sniffing: {e}")
        print("Make sure you have Npcap installed and are running as Administrator")

def process_packet(packet):
    """Process captured packets"""
    global packet_list
    
    if IP in packet:
        # Extract packet information
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        length = len(packet)
        
        # Determine protocol
        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"
        else:
            protocol = "Other"
        
        # Store packet for detailed view
        packet_list.append(packet)
        
        # Insert packet info into the GUI table
        packet_tree.insert("", "end", values=(src_ip, dst_ip, protocol, length))

def show_packet_details(event):
    """Show detailed packet information when clicked"""
    selection = packet_tree.selection()
    if selection:
        # Get selected item index
        item = packet_tree.selection()[0]
        index = packet_tree.index(item)
        
        if index < len(packet_list):
            packet = packet_list[index]
            
            # Clear previous details
            detail_text.delete(1.0, tk.END)
            
            # Show packet details
            detail_text.insert(tk.END, f"Packet Details:\n")
            detail_text.insert(tk.END, f"{'='*50}\n")
            detail_text.insert(tk.END, packet.show(dump=True))

# Create the main GUI window
root = tk.Tk()
root.title("Python Packet Sniffer")
root.geometry("800x600")

# Create start and stop buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start Sniffing", command=start_sniffing, bg="green", fg="white")
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop Sniffing", command=stop_sniffing, bg="red", fg="white", state="disabled")
stop_button.pack(side=tk.LEFT, padx=5)

# Create packet table (Treeview widget)
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Create Treeview with columns
columns = ("Source", "Destination", "Protocol", "Length")
packet_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

# Define column headings
for col in columns:
    packet_tree.heading(col, text=col)
    packet_tree.column(col, width=150)

# Add scrollbar to the treeview
tree_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=packet_tree.yview)
packet_tree.configure(yscrollcommand=tree_scrollbar.set)

# Pack the treeview and scrollbar
packet_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Bind click event to show packet details
packet_tree.bind("<ButtonRelease-1>", show_packet_details)

# Create packet details section
detail_frame = tk.Frame(root)
detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

detail_label = tk.Label(detail_frame, text="Packet Details:", font=("Arial", 12, "bold"))
detail_label.pack(anchor=tk.W)

detail_text = scrolledtext.ScrolledText(detail_frame, height=10, wrap=tk.WORD)
detail_text.pack(fill=tk.BOTH, expand=True)

# Check available interfaces when starting
print("Checking available network interfaces...")
check_interfaces()

# Start the GUI event loop
if __name__ == "__main__":
    print("Starting Packet Sniffer GUI...")
    print("Note: Make sure you have Npcap installed and run as Administrator on Windows")
    root.mainloop()


"""
# TODO: Review key implementation notes for the Python Packet Sniffer.

Main Differences from LMS Material:
    1. Interface Check: LMS shows simple print(get_if_list()) - Complete code adds user-friendly formatting with numbered list

    2. Global Variables: LMS doesn't show explicit globals - Complete code needs sniffing = False and packet_list = [] for state management

    3. Error Handling: LMS mentions it conceptually - Complete code implements actual try/catch blocks

    4. Function Structure: LMS shows conceptual blocks - Complete code shows working implementations with proper threading and GUI state management


Why These Differences:
    * LMS = Teaching concepts (what to do)
    * Complete code = Working implementation (how to do it)
    * LMS breaks down learning, complete code needs all pieces integrated

Setup Requirements:
pip install scapy tkinter

    * Install Npcap (Windows) with WinPcap compatibility
    * Run as Administrator
    * Handles IP packets (TCP/UDP) with GUI display

Core Architecture:
    * Multi-threaded (GUI + packet capture)
    * Tkinter GUI with Treeview for packet display
    * Click packet → view details
    * Start/Stop controls with proper state management

The LMS teaches the structure, the complete code makes it production-ready.
"""