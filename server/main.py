import socket
import threading
from multiprocessing.pool import ThreadPool
from thread import *
from shttp import *
# Some parameter configurations
MAXNUM_WAITING = 1000
MAXNUM_THREAD = 2
SERVER_ADDR = ('127.0.0.1', 8998)
MAX_LATENCY = 100

def run(index, connection):
    try:
        connection.settimeout(MAX_LATENCY)
        while True:
            buf = connection.recv(MAXSIZE_BUFF)
            if len(buf) == 0:
                break
            print("Just received from {}th connection:\n".format(index), buf[:min(len(buf), 150)], "...")
            status_code, instr, item_info = request_parsing(buf)

            if status_code == 200: # request parsed successfully
                error, item_info = handler(instr, item_info)
            if error != None:
                status_code = ERROR_DICT[error]
            send_mess = response_message(status_code=status_code, item_info=item_info)
            print("Soon-to-be sent:\n", send_mess[:min(len(send_mess), 150)], "...")

            connection.send(send_mess)
            print("Sent successfully!")

    except socket.timeout:
        print('time out')
    
    connection.close()
    print("{}th connection closed.".format(index))



# Global variable
g_thread_pool = ThreadPoolManger(MAXNUM_THREAD)

if __name__ == "__main__":
    print("Server is starting...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Configure socket to bind the SERVER's IP address and port number
    sock.bind(SERVER_ADDR)

    # Setting the mAXimum of connections allowed (follow the *FIFO* rule)
    sock.listen(MAXNUM_WAITING)
    print( "Server is listenting {}, with max connection {}".format(SERVER_ADDR, MAXNUM_WAITING))

    # Poll the socket status circularly, waiting for access
 
    for index in range(1, MAXNUM_WAITING + 1):
        client_conn, client_addr = sock.accept()
        print("Connected to the {}th client".format(index))
        # Create a new thread to handle this connection
        g_thread_pool.add_job(run, *(index, client_conn, ))
    # Close the connection
    sock.close()


