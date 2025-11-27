"""
Utility functions for network infrastructure management
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any

def ensure_directory_exists(directory: str):
    """
    Ensure that a directory exists, create if it doesn't
    
    Args:
        directory: Path to directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"✓ Created directory: {directory}")

def save_to_json(data: Dict, filename: str):
    """
    Save data to JSON file
    
    Args:
        data: Dictionary to save
        filename: Output filename
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Data saved to: {filename}")
    except Exception as e:
        print(f"✗ Error saving to {filename}: {e}")

def load_from_json(filename: str) -> Dict:
    """
    Load data from JSON file
    
    Args:
        filename: Input filename
        
    Returns:
        Dictionary with loaded data
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        print(f"✓ Data loaded from: {filename}")
        return data
    except FileNotFoundError:
        print(f"⚠️  File not found: {filename}")
        return {}
    except Exception as e:
        print(f"✗ Error loading {filename}: {e}")
        return {}

def calculate_checksum(text: str) -> str:
    """
    Calculate MD5 checksum of text
    
    Args:
        text: Input text
        
    Returns:
        MD5 hash string
    """
    return hashlib.md5(text.encode()).hexdigest()

def format_timestamp(dt: datetime = None) -> str:
    """
    Format datetime as string
    
    Args:
        dt: Datetime object (uses current time if None)
        
    Returns:
        Formatted timestamp string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def validate_ip_address(ip: str) -> bool:
    """
    Validate IP address format
    
    Args:
        ip: IP address string
        
    Returns:
        True if valid, False otherwise
    """
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

def format_bytes(bytes_value: int) -> str:
    """
    Format bytes to human-readable string
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def print_banner(title: str, width: int = 70):
    """
    Print a formatted banner
    
    Args:
        title: Banner title
        width: Banner width in characters
    """
    print("=" * width)
    print(title.center(width))
    print("=" * width)

def print_section(title: str, width: int = 70):
    """
    Print a section header
    
    Args:
        title: Section title
        width: Width in characters
    """
    print(f"\n{title}")
    print("-" * width)

# Example usage
if __name__ == "__main__":
    print_banner("UTILITY FUNCTIONS TEST")
    
    # Test directory creation
    ensure_directory_exists("test_output")
    
    # Test JSON operations
    test_data = {"test": "data", "timestamp": format_timestamp()}
    save_to_json(test_data, "test_output/test.json")
    loaded_data = load_from_json("test_output/test.json")
    print(f"Loaded data: {loaded_data}")
    
    # Test IP validation
    test_ips = ["192.168.1.1", "256.1.1.1", "10.0.0.1"]
    for ip in test_ips:
        print(f"IP {ip} is {'valid' if validate_ip_address(ip) else 'invalid'}")
    
    # Test byte formatting
    print(f"Bytes formatted: {format_bytes(1536000)}")
  print("\n✓ All tests completed")
