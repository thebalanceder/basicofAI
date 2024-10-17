from pynput import keyboard

# Define the sequence we want to stop recording on
stop_sequence = ['e', keyboard.Key.backspace, 'n', keyboard.Key.backspace, 'd', keyboard.Key.backspace]
current_sequence = []

def on_press(key):
    global current_sequence
    
    try:
        char = key.char
    except AttributeError:
        # Handle special keys
        char = None

    # Append the pressed key to the current sequence
    if char:
        current_sequence.append(char)
    else:
        current_sequence.append(key)

    # Check if the current sequence matches the stop sequence
    if len(current_sequence) > len(stop_sequence):
        current_sequence.pop(0)

    if current_sequence == stop_sequence:
        # Stop the listener
        return False

    # Write the key to the file
    with open("keystrokes.txt", "a") as f:
        if char:
            f.write(char)
        else:
            f.write(f"[{key}]")

def on_release(key):
    pass

# Start the key listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
