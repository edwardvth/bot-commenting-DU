# Human-like Browser Message Sender

This Windows Python script controls your already-open browser using mouse and keyboard automation.

## What it does

- Lets you calibrate the position of the text box.
- Lets you calibrate the position of the red Send button.
- Randomly chooses a message from the list in the script.
- Types one character at a time with randomized delays.
- Adds occasional small "hesitation" pauses while typing.
- Clicks Send.
- Waits a random 5–10 seconds.
- Repeats until stopped.

## Stop controls

- Press **Esc** at any time.
- Or rapidly move your mouse to the **top-left corner** of the screen. PyAutoGUI's failsafe will stop the script.

## Installation

1. Install Python 3 for Windows if you do not already have it.
2. Open Command Prompt or PowerShell.
3. Run:

    pip install pyautogui pynput

## Run

Navigate to the folder containing the script and run:

    python human_message_sender.py

Then follow the calibration prompts.

## Important

Keep the browser window in the same position after calibration. Because this version uses screen coordinates rather than a URL or page-specific HTML selectors, moving or resizing the browser can cause it to click the wrong location.

To change the text it sends, edit the `MESSAGES` list near the top of `human_message_sender.py`.

To change the delay between submissions, edit:

    MIN_BETWEEN_SUBMISSIONS = 5.0
    MAX_BETWEEN_SUBMISSIONS = 10.0
