from operator import le
import socket
from sys import _clear_type_cache
import time
import os

TEST_TIME = 5  #seconds
INITIAL_CHUNK_SIZE = 1024  #bytes
MAX_CHUNK_SIZE = 8192 * 8192  #bytes

def measure_upload():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.0.1", 8080))

    increment_value = 2

    chunk_size = INITIAL_CHUNK_SIZE
    total_data_sent = 0
    t_end = time.time() + TEST_TIME

    while time.time() < t_end:
        t_sent = time.time()
        s.sendall(chunk_size.to_bytes(4, byteorder="big"))
        s.sendall(os.urandom(chunk_size))
        data = s.recv(4)
        t_recv = time.time()

        total_data_sent += chunk_size + 4
        
        if t_recv-t_sent < 1 and chunk_size < MAX_CHUNK_SIZE:
            chunk_size = chunk_size * increment_value
            chunk_size = int(chunk_size)
            if chunk_size > MAX_CHUNK_SIZE:
                chunk_size = MAX_CHUNK_SIZE
        else:
            chunk_size = chunk_size/increment_value
            chunk_size = int(chunk_size)
            increment_value = increment_value/2
    
    leave = 'Q'
    s.sendall(leave.encode())
    s.close()

    upload_speed = total_data_sent / TEST_TIME

    print("Upload speed: {0:.0f} B/s".format(upload_speed))


def measure_download():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.0.1", 8080))

    increment_value=2

    chunk_size = INITIAL_CHUNK_SIZE
    total_data_recv = 0
    t_end = time.time() + TEST_TIME

    while time.time() < t_end:
        t_sent = time.time()
        s.sendall(chunk_size.to_bytes(4, byteorder="big"))

        s.recv(chunk_size)
        t_recv = time.time()

        total_data_recv += chunk_size

        if (t_recv-t_sent < 1.1 or t_recv-t_sent > 0.9) and chunk_size < MAX_CHUNK_SIZE:
            chunk_size = chunk_size * increment_value
            chunk_size = int(chunk_size)
            if chunk_size > MAX_CHUNK_SIZE:
                chunk_size = MAX_CHUNK_SIZE
        else:
            chunk_size = chunk_size/increment_value
            chunk_size = int(chunk_size)
            increment_value = increment_value-0.1
    
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    
    download_speed = total_data_recv / TEST_TIME

    print("Download speed: {0:.0f} B/s".format(download_speed))

def measure_latency_and_jitter():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.0.1", 8080))

    lats = []
    jits = []
    last_lat = -1

    t_end = time.time() + TEST_TIME
    
    while time.time() < t_end:
        # Send packet
        t_sent = time.time()
        s.sendall(os.urandom(1024))

        # Receive packet
        s.recv(1024)
        t_recv = time.time()

        # Calculate latency
        lat = t_recv - t_sent
        lats.append(lat)

        # Calculate jitter
        if last_lat != -1:
            jit = abs(lat - last_lat)
            jits.append(jit)
        
        # Atualize last latency
        last_lat = lat
    
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    
    latency = sum(lats) / len(lats)
    jitter = sum(jits) / len(jits)

    print("Latency: {0:.3f}s".format(latency))
    print("Jitter: {0:.3f}s".format(jitter))


if __name__ == "__main__":

    measure_latency_and_jitter()
    print("------------------")
    measure_download()
    #print("------------------")
    #measure_upload()
