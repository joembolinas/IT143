#!/usr/bin/env python3
"""
CTF Week 8: Web Traffic Inspector - Flag Extractor
Mission: Extract hidden flag from session token in HAR file

This script analyzes the captured web traffic HAR file to find
the session token containing the hidden flag.
"""

import json
import re
import sys

def analyze_har_for_flags(har_file_path):
    """
    Analyze HAR file to extract session tokens and find the flag
    
    Args:
        har_file_path (str): Path to the HAR file
        
    Returns:
        list: Found flags and session tokens
    """
    flags_found = []
    session_tokens = []
    
    try:
        # Load HAR file
        print(f"📁 Loading HAR file: {har_file_path}")
        with open(har_file_path, 'r', encoding='utf-8') as file:
            har_data = json.load(file)
            
        # Extract entries
        entries = har_data['log']['entries']
        print(f"🔍 Analyzing {len(entries)} network requests...")
        
        # Analyze each entry
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
                            session_tokens.append({
                                'entry_index': i,
                                'url': entry.get('request', {}).get('url', 'Unknown'),
                                'session_token': session_token,
                                'full_response': json_data
                            })
                            print(f"🎯 Found session token in entry {i}: {session_token}")
                            
                            # Check if session token contains flag
                            if 'FLAG{' in session_token:
                                flags_found.append({
                                    'entry_index': i,
                                    'url': entry.get('request', {}).get('url', 'Unknown'),
                                    'flag': session_token,
                                    'full_response': json_data
                                })
                                print(f"🚩 FLAG FOUND in entry {i}: {session_token}")
                        
                        # Also search for any FLAG pattern in the entire response
                        response_str = str(json_data)
                        flag_matches = re.findall(r'FLAG\{[^}]+\}', response_str)
                        for flag in flag_matches:
                            if flag not in [f['flag'] for f in flags_found]:
                                flags_found.append({
                                    'entry_index': i,
                                    'url': entry.get('request', {}).get('url', 'Unknown'),
                                    'flag': flag,
                                    'context': 'Found in JSON response'
                                })
                                print(f"🚩 FLAG FOUND in entry {i}: {flag}")
                                
                except json.JSONDecodeError:
                    # Not JSON, search for flags in plain text
                    flag_matches = re.findall(r'FLAG\{[^}]+\}', response_text)
                    for flag in flag_matches:
                        flags_found.append({
                            'entry_index': i,
                            'url': entry.get('request', {}).get('url', 'Unknown'),
                            'flag': flag,
                            'context': 'Found in plain text response'
                        })
                        print(f"🚩 FLAG FOUND in entry {i}: {flag}")
                        
            except Exception as e:
                # Skip problematic entries
                continue
                
        return flags_found, session_tokens
        
    except Exception as e:
        print(f"❌ Error analyzing HAR file: {str(e)}")
        return [], []

def display_results(flags_found, session_tokens):
    """Display the analysis results"""
    
    print("\n" + "="*60)
    print("🎯 CTF ANALYSIS RESULTS")
    print("="*60)
    
    if flags_found:
        print(f"\n🚩 FLAGS FOUND ({len(flags_found)}):")
        print("-" * 40)
        for i, flag_info in enumerate(flags_found, 1):
            print(f"\n{i}. FLAG: {flag_info['flag']}")
            print(f"   URL: {flag_info['url']}")
            print(f"   Entry Index: {flag_info['entry_index']}")
            if 'context' in flag_info:
                print(f"   Context: {flag_info['context']}")
    else:
        print("\n❌ No flags found in the HAR file!")
    
    if session_tokens:
        print(f"\n🔑 SESSION TOKENS FOUND ({len(session_tokens)}):")
        print("-" * 40)
        for i, token_info in enumerate(session_tokens, 1):
            print(f"\n{i}. Session Token: {token_info['session_token']}")
            print(f"   URL: {token_info['url']}")
            print(f"   Entry Index: {token_info['entry_index']}")
    else:
        print("\n❌ No session tokens found!")
    
    print("\n" + "="*60)

def main():
    """Main function to run the CTF flag extractor"""
    
    print("🚀 CTF Week 8: Web Traffic Inspector - Flag Extractor")
    print("🎯 Mission: Find the hidden flag in session token")
    print("-" * 60)
    
    # Path to the HAR file
    har_file_path = "CTF-W8_large_captured_web_traffic.har"
    
    # Check if file exists
    try:
        with open(har_file_path, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"❌ HAR file not found: {har_file_path}")
        print("📥 Please make sure the HAR file is in the current directory")
        return
    
    # Analyze the HAR file
    flags_found, session_tokens = analyze_har_for_flags(har_file_path)
    
    # Display results
    display_results(flags_found, session_tokens)
    
    # Provide submission guidance
    if flags_found:
        print("🎉 SUCCESS! Flag(s) found!")
        print("📝 Submit the flag(s) found above to complete the CTF challenge.")
        
        # If there's a session token with flag, highlight it
        for flag_info in flags_found:
            if 'session_token' in str(flag_info):
                print(f"\n🔑 Session Token Flag: {flag_info['flag']}")
    else:
        print("🔍 No flags found. The file might need manual inspection.")
        print("💡 Try checking the session tokens manually or look for encoded data.")

if __name__ == "__main__":
    main()
