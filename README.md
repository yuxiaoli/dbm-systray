# db-systray

Database Tray Application

## Installation

```sh
# Create a virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install the package
pip install db-systray
```

## Usage

```sh
# View help
python app.py -h

usage: app.py [-h] [-c CONFIG] [-p PORTS PORTS]

Database Tray Application

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to the configuration file (default: configs/config.json)
  -p PORTS PORTS, --ports PORTS PORTS
                        available ports: <starting_port_number> <num_ports>
```

