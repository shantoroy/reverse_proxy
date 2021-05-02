
# Import required modules
import socket
import _thread
import threading
import hashlib
import json
import sys


# Enable locking for a thread
print_lock = threading.Lock()

####################################################################
########################## Option Set Up ###########################
####################################################################

def option_check():
    global args

    # all available argument options
    avail_options = ["-id", "-pp", "-listen", "-revproc"]

    # receive user given options
    options = [opt for opt in sys.argv[1:] if opt.startswith("-")]

    # receive user given arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    # raise error if user given option is wrong
    for i in options:
        if i not in avail_options:
            raise SystemExit(f"Usage: {sys.argv[0]} (-id & -pp & -listen & -revproc) <argument>...")

    # raise error if not all options or arguments are available
    if len(options) != 4 or len(args) != 4:
        raise SystemExit(f"Usage: {sys.argv[0]} (-id & -pp & -listen & -revproc) <argument>...")


####################################################################
###################### Basic Server Functions ######################
####################################################################

# after receiving each connection from reverse proxy/client
def on_new_client(clientsocket,addr):
    while True:

        msg = clientsocket.recv(2048)
        if not msg:
            # lock released on exit
            print_lock.release()
            break

        json_msg = json.loads(msg.decode())
        print("Received a message from client", json_msg["srcid"], "payload", json_msg["payload"])
        payload = json_msg["payload"]
        new_msg = hashlib.sha1()
        new_msg.update(payload.encode())
        hashed_payload = new_msg.hexdigest()
        new_json_msg = {"type":"2", "srcid": str(args[0]), "destid": json_msg["srcid"],\
                        "payloadsize": len(hashed_payload), "payload": hashed_payload}
        
        print("Sending a message to the client", new_json_msg["destid"], "payload", new_json_msg["payload"])
        clientsocket.send(json.dumps(new_json_msg).encode())
    clientsocket.close()


# Connect to the Reverse Proxy
def connect_reverse_proxy():
    new_json_msg = {"type":"1", "id": str(args[0]), "privPolyId": str(args[1]),\
                        "listenport": str(args[2])}
    # rev_proxy_name = 'reverseproxy.ddns.net'
    rev_proxy_name = '127.0.0.1'
    rev_proxy_port = int(args[3])

    rev_proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rev_proxy_socket.connect((rev_proxy_name, rev_proxy_port))

    rev_proxy_socket.send(json.dumps(new_json_msg).encode())
    rev_proxy_socket.close()



####################################################################
########################## Main Function ###########################
####################################################################

if __name__ == "__main__":
    option_check()
    s = socket.socket()         # Create a socket object
    host = '127.0.0.1' # Get local machine name
    port = int(args[2])              # Reserve a port for your service.


    print ("Server running with id", args[0])
    print ("Server serving privacy policy", args[1])
    print ("Listening on port", args[2])
    
    # Broadcast "Alive" status to the Reverse Proxy first
    connect_reverse_proxy()
    print ("Connecting to the reverse proxy on port", args[3])

    # Binds to the port
    s.bind((host, port))     
    # Allow 10 clients to connect
    s.listen(10)                 

    # Receive/Process each client connection in a seperate thread
    while True:
        c, addr = s.accept()     # Establish connection with client.
        # lock acquired by client
        print_lock.acquire()
        print ('Received a message from client', addr, "payload")
        _thread.start_new_thread(on_new_client,(c,addr))
        
    s.close()