from pynput import keyboard
import time
import threading

# Global variables
typing_enabled = False
exit_sequence = ['r', keyboard.Key.backspace, 'r', keyboard.Key.backspace, 'r', keyboard.Key.backspace]
q_sequence = ['q', keyboard.Key.backspace, 'q', keyboard.Key.backspace, 'q', keyboard.Key.backspace]
w_sequence = ['w', keyboard.Key.backspace, 'w', keyboard.Key.backspace, 'w', keyboard.Key.backspace]
e_sequence = ['e', keyboard.Key.backspace, 'e', keyboard.Key.backspace, 'e', keyboard.Key.backspace]
current_sequence = []
keystrokes1 = ""
keystrokes2 = ""
keystrokes3 = ""

# Load keystrokes from files
def load_keystrokes():
    global keystrokes1, keystrokes2, keystrokes3
    with open("keystrokes1.txt", "r") as file1:
        keystrokes1 = file1.read()
    with open("keystrokes2.txt", "r") as file2:
        keystrokes2 = file2.read()
    with open("keystrokes3.txt", "r") as file3:
        keystrokes3 = file3.read()

def simulate_keystrokes(keystrokes):
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
                # Add more special keys here if needed
                i = end_index
        else:
            press_key(char)
        
        i += 1
        time.sleep(0.1)  # Small delay to simulate typing speed

def on_press(key):
    global typing_enabled, current_sequence

    try:
        char = key.char
    except AttributeError:
        char = None

    # Track key presses
    if char:
        current_sequence.append(char)
    else:
        current_sequence.append(key)

    if len(current_sequence) > len(exit_sequence):
        current_sequence.pop(0)

    # Handle q + backspace + q + backspace + q + backspace to type from the first file
    if current_sequence == q_sequence:
        print("Typing from first keystroke file")
        threading.Thread(target=simulate_keystrokes, args=(keystrokes1,)).start()

    # Handle w + backspace + w + backspace + w + backspace to type from the second file
    elif current_sequence == w_sequence:
        print("Typing from second keystroke file")
        threading.Thread(target=simulate_keystrokes, args=(keystrokes2,)).start()

    # Handle e + backspace + e + backspace + e + backspace to type from the third file
    elif current_sequence == e_sequence:
        print("Typing from third keystroke file")
        threading.Thread(target=simulate_keystrokes, args=(keystrokes3,)).start()

    # Handle r + backspace + r + backspace + r + backspace to exit the program
    elif current_sequence == exit_sequence:
        print("Exit sequence detected. Stopping program.")
        return False  # Stop the listener and exit

def on_release(key):
    pass  # No need to handle key release

# Load keystrokes files
load_keystrokes()

# Start the key listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

