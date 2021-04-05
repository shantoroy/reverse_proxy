# The Reverse Proxy
# Supports Python v3.*

# help sources:
# https://medium.com/customorchestrator/simple-reverse-proxy-server-using-flask-936087ce0afb
# https://github.com/MollardMichael/python-reverse-proxy/blob/master/proxy.py


# Import required modules
import socket
import _thread
import threading
import json
import sys
import time
import pandas as pd
import itertools


# Enable locking for a thread
print_lock = threading.Lock()

####################################################################
########################## Option Set Up ###########################
####################################################################

def option_check():
    # all available argument options
    avail_options = ["-port"]

    # receive user given options
    options = [opt for opt in sys.argv[1:] if opt.startswith("-")]

    # receive user given arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    # raise error if user given option is wrong
    for i in options:
        if i not in avail_options:
            raise SystemExit(f"Usage: {sys.argv[0]} -port <argument>...")

    # raise error if not all options or arguments are available
    if len(options) != 1 or len(args) != 1:
        raise SystemExit(f"Usage: {sys.argv[0]} -port <argument>...")

    return args


####################################################################
#################### Basic RP Server Functions #####################
####################################################################

def round_robin(iterable):
    return next(iterable)

# define the available table
column_names = ["type", "id", "privPolyId", "listenport"]
updated_available_server_table = pd.DataFrame(columns = column_names)

# define the packet switch table
# column_names = ["policy", "server_id", "connections"]
# server_info_table = pd.DataFrame(columns = column_names)

# create table of available servers
def available_server(msg):
    global updated_available_server_table
    global policy_table

    updated_available_server_table = updated_available_server_table.append(msg, ignore_index = True)
    policy_list = set(updated_available_server_table["privPolyId"].tolist())
    # print(policy_list)
    
    policy_table = {}
    for policy in policy_list:
        policy_table[policy] = itertools.cycle(set(updated_available_server_table\
                [updated_available_server_table["privPolyId"]==policy]["id"].tolist()))

    # print(policy_table)
    # for policy in policy_list:
    #     globals()['policy%s' % policy] = \
    #         updated_available_server_table[updated_available_server_table["privPolyId"]==policy]


    
# Establish connection with new client
def on_new_client(clientsocket,addr):
    while True:

        msg = clientsocket.recv(2048)
        if not msg:
            # lock released on exit
            print_lock.release()
            break
        
        json_msg = json.loads(msg.decode())

        if json_msg["type"] == "1":
            print ("Received setup message from server id", json_msg["id"], "privacy policy",\
                                json_msg["privPolyId"], "port", json_msg["listenport"])
            available_server(json_msg)

        # elif json_msg["type"] == "2":
        #     print ("Received a data message from server id", json_msg["srcid"],\
        #                                          "payload", json_msg["payload"])
        #     target_client_id = json_msg["destid"]


        elif json_msg["type"] == "0":
            print ('Received a message from client', json_msg["srcid"], \
                                            "payload", json_msg["payload"])
            policy = json_msg["privPoliId"]
            print(policy)
            target_host_id = round_robin(policy_table[policy])
            print(target_host_id)
            server_name = 'localhost'
            server_port = updated_available_server_table\
                                [updated_available_server_table["id"]==target_host_id]["listenport"]

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((server_name,server_port))

            print("Forwarding a data message to server id", target_host_id, \
                                                "payload", json_msg["payload"])
            server_socket.send(json.dumps(json_msg).encode())
            recv_msg = server_socket.recv(2048)
            recv_json_msg = json.loads(recv_msg.decode())
            print ("Received a data message from server id", recv_json_msg["srcid"],\
                                                 "payload", recv_json_msg["payload"])
            server_socket.close()

            clientsocket.send(json.dumps(recv_json_msg).encode())

        else:
            pass

    clientsocket.close()




                
####################################################################
########################## Main Function ###########################
####################################################################

if __name__ == "__main__":
    args = option_check()
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = int(args[0])              # Reserve a port for your service.
    print("Running the reverse proxy on port", port)

    # Binds to the port
    s.bind((host, port))     
    # Allow 10 clients to connect
    s.listen(100) 

    while True:
        c, addr = s.accept()     # Establish connection with client.
        # lock acquired by client
        print_lock.acquire()
        _thread.start_new_thread(on_new_client,(c,addr))
        
    s.close()