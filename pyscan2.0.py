import socket
import time
import threading
from queue import Queue


def scan_ports():
    print("\nWelcome to the Advanced Port Scanner")
    print("======================================")

    # Set socket default timeout
    socket.setdefaulttimeout(0.55)

    # Thread lock for printing
    thread_lock = threading.Lock()

    # User Input
    target_IP = input("\nPlease enter the target IP Address: ")
    port_start = int(input("Please enter the target port to start: "))
    port_stop = int(input("Please enter the target port to stop: "))

    # Resolve hostname/IP
    try:
        t_ip = socket.gethostbyname(target_IP)
        print("\nScanning Host for open ports:", t_ip)
    except socket.gaierror:
        print("Invalid Host name. Please enter a valid IP or domain")
        return

    # Function to scan a port
    def portscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.55)
        try:
            s.connect((t_ip, port))
            s.close()
            with thread_lock:
                print(f"Port {port} is OPEN")
        except:
            pass  # Ignore closed ports

    # Thread worker function
    def threader():
        while True:
            worker = q.get()
            portscan(worker)
            q.task_done()

    # Create Queue for threading
    q = Queue()

    # Start timing
    startTime = time.time()

    # Create and start threads
    for _ in range(200):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    # Add ports to queue
    for worker in range(port_start, port_stop + 1):
        q.put(worker)

    # Wait until all threads complete
    q.join()

    # Calculate and print runtime
    runtime = time.time() - startTime
    print(f"\nRun Time: {runtime:.2f} seconds")


# Main loop to allow repeated scans
while True:
    scan_ports()
    choice = input("\nDo you want to scan another target? (yes/no): ").strip().lower()
    if choice != "yes":
        print("\nExiting the scanner. Have a great day!")
        break
