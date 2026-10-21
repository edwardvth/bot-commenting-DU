import sys
import time
import random
import threading

import pyautogui
import pyperclip
from pynput import keyboard

# ----------------------------
# Configuration
# ----------------------------

MESSAGES = [
    "🔥",
    "😎",
    "😍",
    "🙌",
    "💯",
    "👏",
    "🤩",
    "❤️",
    "🚀",
    "✨",
]

MIN_BETWEEN_SUBMISSIONS = 1.0
MAX_BETWEEN_SUBMISSIONS = 5.0

# Human-like typing speed in seconds between individual keypresses.
MIN_KEY_DELAY = 0.035
MAX_KEY_DELAY = 0.135

# Occasional slightly longer pause, as if a person hesitated while typing.
HESITATION_CHANCE = 0.055
MIN_HESITATION = 0.15
MAX_HESITATION = 0.55

# Brief pause after typing before clicking Send.
MIN_PRE_SEND_PAUSE = 0.25
MAX_PRE_SEND_PAUSE = 0.9

# Move mouse to the TOP-LEFT corner of the screen to trigger PyAutoGUI's failsafe.
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

# Mac uses Command for select-all / paste; Windows and Linux use Ctrl.
MOD_KEY = "command" if sys.platform == "darwin" else "ctrl"

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
    """Stop the loop when Esc is pressed."""
    if key == keyboard.Key.esc:
        print("\nEsc pressed — stopping.")
        stop_event.set()
        return False


def wait_for_enter(prompt):
    input(prompt)


def capture_mouse_position(label):
    print(f"\nMove your mouse over the {label}.")
    input("When the cursor is in the correct spot, press Enter here...")
    pos = pyautogui.position()
    print(f"Captured {label}: {pos}")
    return pos


def human_type(text):
    """Type text character-by-character with randomized timing."""
    for char in text:
        if stop_event.is_set():
            return

        # pyautogui.write only handles ASCII, so paste anything else (emojis).
        if char.isascii():
            pyautogui.write(char)
        else:
            pyperclip.copy(char)
            pyautogui.hotkey(MOD_KEY, "v")
        time.sleep(random.uniform(MIN_KEY_DELAY, MAX_KEY_DELAY))

        if random.random() < HESITATION_CHANCE:
            time.sleep(random.uniform(MIN_HESITATION, MAX_HESITATION))


def interruptible_sleep(seconds):
    """Sleep in small slices so Esc can stop quickly."""
    end = time.time() + seconds
    while time.time() < end:
        if stop_event.is_set():
            return False
        time.sleep(min(0.1, end - time.time()))
    return True


def main():
    print("=" * 60)
    print("Human-like Browser Message Sender")
    print("=" * 60)
    print(
        "\nSafety controls:\n"
        "  • Press Esc at any time to stop.\n"
        "  • Or click this terminal window and press Enter.\n"
        "  • Move the mouse to the TOP-LEFT corner to trigger the failsafe.\n"
        "  • Keep the target browser window visible and do not move/resize it\n"
        "    after calibration.\n"
    )

    if not _mac_permissions_ok():
        return

    wait_for_enter(
        "Open your website in the browser and position the window exactly how "
        "you want it. Press Enter to start calibration..."
    )

    textbox_pos = capture_mouse_position("CENTER of the text/comment box")
    send_pos = capture_mouse_position("CENTER of the red Send button")

    print("\nCalibration complete.")
    print(f"Text box: {textbox_pos}")
    print(f"Send button: {send_pos}")

    # Arm every stop path BEFORE the countdown so Esc works from the first second.
    listener = _start_esc_listener()
    threading.Thread(target=_stdin_stop_watcher, daemon=True).start()

    print("\nStarting in 5 seconds. Click nothing after this point.")
    print("Stop with Esc, or click this terminal and press Enter, or fling the mouse to the top-left corner.")
    for i in range(5, 0, -1):
        if stop_event.is_set():
            return
        print(i)
        time.sleep(1)

    sent_count = 0

    try:
        while not stop_event.is_set():
            message = random.choice(MESSAGES)

            # Click the text box.
            pyautogui.click(textbox_pos.x, textbox_pos.y)

            # Clear any text that might remain from a previous submission.
            pyautogui.hotkey(MOD_KEY, "a")
            pyautogui.press("backspace")

            # Type like a person.
            human_type(message)

            if stop_event.is_set():
                break

            if not interruptible_sleep(
                random.uniform(MIN_PRE_SEND_PAUSE, MAX_PRE_SEND_PAUSE)
            ):
                break

            # Click Send.
            pyautogui.click(send_pos.x, send_pos.y)
            sent_count += 1

            delay = random.uniform(
                MIN_BETWEEN_SUBMISSIONS,
                MAX_BETWEEN_SUBMISSIONS
            )

            print(
                f'[{sent_count}] Sent: "{message}" '
                f"— next in {delay:.1f}s"
            )

            if not interruptible_sleep(delay):
                break

    except pyautogui.FailSafeException:
        print("\nMouse moved to the top-left corner — failsafe triggered.")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt — stopping.")

    finally:
        stop_event.set()
        try:
            listener.stop()
        except Exception:
            pass
        print(f"\nStopped. Total submissions: {sent_count}")


if __name__ == "__main__":
    main()
