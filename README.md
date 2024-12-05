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

## Configuration File Format

The `config.json` file should be a JSON array where each element represents an entry with the following properties:

- `name` (string): The name of the resource.
- `path` (string): The file path to the resource (e.g., SQLite database or JSON file).

### JSON Schema for `config.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string"
      },
      "path": {
        "type": "string"
      }
    },
    "required": ["name", "path"],
    "additionalProperties": false
  }
}
```

## Environment Configuration

The program will read the starting directory and look for a `.env` file. In the `.env` file, you can configure the following environment variables:

1. `EDITOR` - Specifies the text editor to be used.
2. `SQLITE_BROWSER_EXE` - Path to the SQLite browser executable.
3. `SQLITE_WEB` - Configuration for the SQLite web server.
4. `LITECLI` - Path to the LiteCLI executable for interacting with SQLite databases.

