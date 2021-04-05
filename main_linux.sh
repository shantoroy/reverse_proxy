#!/bin/bash

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python reverse_proxy.py -port 2200; bash"

sleep 2

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python server.py -id 100 -pp 111 -listen 2105 -revproc 2200; bash"

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python server.py -id 200 -pp 222 -listen 2110 -revproc 2200; bash"

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python server.py -id 300 -pp 111 -listen 2115 -revproc 2200; bash"

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python server.py -id 400 -pp 222 -listen 2120 -revproc 2200; bash"


sleep 2

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python client.py -id 1 -revproc 2200 -pkt pktfiles/1.json; bash"

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python client.py -id 2 -revproc 2200 -pkt pktfiles/2.json; bash"

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python client.py -id 3 -revproc 2200 -pkt pktfiles/3.json; bash"

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python client.py -id 4 -revproc 2200 -pkt pktfiles/4.json; bash"

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python client.py -id 5 -revproc 2200 -pkt pktfiles/5.json; bash"

gnome-terminal -- /bin/bash -c "cd ~/reverse_proxy; python client.py -id 6 -revproc 2200 -pkt pktfiles/6.json; bash"

