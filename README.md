# PySocketCAN
The ```pysocketcan``` module provides a class to quickly modify Linux SocketCAN parameters directly from Python.

For example, to change the baudrate in Linux you need to run
```bash
$ sudo ip link set can0 down
$ sudo ip link set can0 type can bitrate 250000
$ sudo ip link set can0 up
```
The  ```pysocketcan``` equivalent is
```python
>>> can0.baud = 250000
```



## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install

```bash
$ pip install pysocketcan
```

## Usage

```python
import pysocket as pysc

>>> pysc.view_available() # returns available interfaces
'can0'
>>> can0 = pysc.Interface("can0") # instantiate interface object

>>> can0.on() # set interface up
>>> can0.off() # set interface down
>>> can0.state # returns current state of interface
'STOPPED'

>>> can0.baud = 250000 # sets the baudrate
>>> can0.baud # returns current baudrate
'250000'

>>> can0.status # returns currently active modes
'LOOPBACK,LISTEN-ONLY,TRIPLE-SAMPLING'
>>> can0.listen_only = False # turns mode off
>>> can0.status
'LOOPBACK,TRIPLE-SAMPLING'
```
If can-utils is installed you can also use
```python
>>> can0.receive() # returns bus message
>>> can0.send(100, 12345678) # adds message to bus
```
#### Note:
To function correctly Python needs root priveleges
```bash
$ sudo python3
     # or
$ sudo venv/bin/python3
```
## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
