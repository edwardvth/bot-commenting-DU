import sys
import time
import threading
import pyautogui
from pynput import keyboard

BUTTON_DELAY = 0.5
START_DELAY = 3

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

stop_event = threading.Event()

def _mac_permissions_ok():
    """macOS only. Esc works through a global keyboard hook, and macOS silently
    disables that hook unless the terminal app has BOTH Accessibility and Input
    Monitoring permission. Ask for both up front and refuse to run without them,
    so the script never runs with a dead Esc key."""
    if sys.platform != "darwin":
        return True
    ok = True
    try:
        try:
            from ApplicationServices import AXIsProcessTrustedWithOptions, kAXTrustedCheckOptionPrompt
            trusted = AXIsProcessTrustedWithOptions({kAXTrustedCheckOptionPrompt: True})
        except ImportError:
            from ApplicationServices import AXIsProcessTrusted
            trusted = AXIsProcessTrusted()
        if not trusted:
            print("\n[!] macOS Accessibility permission is OFF for this terminal app.")
            ok = False
    except Exception as e:
        print(f"\n[!] Could not check Accessibility permission ({e}).")
    try:
        import Quartz
        if not Quartz.CGPreflightListenEventAccess():
            Quartz.CGRequestListenEventAccess()  # pops the Input Monitoring prompt
            if not Quartz.CGPreflightListenEventAccess():
                print("[!] macOS Input Monitoring permission is OFF for this terminal app. "
                      "The Esc key cannot work without it.")
                ok = False
    except Exception as e:
        print(f"[!] Could not check Input Monitoring permission ({e}).")
    if not ok:
        print(
            "\nFix it like this, then run the script again:\n"
            "  1. System Settings > Privacy & Security > Accessibility: turn ON Terminal.\n"
            "  2. System Settings > Privacy & Security > Input Monitoring: turn ON Terminal.\n"
            "  3. QUIT Terminal completely (Cmd+Q), open it again, cd back into this folder.\n"
        )
    return ok


def _stdin_stop_watcher():
    """Second stop path that needs no permissions: click the terminal window and
    press Enter. Started only after calibration so it does not eat those Enters."""
    try:
        for _ in sys.stdin:
            print("\nEnter pressed in the terminal - stopping.")
            stop_event.set()
            return
    except Exception:
        pass


def _start_esc_listener():
    """Start the global Esc hook and confirm it is actually alive."""
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    time.sleep(0.3)
    if not listener.is_alive():
        print("[!] The Esc listener did not start. Use Enter in the terminal or the "
              "top-left-corner failsafe to stop.")
    return listener

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
    print("\nStop with Esc, or click this terminal and press Enter.")
    print("Move the mouse to the TOP-LEFT corner for the PyAutoGUI failsafe.")

    if not _mac_permissions_ok():
        return

    input("\nOpen the page and position the browser. Press Enter to begin calibration...")

    button1 = capture_mouse_position("Button 1")
    button2 = capture_mouse_position("Button 2")

    print(f"\nButton 1: {button1}")
    print(f"Button 2: {button2}")

    listener = _start_esc_listener()
    threading.Thread(target=_stdin_stop_watcher, daemon=True).start()

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
