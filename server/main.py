import socket
from thread import *
from shttp import *
# Some parameter configurations
MAXNUM_WAITING = 5
SERVER_ADDR = ('127.0.0.1', 8998)


def run(index, connection):
    try:
        connection.settimeout(MAX_LATENCY)
        while True:
            buf = connection.recv(MAXSIZE_BUFF)
            if len(buf) == 0:
                break
            status_code, instr, item_info = request_parsing(buf)
            print("error:", status_code, " instr:", instr, " item_info: ", item_info)
            handler_mess = ""
            if status_code == 200: # request parsed successfully
                handler_mess, binary_data = handler(instr, item_info)

            send_mess = response_message(status_code=status_code, content=handler_mess)
            print("send_mess: \n", send_mess)

            if binary_data != None:
                connection.send(send_mess.encode(DEFAULT_ENCODING) + binary_data)
            else:
                connection.send(send_mess.encode(DEFAULT_ENCODING))
            print("sended!")

    except socket.timeout:
        print('time out')
    
    connection.close()


# Global variable
g_thread_pool = ThreadPoolManger(MAXNUM_WAITING)

if __name__ == "__main__":
    print("Server is starting...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Configure socket to bind the SERVER's IP address and port number
    sock.bind(SERVER_ADDR)

    # Setting the mAXimum of connections allowed (follow the *FIFO* rule)
    sock.listen(MAXNUM_WAITING)
    print( "Server is listenting port 8001, with max connection 5")

    # Poll the socket status circularly, waiting for access
 
    for index in range(MAXNUM_WAITING):
        client_conn, client_addr = sock.accept()
        # Create a new thread to handle this connection
        g_thread_pool.add_job(run, *(index, client_conn, ))

    # Close the connection
    sock.close()


