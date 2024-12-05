# dbm-systray

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

## Environment Configuration

The program will read the startup directory and look for a `.env` file. In the `.env` file, you can configure the following environment variables:

- `EDITOR`: Specify the editor to be used for editing configuration files.
- `SQLITE_BROWSER_EXE`: Specify the path to the SQLite browser executable.

