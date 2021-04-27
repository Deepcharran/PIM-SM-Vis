# Real-time Multicast Flow Visualization 

This project is aimed at Visually representing the real-time Multicast Flow in a network topology.

## Getting Started

### Prerequisites

* Git
* Python 3 
* Pip
* Flask
* InfluxDB
* InfluxDB Python Client

### Installing

Follow the links and steps below to install the prerequisites.

* [Git](https://git-scm.com/)
* [Python 3](https://www.python.org/downloads/) : Latest version preffered.
* Pip : comes pre-installed with latest python packages.
* To install flask enter the following command in your Terminal/Cmd.

```
pip install Flask
```
* [InfluxDB](https://portal.influxdata.com/downloads/) : We use version 1.8.4
* To install InfluxDB python client enter the following command in your Terminal/Cmd.

```
pip install influxdb
```


### Running 

To run this web-app run your influxdb server and go to this directory in your Terminal/Cmd and enter the following command:

```
python3 main.py
```
To run on localhost replace :

```
application.run(host='0.0.0.0', port=5001)
```
with

```
application.run(host='localhost', port=<your preferred port>)
```

### Example

#### Topology View
![topology](https://gitlab-sjc.cisco.com/aspanda/rtfv_mcast/blob/master/examples/topology.png)
#### PIM SSM FLOW
![ssmflow](https://gitlab-sjc.cisco.com/aspanda/rtfv_mcast/blob/master/examples/ssmflow.png)

## Deploying

Currently in development.

## Versioning

Currently in development. 

## Authors
* **Ashish Panda** - [View Gitlab](https://gitlab-sjc.cisco.com/aspanda)
* **Moksh Kant** - [View Gitlab](https://gitlab-sjc.cisco.com/mokant)
* **Deepcharran** - [View Gitlab](https://gitlab-sjc.cisco.com/deepcharran)
* **Sreelakshmi K Nair** - [View Gitlab](https://gitlab-sjc.cisco.com/sreelnai)

## License

Currently in development.

## Acknowledgments

Currently in development.