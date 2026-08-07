# Import required libraries
import socket
import threading
import time
import argparse

# Define a function to scan a single port
def scan_port(host, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout of 1 second
        sock.settimeout(1)
        # Try to connect to the host on the given port
        result = sock.connect_ex((host, port))
        # If the connection is successful, print the port as open
        if result == 0:
            print(f"Port {port} is open")
        # Close the socket
        sock.close()
    except Exception as e:
        # Print any exceptions that occur during the scan
        print(f"Error scanning port {port}: {e}")

# Define a function to perform a port scan
def port_scan(host, start_port, end_port):
    # Create a thread for each port to be scanned
    threads = []
    for port in range(start_port, end_port + 1):
        # Create a new thread for the current port
        thread = threading.Thread(target=scan_port, args=(host, port))
        # Start the thread
        thread.start()
        # Add the thread to the list of threads
        threads.append(thread)
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Define the main function
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Port Scanner Tool")
    parser.add_argument("-t", "--target", help="Target host to scan", required=True)
    parser.add_argument("-s", "--start", help="Starting port number", type=int, default=1)
    parser.add_argument("-e", "--end", help="Ending port number", type=int, default=65535)
    args = parser.parse_args()
    
    # Get the target host and port range from the command-line arguments
    host = args.target
    start_port = args.start
    end_port = args.end
    
    # Perform the port scan
    print(f"Scanning {host} from port {start_port} to {end_port}...")
    start_time = time.time()
    port_scan(host, start_port, end_port)
    end_time = time.time()
    print(f"Scan completed in {end_time - start_time} seconds")

# Run the main function
if __name__ == "__main__":
    main()