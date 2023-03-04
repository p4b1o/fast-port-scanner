import socket
import sys
import threading
import time

def check_port(host, port, timeout, open_ports):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout/1000.0)
    try:
        s.connect((host, port))
        open_ports.append(port)
    except socket.timeout:
        pass
    except:
        pass
    finally:
        s.close()

def check_ports(host, port_range, timeout, max_threads):
    open_ports = []
    start, end = map(int, port_range.split('-'))
    threads = []
    for port in range(start, end+1):
        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []
        t = threading.Thread(target=check_port, args=(host, port, timeout, open_ports))
        t.start()
        threads.append(t)
        print "scanning port %d" % port
    for t in threads:
        t.join()
    return open_ports

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "USE: python check_ports.py host port_range timeout_ms max_threads"
        sys.exit(1)

    host = sys.argv[1]
    port_range = sys.argv[2]
    timeout = int(sys.argv[3])
    max_threads = int(sys.argv[4])

    start_time = time.time()
    open_ports = check_ports(host, port_range, timeout, max_threads)
    end_time = time.time()
    execution_time = end_time - start_time

    if open_ports:
        print "Opened ports: %s" % open_ports
    else:
        print "No ports open"

    print "Time: %.2f seconds" % execution_time
