from pynput import keyboard
import time
import threading

# Global variables
typing_enabled = False
exit_sequence = ['e', keyboard.Key.backspace, 'n', keyboard.Key.backspace, 'd', keyboard.Key.backspace]
current_sequence = []
shift_count = 0
ctrl_count = 0
keystrokes = ""

# Load keystrokes from file
def load_keystrokes(filename):
    global keystrokes
    with open(filename, "r") as file:
        keystrokes = file.read()

def simulate_keystrokes():
    global typing_enabled
    controller = keyboard.Controller()

    def press_key(key):
        if isinstance(key, str):
            # Normal character
            controller.press(key)
            controller.release(key)
        else:
            # Special key
            controller.press(key)
            controller.release(key)

    i = 0
    while i < len(keystrokes):
        if typing_enabled:
            char = keystrokes[i]

            if char == '\n':
                time.sleep(0.1)  # Small delay to simulate typing speed
            elif char == '[':
                # Handle special keys (e.g., [Key.backspace])
                end_index = keystrokes.find(']', i)
                if end_index != -1:
                    key_str = keystrokes[i+1:end_index]
                    if key_str == 'Key.backspace':
                        press_key(keyboard.Key.backspace)
                    elif key_str == 'Key.enter':
                        press_key(keyboard.Key.enter)
                    # Add more special keys if needed
                    i = end_index
            else:
                press_key(char)
            
            i += 1
            time.sleep(0.1)  # Small delay to simulate typing speed
        else:
            break

def on_press(key):
    global typing_enabled, current_sequence, shift_count, ctrl_count

    try:
        char = key.char
    except AttributeError:
        char = None

    # Handle Shift + Shift + Shift to start typing
    if key == keyboard.Key.shift:
        shift_count += 1
        if shift_count == 3:
            typing_enabled = True
            print("Typing enabled")
            shift_count = 0
            # Trigger keystroke simulation in a new thread
            threading.Thread(target=simulate_keystrokes).start()
    else:
        shift_count = 0

    # Handle Ctrl + Ctrl + Ctrl to stop typing
    if key == keyboard.Key.ctrl:
        ctrl_count += 1
        if ctrl_count == 3:
            print("Typing disabled")
            typing_enabled = False
            return False  # Stop the listener
    else:
        ctrl_count = 0

    # Track the exit sequence (e + backspace + n + backspace + d + backspace)
    if char:
        current_sequence.append(char)
    else:
        current_sequence.append(key)

    if len(current_sequence) > len(exit_sequence):
        current_sequence.pop(0)

    if current_sequence == exit_sequence:
        print("Exit sequence detected. Stopping.")
        typing_enabled = False
        return False  # Stop the listener

def on_release(key):
    pass  # No need to handle key release

# Load keystrokes file
load_keystrokes("keystrokes.txt")

# Start the key listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

