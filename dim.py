import tkinter as tk
from screeninfo import get_monitors
import threading
from pynput import keyboard

open_windows = []  # List to keep track of open windows
should_close = False  # Flag to indicate when windows should close

def create_overlay(monitor):
    window = tk.Tk()
    window.title("Black Overlay")
    window.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
    window.configure(bg='black')
    window.overrideredirect(True)
    window.attributes('-topmost', True)
    window.focus_set()
    window.grab_set()

    # Main loop modified to check for closing condition
    while not should_close:
        window.update_idletasks()
        window.update()

    window.destroy()

def manage_overlays(target_monitor_names):
    global should_close
    if open_windows:
        # Set flag to close all windows
        should_close = True
        open_windows.clear()  # Clear list once windows are set to close
    else:
        should_close = False
        monitors = get_monitors()
        for monitor in monitors:
            if monitor.name in target_monitor_names:
                thread = threading.Thread(target=create_overlay, args=(monitor,))
                open_windows.append(thread)
                thread.start()
                
current_keys = set()  # Set to keep track of currently pressed keys

def on_press(key):
    current_keys.add(key)
    if all(k in current_keys for k in [
        keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.KeyCode.from_char('f')
    ]):
        print("Toggle Overlay")
        target_names = ['DP-3', 'DP-1', 'HDMI-A-1']  # Names of monitors to toggle overlays on
        manage_overlays(target_names)

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

def main():
    monitors = get_monitors()
    print("Available Monitors:")
    for index, monitor in enumerate(monitors):
        print(f"{index}: {monitor}")
    # Set up the listener to handle key press and release
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
