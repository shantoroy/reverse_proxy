# Import required modules
import socket 
import hashlib
import json
import sys


####################################################################
########################## Option Set Up ###########################
####################################################################

def option_check():
    global args 

    # all available argument options
    avail_options = ["-id", "-revproc", "-pkt"]

    # receive user given options
    options = [opt for opt in sys.argv[1:] if opt.startswith("-")]

    # receive user given arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    # raise error if user given option is wrong
    for i in options:
        if i not in avail_options:
            raise SystemExit(f"Usage: {sys.argv[0]} (-id & -revproc & -pkt) <argument>...")

    # raise error if not all options or arguments are available
    if len(options) != 3 or len(args) != 3:
        raise SystemExit(f"Usage: {sys.argv[0]} (-id & -revproc & -pkt) <argument>...")


####################################################################
###################### Basic Client Functions ######################
####################################################################

def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


####################################################################
########################## Main Function ###########################
####################################################################

if __name__ == "__main__":
    option_check()
    server_name = 'localhost'
    server_port = int(args[1])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_name,server_port))

    # Use while loop for continuous connection
    # while True:
    with open(args[2]) as f:
        send_msg = json.load(f)
    print("Sending message", send_msg["payload"], "to privacy policy", send_msg["privPoliId"],\
                        "through reverse proxy running on port", args[1])
    client_socket.send(json.dumps(send_msg).encode())
    recv_msg = client_socket.recv(2048).decode()
    recv_msg = json.loads(recv_msg)
    # print (">> ", recv_msg)
    hashed_sent = hashlib.sha1(send_msg["payload"].encode()).hexdigest()
    print ("Receiving a response from the server payload:", recv_msg["payload"])

    if hashed_sent == recv_msg["payload"]:
        print ("Hash of payload is correct")
    else:
        print ("Hash of payload is not correct")

    # if(send_msg == 'q'):
    #     client_socket.close()