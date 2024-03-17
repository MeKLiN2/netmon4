import psutil
import time
import os
from colorama import Fore, Style

ACTIVE_CONNECTIONS = set()

def update_connections(output_file):
    global ACTIVE_CONNECTIONS
    
    # Get the current set of active connections
    new_active_connections = set()
    for conn in psutil.net_connections():
        if conn.raddr and conn.status == 'ESTABLISHED':
            ip_address = conn.raddr.ip
            new_active_connections.add(ip_address)
    
    # Find new connections
    new_connections = new_active_connections - ACTIVE_CONNECTIONS
    # Find removed connections
    removed_connections = ACTIVE_CONNECTIONS - new_active_connections

    # Update active connections set
    ACTIVE_CONNECTIONS = new_active_connections

    # Open the output file in append mode
    with open(output_file, 'a') as file:
        # Add new connections to the file with an asterisk marker
        for ip in new_connections:
            file.write(f"* {ip}\n")
        # Add removed connections to the file with a strikethrough marker
        for ip in removed_connections:
            file.write(f"~ {ip}\n")

def display_connections(output_file):
    # Clear the terminal before printing to avoid clutter
    os.system('cls' if os.name == 'nt' else 'clear')

    # Read and display the contents of the output file
    print(f"{Fore.YELLOW}Current Connections:\n{Style.RESET_ALL}")
    with open(output_file, 'r') as file:
        for line in file:
            # Highlight new connections in green and removed connections in red
            if line.startswith('*'):
                print(Fore.GREEN + line.strip() + Style.RESET_ALL)
            elif line.startswith('~'):
                print(Fore.RED + line.strip() + Style.RESET_ALL)
            else:
                print(line.strip())

    print("\n")

def monitor_connections(output_file, interval):
    while True:
        # Update the connections file
        update_connections(output_file)
        # Display the connections in the terminal
        display_connections(output_file)
        # Sleep for the specified interval
        time.sleep(interval)

if __name__ == "__main__":
    output_file = "connections.txt"

    # Initial monitoring interval
    interval = int(input("Enter the initial monitoring interval in seconds: "))

    # Start monitoring connections
    monitor_connections(output_file, interval)
