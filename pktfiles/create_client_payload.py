#!/usr/bin/env python3

import json
import random

def client_message(client_id, policy_list):
    data = {
                "type": "0",         
                "srcid": str(client_id),      
                "privPoliId": random.choice(policy_list),   
                "payload": "xyz" + str(client_id)
            }
    
    file_name = "pktfiles/" + str(client_id) + ".json"
    with open(file_name, "w") as write_file:
        json.dump(data, write_file)

def main():
    number_of_clients = 15
    policy_list = ["111", "222"]
    for client_id in range(number_of_clients):
        client_message(client_id, policy_list)


if __name__ == "__main__":
    main()
