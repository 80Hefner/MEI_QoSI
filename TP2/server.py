import socket
import os
import time

MAX_CONNS = 3

def lat_and_jit_connection(conn):
    while True:
        try:
            data = conn.recv(1024)

            conn.sendall(os.urandom(1024))
        except:
            conn.close()
            break

def download_speed_connection(conn):
    while True:
        try:
            data = conn.recv(4)
            
            requested_bytes = int.from_bytes(data, "big")

            conn.sendall(os.urandom(requested_bytes))
        except:
            conn.close()
            break

def upload_speed_connection(conn):
    while True:
        data = conn.recv(4)
        
        try:
            msg = data.decode()
            if 'Q' in msg:
                break
            pass
        except:
            pass
        try:
            incoming_bytes = int.from_bytes(data, "big")
        
            data = conn.recv(incoming_bytes)

            conn.sendall(os.urandom(4))
        except:
            pass



if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("10.0.0.1", 8080))

    s.listen(3)
    
    # Latency and jitter connection
    conn, addr = s.accept()
    lat_and_jit_connection(conn)
    conn.close()

    # Download speed connection
    conn, addr = s.accept()
    download_speed_connection(conn)
    conn.close()

    # Upload speed connection
    #conn, addr = s.accept()
    #upload_speed_connection(conn)
    #conn.close()

