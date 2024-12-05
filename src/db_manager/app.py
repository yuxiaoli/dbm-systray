import os
import sys
import subprocess
from subprocess import CREATE_NEW_CONSOLE
from omegaconf import OmegaConf
import pystray
# from pystray import MenuItem as item
from pystray import MenuItem
from pystray import Menu
from PIL import Image, ImageDraw
import webbrowser
from dotenv import load_dotenv
import argparse
import platform

config_path = "configs/config.json"

if not os.path.exists(config_path):
    print(f"Config file not found at {config_path}")
    sys.exit(1)

# config = OmegaConf.load(config_path)

class AppState:
    def __init__(self, ports=list(range(8080, 8090))):
        self.server_processes = {}  # Map from file_path to process and port
        self.icon = None
        self.ports = ports

    def get_port(self) -> int:
        if (len(self.ports) == 0):
            return -1
        port = self.ports.pop()
        # port = self.ports.pop(0)
        return port

def run_command(command, file_path):
    try:
        subprocess.Popen([command, file_path], shell=True)
    except Exception as e:
        print(f"Error running command {command}: {e}")

def run_in_new_terminal(command, file_path):
    # print(file_path)
    # For Windows
    # command_line = f'{command} "{file_path}"'
    command_line = f'{command} {file_path}'
    # print(command_line)
    try:
        subprocess.Popen(['start', 'cmd', '/k', command_line], shell=True)
    except Exception as e:
        print(f"Error opening new terminal for command {command}: {e}")

def open_directory(file_path):
    directory = os.path.dirname(file_path)
    if os.path.exists(directory):
        os.startfile(directory)
    else:
        print(f"Directory {directory} does not exist")

def start_sqlite_web_server(file_path, app_state):
    if file_path in app_state.server_processes:
        print("Server is already running")
        return
    # Start the server in a new terminal
    port = app_state.get_port()
    if (port < 0):
        # raise Exception("No port available")
        print("No port available")
        return
    # For Windows
    # command_line = f'sqlite_web "{file_path}"'
    # command_line = f'sqlite_web {file_path}'
    try:
        # Start the sqlite_web server in a new console window
        sqlite_web = os.getenv('SQLITE_WEB')
        if not sqlite_web:
            sqlite_web = "sqlite_web"
        proc = subprocess.Popen([sqlite_web, "-p", str(port), file_path], creationflags=CREATE_NEW_CONSOLE)
        app_state.server_processes[file_path] = {
            "process": proc,
            "port": port
        }
        print(f"Started sqlite_web server for {file_path}")
    except Exception as e:
        print(f"Error starting sqlite_web server: {e}")

def stop_sqlite_web_server(file_path, app_state):
    if file_path not in app_state.server_processes:
        print("Server is not running")
        return
    proc = app_state.server_processes[file_path]["process"]
    port = app_state.server_processes[file_path]["port"]
    try:
        # Terminate the process
        proc.terminate()
        proc.wait()
        del app_state.server_processes[file_path]
        # Recycle the port
        app_state.ports.append(port)
        print(f"Stopped sqlite_web server for {file_path} on port {port}")
    except Exception as e:
        print(f"Error stopping sqlite_web server: {e}")

def generate_menu(db_name, file_path, app_state):
    # print(file_path)
    # ext = os.path.splitext(file_path)[1].lower()
    basename = os.path.basename(file_path)
    filename, extension = os.path.splitext(basename)
    ext = extension[1:].upper()
    if not db_name:
        db_name = f"{filename} [{ext}]"
    else:
        db_name += f" [{ext}]"
    ext = extension.lower()
    def submenu():
        menu_items = []
        if ext == '.sqlite':
            # Add options
            sqlite_browser = os.getenv('SQLITE_BROWSER_EXE')
            menu_items.append(MenuItem(
                # "Run SQLiteDatabaseBrowserPortable",
                "SQLite Browser",
                lambda: run_command(sqlite_browser, file_path)
            ))
            litecli = os.getenv('LITECLI')
            if not litecli:
                litecli = "litecli"
            menu_items.append(MenuItem(
                # "Open litecli",
                "LiteCli",
                lambda: run_in_new_terminal(litecli, file_path)
            ))
            # For sqlite_web server, we need to check if the server is running
            def start_server_action():
                start_sqlite_web_server(file_path, app_state)
                # app_state.icon.update_menu()
                # print(app_state.server_processes)
                app_state.icon.menu = create_menu(app_state)

            def stop_server_action():
                stop_sqlite_web_server(file_path, app_state)
                # app_state.icon.update_menu()
                app_state.icon.menu = create_menu(app_state)

            def open_web_page_action():
                webbrowser.open(f'http://127.0.0.1:{app_state.server_processes[file_path]["port"]}')

            # Create a submenu for sqlite-web server
            if file_path in app_state.server_processes:
                # Server is running
                sqlite_web_items = [
                    MenuItem("Stop server", stop_server_action),
                    # MenuItem("Go to Web page URL", open_web_page_action)
                    MenuItem("Web page", open_web_page_action)
                ]
            else:
                sqlite_web_items = [
                    # MenuItem("Start sqlite-web server", start_server_action)
                    MenuItem("Start server", start_server_action)
                ]

            menu_items.append(MenuItem(
                # "sqlite-web server",
                "sqlite-web",
                Menu(*sqlite_web_items)
            ))
            menu_items.append(MenuItem(
                "Open directory",
                lambda: open_directory(file_path)
            ))
        elif ext == '.json':
            editor = os.getenv('EDITOR')
            if not editor:
                if (platform.system() == "Windows"):
                    editor = "notepad"
            menu_items.append(MenuItem(
                # "Open in Notepad",
                "Edit...",
                lambda: run_command(editor, file_path)
            ))
            menu_items.append(MenuItem(
                "Open directory",
                lambda: open_directory(file_path)
            ))
        else:
            pass  # Do nothing
        return menu_items
    return MenuItem(db_name, Menu(*submenu()))

def quit(app_state) -> None:
    # Shut down all server processes
    print("Shutting down all server processes...")
    # print(app_state.server_processes)
    for file_path in list(app_state.server_processes.keys()):
        stop_sqlite_web_server(file_path, app_state)
    app_state.icon.stop()

def create_menu(app_state):
    config = OmegaConf.load(config_path)
    menu_items = []
    for item_config in config:
        db_name = item_config['name']
        file_path = item_config['path']
        menu_items.append(generate_menu(db_name, file_path, app_state))

    # Add Configuration submenu
    def reload_config() -> None:
        app_state.icon.menu = create_menu(app_state)

    editor = os.getenv('EDITOR')
    if not editor:
        if (platform.system() == "Windows"):
            editor = "notepad"
    config_submenu = Menu(
        MenuItem("Edit", lambda: run_command(editor, config_path)),
        MenuItem("Reload", reload_config)
    )
    menu_items.append(MenuItem('Configuration', config_submenu))

    # Add Quit option
    # menu_items.append(MenuItem('Quit', lambda: app_state.icon.stop()))
    menu_items.append(MenuItem('Quit', lambda: quit(app_state)))
    return menu_items

def create_image():
    # Get the absolute path of the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return Image.open(os.path.join(current_dir, "assets", "images", 'data-server.png'))
    # return Image.open(os.path.join(current_dir, "assets", "images", 'hard-disk.png'))

def main():
    parser = argparse.ArgumentParser(description="Database Tray Application")
    parser.add_argument('-c', '--config', default='configs/config.json',
                        help='path to the configuration file (default: configs/config.json)')
    parser.add_argument('-p', '--ports', type=int, nargs=2, default=(8080, 10),
                        help='available ports: <starting_port_number> <num_ports>')
    args = parser.parse_args()
    global config_path
    config_path = args.config
    if not os.path.exists(config_path):
        print(f"Config file not found at {config_path}")
        sys.exit(1)

    load_dotenv(override=True)  # take environment variables from .env.

    start_port, num_ports = args.ports
    app_state = AppState(ports=list(range(start_port, start_port + num_ports)))
    menu = create_menu(app_state)
    image = create_image()
    icon = pystray.Icon("db_icon", image, "Database Tray", menu=menu)
    app_state.icon = icon
    icon.run()

if __name__ == "__main__":
    main()
