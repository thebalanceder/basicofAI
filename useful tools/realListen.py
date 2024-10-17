from pynput import keyboard

# Global variables
recording_file = None
keystrokes1 = ""
keystrokes2 = ""
keystrokes3 = ""
current_sequence = []
recording = False
file1_recording = False
file2_recording = False
file3_recording = False

# Define exit sequence
exit_sequence = ['r', keyboard.Key.backspace, 'r', keyboard.Key.backspace, 'r', keyboard.Key.backspace]

def on_press(key):
    global recording_file, keystrokes1, keystrokes2, keystrokes3
    global current_sequence, file1_recording, file2_recording, file3_recording

    try:
        char = key.char
    except AttributeError:
        char = None

    if char:
        current_sequence.append(char)
    else:
        current_sequence.append(key)

    # Handle start and stop sequences for keystrokes1.txt
    if current_sequence[-6:] == ['a', keyboard.Key.backspace, 'a', keyboard.Key.backspace, 'a', keyboard.Key.backspace]:
        file1_recording = True
        print("Started recording keystrokes1.txt")
        current_sequence.clear()
    elif current_sequence[-6:] == ['z', keyboard.Key.backspace, 'z', keyboard.Key.backspace, 'z', keyboard.Key.backspace]:
        file1_recording = False
        print("Stopped recording keystrokes1.txt")
        current_sequence.clear()

    # Handle start and stop sequences for keystrokes2.txt
    elif current_sequence[-6:] == ['s', keyboard.Key.backspace, 's', keyboard.Key.backspace, 's', keyboard.Key.backspace]:
        file2_recording = True
        print("Started recording keystrokes2.txt")
        current_sequence.clear()
    elif current_sequence[-6:] == ['x', keyboard.Key.backspace, 'x', keyboard.Key.backspace, 'x', keyboard.Key.backspace]:
        file2_recording = False
        print("Stopped recording keystrokes2.txt")
        current_sequence.clear()

    # Handle start and stop sequences for keystrokes3.txt
    elif current_sequence[-6:] == ['d', keyboard.Key.backspace, 'd', keyboard.Key.backspace, 'd', keyboard.Key.backspace]:
        file3_recording = True
        print("Started recording keystrokes3.txt")
        current_sequence.clear()
    elif current_sequence[-6:] == ['c', keyboard.Key.backspace, 'c', keyboard.Key.backspace, 'c', keyboard.Key.backspace]:
        file3_recording = False
        print("Stopped recording keystrokes3.txt")
        current_sequence.clear()

    # Handle exit sequence
    if current_sequence == exit_sequence:
        print("Exit sequence detected. Stopping program.")
        with open("keystrokes1.txt", "w") as file1:
            file1.write(keystrokes1)
        with open("keystrokes2.txt", "w") as file2:
            file2.write(keystrokes2)
        with open("keystrokes3.txt", "w") as file3:
            file3.write(keystrokes3)
        return False  # Stop the listener

    # Record keystrokes into appropriate file
    if file1_recording:
        if char:
            keystrokes1 += char
        else:
            if key == keyboard.Key.backspace:
                keystrokes1 += '[Key.backspace]'
    elif file2_recording:
        if char:
            keystrokes2 += char
        else:
            if key == keyboard.Key.backspace:
                keystrokes2 += '[Key.backspace]'
    elif file3_recording:
        if char:
            keystrokes3 += char
        else:
            if key == keyboard.Key.backspace:
                keystrokes3 += '[Key.backspace]'

def on_release(key):
    # Not used for exit sequence, handled in on_press
    pass

# Start the key listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

