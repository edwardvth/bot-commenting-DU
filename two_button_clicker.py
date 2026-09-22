import time
import threading
import pyautogui
from pynput import keyboard

BUTTON_DELAY = 0.5
START_DELAY = 3

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

stop_event = threading.Event()

def on_press(key):
    if key == keyboard.Key.esc:
        print("\nEsc pressed - stopping.")
        stop_event.set()
        return False

def capture_mouse_position(label):
    print(f"\nMove your mouse over the CENTER of {label}.")
    input("Press Enter when the cursor is in the correct spot...")
    pos = pyautogui.position()
    print(f"Captured {label}: {pos}")
    return pos

def interruptible_sleep(seconds):
    end = time.time() + seconds
    while time.time() < end:
        if stop_event.is_set():
            return False
        time.sleep(min(0.05, end - time.time()))
    return True

def main():
    print("=" * 55)
    print("Two-Button Coordinate Clicker")
    print("=" * 55)
    print("\nPress Esc to stop.")
    print("Move the mouse to the TOP-LEFT corner for the PyAutoGUI failsafe.")

    input("\nOpen the page and position the browser. Press Enter to begin calibration...")

    button1 = capture_mouse_position("Button 1")
    button2 = capture_mouse_position("Button 2")

    print(f"\nButton 1: {button1}")
    print(f"Button 2: {button2}")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    print(f"\nStarting in {START_DELAY} seconds...")
    for i in range(START_DELAY, 0, -1):
        if stop_event.is_set():
            return
        print(i)
        time.sleep(1)

    cycle_count = 0

    try:
        while not stop_event.is_set():
            pyautogui.click(button1.x, button1.y)

            if not interruptible_sleep(BUTTON_DELAY):
                break

            pyautogui.click(button2.x, button2.y)

            cycle_count += 1
            print(f"Completed cycle {cycle_count}")

    except pyautogui.FailSafeException:
        print("\nTop-left failsafe triggered.")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt - stopping.")
    finally:
        stop_event.set()
        try:
            listener.stop()
        except Exception:
            pass
        print(f"\nStopped. Total cycles: {cycle_count}")

if __name__ == "__main__":
    main()
