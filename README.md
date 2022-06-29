# Bachelors Project

This is the code for my bachelors thesis from Vrije Universiteit Amsterdam

## Installation

Download [Vagrant](https://www.vagrantup.com/downloads)

Download [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

Clone [p4lang tutorials](https://github.com/p4lang/tutorials)

`git clone https://github.com/p4lang/tutorials`

Navitage to p4lang/tutorials/vm-ubuntu-20.04 with `cd tutorials/vm-ubuntu-20.04`

Run `vagrant up`, this should take about 20 minutes

Login with username p4 and password p4

Launch a terminal and install git

`sudo apt install git`

Clone this library

`git clone https://github.com/QuinnRutherford/BachelorsProject`

`cd BachelorsProject`

Install P4-Utils

`git clone https://github.com/nsg-ethz/p4-utils.git`

`cd p4-utils`

`sudo ./install.sh`

## Network topology
![Topology](https://user-images.githubusercontent.com/66821354/176452249-d5162585-0098-4e4b-8ec2-7b31584c1787.svg)


## Running Tests

### Starting the network

`sudo python3 network.py <delay p1> <delay p2> <delay p3>` (delay in seconds)

Open terminals on hosts

`xterm h1 h2`

This will open two separate terminals

h1's ip address is: `10.0.0.1`

h2's ip address is: `10.0.0.2`

run `sudo python3 rec_udp.py` on host 2

run `sudo python3 snd_udp.py <destination ip> '<message>' (optional)<path #>` on host 1

If no path is specified a packet will be sent over every path

Path p0 can be used to send network over fastest known path (must be set by controller first)

**Examples**

`sudo python3 snd_udp.py 10.0.0.2 'hello world' 1` will send hello world over to h2 over path 1

`sudo python3 snd_udp.py 10.0.0.2 'flood paths'` will send 'flood paths' over all paths

### Controller

The controller manages updating the fastest path

To launch the controller, start the network (see above), open another terminal and run

`sudo python3 controller.py`

The controller CLI should launch

Available commands are:

`set-fpath <path name>` to set the path used when path 0 is specified by snd_udp.py file

`fpath` to set path 0 to the fastes known path that the end host has recieved from

To have forwarding tables set to the fastest known path run:

`sudo python3 rec_udp.py` on host 2

`sudo python3 snd_udp.py 10.0.0.2 'flood paths'` on host 1

`fpath` as a CLI to the controller

Then all packets set over path 0 should follow the lowest latency path

The time displayed at the endhost should match that of the time displayed when sent over the path with the lowest delay


