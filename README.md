# Bot Commenting DU

A small Python script, `human_message_sender.py`, that types short messages into a text box on a website and clicks Send, over and over, the way a person would. It moves your real mouse and keyboard, so it works on any site without needing to know anything about the page.

**You do not need to know how to code.** Everything below is done by copying commands into the terminal. Nothing needs to be downloaded from a website by hand. Pick your operating system and go top to bottom.

---

## How to stop it (read this first)

- Press the **Esc** key at any time.
- Or click the terminal window and press **Enter**. This works even if Esc does not.
- Or fling your mouse into the **top-left corner** of the screen. That triggers a built-in emergency stop.

---

## Step 1 - Open the terminal

**Windows 10 / 11:** press the **Windows key**, type `PowerShell`, press Enter. A blue window opens.

**Mac:** press **Command + Space**, type `Terminal`, press Enter. A window opens.

For every step below, copy the block for your system, paste it into this window, and press Enter.

---

## Step 2 - Install Python from the terminal

Python is the program that runs the script. You install it once.

### Windows (PowerShell)

```
winget install -e --id Python.Python.3.13 --accept-package-agreements --accept-source-agreements
```

When it says `Successfully installed`, **close PowerShell and open it again** so it can find Python. Then check it worked:

```
py --version
```

You should see something like `Python 3.13.9`.

### Mac (Terminal)

```
curl -L -o ~/Downloads/python.pkg https://www.python.org/ftp/python/3.13.9/python-3.13.9-macos11.pkg
sudo installer -pkg ~/Downloads/python.pkg -target /
```

It will ask for your Mac password. Type it and press Enter (nothing shows on screen while you type, that is normal). When it says `The install was successful`, check it worked:

```
python3 --version
```

You should see `Python 3.13.9`.

---

## Step 3 - Download human_message_sender.py from GitHub

This pulls the script straight from this GitHub repo into a new folder called `bot-commenting-DU` in your Downloads, and moves you into it.

### Windows (PowerShell)

```
mkdir ~\Downloads\bot-commenting-DU -Force
cd ~\Downloads\bot-commenting-DU
Invoke-WebRequest -Uri https://raw.githubusercontent.com/edwardvth/bot-commenting-DU/main/human_message_sender.py -OutFile human_message_sender.py
```

### Mac (Terminal)

```
mkdir -p ~/Downloads/bot-commenting-DU
cd ~/Downloads/bot-commenting-DU
curl -L -o human_message_sender.py https://raw.githubusercontent.com/edwardvth/bot-commenting-DU/main/human_message_sender.py
```

Your terminal is now sitting inside the folder with the script. Stay there for every step below. Run the same commands again any time you want the latest version.

---

## Step 4 - Install the three helper packages

The script needs three small add-ons. One command installs all of them.

### Windows

```
py -m pip install pyautogui pynput pyperclip
```

### Mac

```
python3 -m pip install pyautogui pynput pyperclip
```

Wait until you see `Successfully installed ...`. It can take a minute. Warnings in yellow are fine; only red errors matter.

---

## Step 5 - Mac only: allow Terminal to control the mouse and keyboard

macOS blocks programs from clicking and typing until you give permission. The script checks for both permissions when it starts. If either is missing it pops up the macOS permission dialog, prints exactly what to turn on, and exits instead of running with a dead Esc key.

You can jump straight to the right settings pages from the terminal:

```
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
```

Turn the switch **on** for **Terminal**. If Terminal is not in the list, click **+**, go to Applications, then Utilities, and pick Terminal.

```
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ListenEvent"
```

This is **Input Monitoring**. Turn the switch **on** for **Terminal** here too.

Then **quit Terminal completely** (Command + Q), open it again, and go back into the folder:

```
cd ~/Downloads/bot-commenting-DU
```

Windows users skip this step.

---

## Step 6 - Run human_message_sender.py

1. Open the website in your browser. Put the browser window exactly where you want it and leave it there. **Do not move or resize the browser after this point.** The script remembers screen positions, not the page itself.
2. Switch back to your terminal and run:

   **Windows**
   ```
   py human_message_sender.py
   ```

   **Mac**
   ```
   python3 human_message_sender.py
   ```

3. Follow the prompts in the terminal:
   - Press Enter to begin.
   - Move your mouse so it is hovering over the **center of the text box** on the website, then press Enter in the terminal.
   - Move your mouse over the **center of the Send button**, then press Enter.
4. A 5-second countdown starts. Take your hands off the mouse and keyboard.
5. It will type a message, click Send, wait a few seconds, and repeat until you stop it with **Esc**, **Enter** in the terminal, or the top-left corner.

**Running it again later:** open the terminal, then

- Windows: `cd ~\Downloads\bot-commenting-DU` then `py human_message_sender.py`
- Mac: `cd ~/Downloads/bot-commenting-DU` then `python3 human_message_sender.py`

---

## Changing what it sends and how fast

Open the script in a text editor from the terminal:

- Windows: `notepad human_message_sender.py`
- Mac: `open -e human_message_sender.py`

Near the top you will see:

- `MESSAGES = [ ... ]` - the list it picks from. Add, remove, or change lines. Keep each one inside quotes with a comma after it.
- `MIN_BETWEEN_SUBMISSIONS` and `MAX_BETWEEN_SUBMISSIONS` - the shortest and longest wait, in seconds, between sends.
- `MIN_KEY_DELAY` and `MAX_KEY_DELAY` - how fast it types each character.

Save the file and run it again. Note that re-running the Step 3 download overwrites your changes with the GitHub version.

---

## If something goes wrong

**"winget is not recognized" (Windows)**
Update **App Installer** from the Microsoft Store, or run Windows Update, then open a new PowerShell and try Step 2 again.

**"py is not recognized" or the Microsoft Store opens (Windows)**
PowerShell was not reopened after installing Python. Close it, open a new one, and try again. Always use `py` rather than `python` in the commands.

**"pip is not recognized"**
Use the longer form shown in Step 4: `py -m pip ...` on Windows, `python3 -m pip ...` on Mac.

**"No module named pyautogui" (or pynput, or pyperclip)**
The packages were installed into a different copy of Python than the one running the script. Run the Step 4 install command again, using exactly the same first word you use to run the script (`py` on Windows, `python3` on Mac).

**"can't open file ... human_message_sender.py"**
You are not in the right folder. Run the `cd` line from Step 3, or redo all of Step 3.

**On Mac, Esc does not stop it**
Esc uses a system-wide keyboard hook that macOS only allows when Terminal has **Input Monitoring** turned on (Accessibility alone is not enough). Redo Step 5, then quit Terminal with Command + Q and open it again. In the meantime, click the terminal window and press Enter, which always works.

**On Mac the script runs but nothing gets clicked or typed**
Accessibility is off for Terminal. Redo Step 5, quit Terminal with Command + Q, open it again.

**It clicks the wrong spot**
The browser window moved or changed size after calibration. Stop it, put the browser back, run the script again and recalibrate. On Windows, if clicks are consistently off, set display scaling to 100% in Settings, then System, then Display.

**Emoji show up as blank or question marks**
Emoji are pasted through the clipboard, which needs `pyperclip`. Make sure the Step 4 install included it.

**It will not stop**
Fling the mouse hard into the very top-left corner of the screen. If all else fails, close the terminal window.
