#!/bin/bash

osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python reverse_proxy.py -port 2100"
end tell'

sleep 2

osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python server.py -id 100 -pp 111 -listen 2105 -revproc 2100"
end tell'

osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python server.py -id 200 -pp 222 -listen 2110 -revproc 2100"
end tell'

osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python server.py -id 300 -pp 111 -listen 2115 -revproc 2100"
end tell'

osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python server.py -id 400 -pp 222 -listen 2120 -revproc 2100"
end tell'

sleep 2

osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python client.py -id 1 -revproc 2100 -pkt pktfiles/1.json"
end tell'
osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python client.py -id 2 -revproc 2100 -pkt pktfiles/2.json"
end tell'
osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python client.py -id 3 -revproc 2100 -pkt pktfiles/3.json"
end tell'
osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python client.py -id 4 -revproc 2100 -pkt pktfiles/4.json"
end tell'
osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python client.py -id 5 -revproc 2100 -pkt pktfiles/5.json"
end tell'
osascript -e 'tell app "Terminal"
    do script "cd ~/reverse_proxy && python client.py -id 6 -revproc 2100 -pkt pktfiles/6.json"
end tell'