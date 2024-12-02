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

config_path = "configs/config.json"

if not os.path.exists(config_path):
    print(f"Config file not found at {config_path}")
    sys.exit(1)

config = OmegaConf.load(config_path)

class AppState:
    def __init__(self):
        self.server_processes = {}  # Map from file_path to process
        self.icon = None

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
    # For Windows
    # command_line = f'sqlite_web "{file_path}"'
    command_line = f'sqlite_web {file_path}'
    try:
        # Start the sqlite_web server in a new console window
        proc = subprocess.Popen(['sqlite_web', file_path], creationflags=CREATE_NEW_CONSOLE)
        app_state.server_processes[file_path] = proc
        print(f"Started sqlite_web server for {file_path}")
    except Exception as e:
        print(f"Error starting sqlite_web server: {e}")

def stop_sqlite_web_server(file_path, app_state):
    if file_path not in app_state.server_processes:
        print("Server is not running")
        return
    proc = app_state.server_processes[file_path]
    try:
        # Terminate the process
        proc.terminate()
        proc.wait()
        del app_state.server_processes[file_path]
        print(f"Stopped sqlite_web server for {file_path}")
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
            menu_items.append(MenuItem(
                # "Open litecli",
                "LiteCli",
                lambda: run_in_new_terminal('litecli', file_path)
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
                webbrowser.open('http://127.0.0.1:8080')  # Assuming default port

            # Create a submenu for sqlite-web server
            if file_path in app_state.server_processes:
                # Server is running
                sqlite_web_items = [
                    MenuItem("Stop server", stop_server_action),
                    MenuItem("Go to Web page URL", open_web_page_action)
                ]
            else:
                sqlite_web_items = [
                    MenuItem("Start sqlite-web server", start_server_action)
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

def create_menu(app_state):
    menu_items = []
    for item_config in config:
        db_name = item_config['db_name']
        file_path = item_config['file_path']
        menu_items.append(generate_menu(db_name, file_path, app_state))
    menu_items.append(MenuItem('Quit', lambda: app_state.icon.stop()))
    return menu_items

def create_image():
    # Get the absolute path of the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return Image.open(os.path.join(current_dir, "assets", "images", 'application.png'))

def main():
    load_dotenv(override=True)  # take environment variables from .env.
    app_state = AppState()
    menu = create_menu(app_state)
    image = create_image()
    icon = pystray.Icon("db_icon", image, "Database Tray", menu=menu)
    app_state.icon = icon
    icon.run()

if __name__ == "__main__":
    main()
