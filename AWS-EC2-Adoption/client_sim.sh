#!/bin/bash


osascript -e 'tell app "Terminal"
    do script "cd ~/HW3 && python client.py -id 1 -revproc 8000 -pkt pktfiles/1.json"
end tell'

sleep 1

osascript -e 'tell app "Terminal"
    do script "cd ~/HW3 && python client.py -id 2 -revproc 8000 -pkt pktfiles/2.json"
end tell'

sleep 1

osascript -e 'tell app "Terminal"
    do script "cd ~/HW3 && python client.py -id 3 -revproc 8000 -pkt pktfiles/1.json"
end tell'

sleep 1

osascript -e 'tell app "Terminal"
    do script "cd ~/HW3 && python client.py -id 4 -revproc 8000 -pkt pktfiles/2.json"
end tell'

sleep 1

osascript -e 'tell app "Terminal"
    do script "cd ~/HW3 && python client.py -id 5 -revproc 8000 -pkt pktfiles/1.json"
end tell'

sleep 1

osascript -e 'tell app "Terminal"
    do script "cd ~/HW3 && python client.py -id 6 -revproc 8000 -pkt pktfiles/2.json"
end tell'
