"""
Network Monitoring System
Monitors network device health and performance
"""

import logging
import socket
import time
from datetime import datetime
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logs/network_monitor.log'
)

class NetworkMonitor:
    """
    Monitors network devices and reports status
    """
    
    def __init__(self, devices: List[str]):
        """
        Initialize monitor with list of device IPs
        
        Args:
            devices: List of device IP addresses to monitor
        """
        self.devices = devices
        self.status_history = {}
        logging.info("NetworkMonitor initialized")
    
    def check_device_status(self, device_ip: str, port: int = 22) -> bool:
        """
        Check if a device is reachable
        
        Args:
            device_ip: IP address of the device
            port: Port to check (default SSH port 22)
            
        Returns:
            True if device is reachable, False otherwise
        """
        try:
            # Attempt to connect to device
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((device_ip, port))
            sock.close()
            
            status = result == 0
            
            if status:
                logging.info(f"Device {device_ip} is UP")
            else:
                logging.warning(f"Device {device_ip} is DOWN")
            
            return status
            
        except Exception as e:
            logging.error(f"Error checking device {device_ip}: {e}")
            return False
    
    def monitor_all_devices(self) -> Dict[str, bool]:
        """
        Monitor all devices and return status
        
        Returns:
            Dictionary mapping device IPs to their status
        """
        status_report = {}
        
        print("\n" + "=" * 50)
        print(f"Network Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        for device_ip in self.devices:
            status = self.check_device_status(device_ip)
            status_report[device_ip] = status
            
            # Display status with color
            status_symbol = "✓" if status else "✗"
            status_text = "UP" if status else "DOWN"
            print(f"{status_symbol} {device_ip:15} - {status_text}")
        
        # Calculate uptime percentage
        total_devices = len(self.devices)
        up_devices = sum(status_report.values())
        uptime_percentage = (up_devices / total_devices * 100) if total_devices > 0 else 0
        
        print("=" * 50)
        print(f"Network Uptime: {uptime_percentage:.1f}% ({up_devices}/{total_devices} devices up)")
        print("=" * 50 + "\n")
        
        return status_report
    
    def continuous_monitoring(self, interval: int = 60):
        """
        Continuously monitor devices at specified interval
        
        Args:
            interval: Monitoring interval in seconds
        """
        logging.info(f"Starting continuous monitoring (interval: {interval}s)")
        print(f"Starting continuous network monitoring...")
        print(f"Monitoring interval: {interval} seconds")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.monitor_all_devices()
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
            logging.info("Monitoring stopped by user")

def main():
    """
    Main entry point for the monitoring script
    """
    # Example devices to monitor (replace with actual IPs)
    devices = [
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.10",
        "8.8.8.8",  # Google DNS for testing
    ]
    
    monitor = NetworkMonitor(devices)
    
    # Run continuous monitoring
    monitor.continuous_monitoring(interval=30)

if __name__ == "__main__":
    main()
