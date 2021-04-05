# Reverse Proxy in Python

## Basic Information
* Name - Shanto Roy
* PSID - 1894941
* Course - Computer Networks
* Assignment - Reverse Proxy with Loadbalancing (Round Robin)

## About
The Reverse Proxy keeps track of available servers, receives client data, forwards client data to servers
with corresponding privacy policy based on Round-Robin loadbalancing, receives processed data from servers, and returns the processed data to the clients. Each process is maintained using thread. The socket programming is done using python (version 3.x).


## Setup
1. clone the repository to your **home directory**
2. make sure python (3.x) is selected by default as python (virtual env is preferable)
3. Run `pip install -r requirements.txt `
4. run `./main.sh` in Mac terminal or `./main_linux` in a Linux terminal. Outputs are visible in several terminals.


## Examples
### Reverse Proxy
![plot](./screenshots/rev_proxy.png)

### Server
![plot](./screenshots/server.png)

### Client
![plot](./screenshots/client.png)


## Thanks to
* [Stack Overflow](https://stackoverflow.com/)
* [Github](https://github.com)
* Other random tutorials
