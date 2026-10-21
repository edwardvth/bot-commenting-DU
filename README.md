# Bot Commenting DU

A small Python script that types short messages into a text box on a website and clicks Send, over and over, the way a person would. It moves your real mouse and keyboard, so it works on any site without needing to know anything about the page.

Two scripts are included:

- `human_message_sender.py` - types a random message from a list, clicks Send, waits a few seconds, repeats.
- `two_button_clicker.py` - clicks two spots on the screen back and forth.

**You do not need to know how to code.** These steps assume a fresh computer with nothing installed. Pick your operating system below and go top to bottom.

---

## How to stop it (read this first)

- Press the **Esc** key at any time.
- Or click the terminal window and press **Enter**. This works even if Esc does not.
- Or fling your mouse into the **top-left corner** of the screen. That triggers a built-in emergency stop.

---

## Step 1 - Install Python

Python is the program that runs the script. You install it once.

### Windows 10 / 11

1. Open your web browser and go to **https://www.python.org/downloads/**
2. Click the big yellow **Download Python 3.x.x** button. Open the file it downloads.
3. On the very first screen of the installer, **tick the box that says "Add python.exe to PATH"** at the bottom. This is the step people miss. Then click **Install Now**.
4. When it finishes, click Close.
5. Check it worked: press the **Windows key**, type `PowerShell`, press Enter. A blue window opens. Type this and press Enter:

   ```
   py --version
   ```

   You should see something like `Python 3.12.4`. If you do, move on.

If typing `python` opens the Microsoft Store instead, Python is not set up. Run the installer again and make sure the **Add python.exe to PATH** box is ticked.

### Mac

1. Open Safari and go to **https://www.python.org/downloads/**
2. Click the big yellow **Download Python 3.x.x** button. Open the `.pkg` file it downloads.
3. Click Continue, Continue, Agree, Install. Enter your Mac password if asked. Click Close when done.
4. Check it worked: press **Command + Space**, type `Terminal`, press Enter. A window opens. Type this and press Enter:

   ```
   python3 --version
   ```

   You should see something like `Python 3.12.4`.

You do not need Homebrew or anything else.

---

## Step 2 - Download this project from the terminal

Keep the same terminal window open (PowerShell on Windows, Terminal on Mac). Copy each block, paste it in, and press Enter. These commands download the project into your Downloads folder and move you into it.

### Windows (PowerShell)

```
cd ~\Downloads
Invoke-WebRequest -Uri https://github.com/edwardvth/bot-commenting-DU/archive/refs/heads/main.zip -OutFile bot-commenting-DU.zip
Expand-Archive -Path bot-commenting-DU.zip -DestinationPath . -Force
cd bot-commenting-DU-main
```

### Mac (Terminal)

```
cd ~/Downloads
curl -L -o bot-commenting-DU.zip https://github.com/edwardvth/bot-commenting-DU/archive/refs/heads/main.zip
unzip -o bot-commenting-DU.zip
cd bot-commenting-DU-main
```

After the last command, your terminal is sitting inside the project folder. Stay there for every step below.

**Prefer not to use the terminal for the download?** On this GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it, then in your terminal type `cd ` (with a space), drag the unzipped folder onto the terminal window, and press Enter.

---

## Step 3 - Install the three helper packages

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

## Step 4 - Mac only: allow Terminal to control the mouse and keyboard

macOS blocks programs from clicking and typing until you give permission. The script checks for both permissions when it starts. If either is missing it pops up the macOS permission dialog, prints exactly what to turn on, and exits instead of running with a dead Esc key.

1. Open **System Settings** (Apple menu, top left).
2. Go to **Privacy & Security**, then **Accessibility**. Turn the switch **on** for **Terminal**. If Terminal is not in the list, click the **+** button, go to Applications, then Utilities, and pick Terminal.
3. Still in Privacy & Security, go to **Input Monitoring**. Turn the switch **on** for **Terminal**.
4. If a macOS dialog appeared asking to allow Terminal, click **Open System Settings** and turn it on there.
5. **Quit Terminal completely** (Command + Q) and open it again, then `cd` back into the folder:

   ```
   cd ~/Downloads/bot-commenting-DU-main
   ```

Windows users skip this step.

---

## Step 5 - Run it

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
5. It will type a message, click Send, wait a few seconds, and repeat until you stop it with **Esc** or the top-left corner.

---

## Changing what it sends and how fast

Open `human_message_sender.py` in any text editor (Notepad on Windows, TextEdit on Mac, or right-click the file and choose Open With). Near the top you will see:

- `MESSAGES = [ ... ]` - the list it picks from. Add, remove, or change lines. Keep each one inside quotes with a comma after it.
- `MIN_BETWEEN_SUBMISSIONS` and `MAX_BETWEEN_SUBMISSIONS` - the shortest and longest wait, in seconds, between sends.
- `MIN_KEY_DELAY` and `MAX_KEY_DELAY` - how fast it types each character.

Save the file and run it again.

---

## The second script: two_button_clicker.py

Clicks spot A, waits half a second, clicks spot B, and repeats. Same setup as above. Run it with:

**Windows**
```
py two_button_clicker.py
```

**Mac**
```
python3 two_button_clicker.py
```

It asks you to hover over Button 1 and Button 2 the same way, then starts after a 3-second countdown. Change `BUTTON_DELAY` at the top of the file to speed it up or slow it down.

---

## If something goes wrong

**"python is not recognized" or the Microsoft Store opens (Windows)**
Python was installed without the PATH box ticked. Reinstall from python.org and tick **Add python.exe to PATH**. Always use `py` rather than `python` in the commands.

**"pip is not recognized"**
Use the longer form shown in Step 3: `py -m pip ...` on Windows, `python3 -m pip ...` on Mac.

**"No module named pyautogui" (or pynput, or pyperclip)**
The packages were installed into a different copy of Python than the one running the script. Run the Step 3 install command again, using exactly the same first word you use to run the script (`py` on Windows, `python3` on Mac).

**On Mac, Esc does not stop it**
Esc uses a system-wide keyboard hook that macOS only allows when Terminal has **Input Monitoring** turned on (Accessibility alone is not enough). Turn it on in System Settings, then Privacy & Security, then Input Monitoring, quit Terminal with Command + Q and open it again. The script now checks this at startup and tells you if it is off. In the meantime, click the terminal window and press Enter, which always works.

**On Mac the script runs but nothing gets clicked or typed**
Accessibility is off for Terminal. Turn it on under Privacy & Security, then Accessibility, quit Terminal with Command + Q, open it again.

**It clicks the wrong spot**
The browser window moved or changed size after calibration. Stop it, put the browser back, run the script again and recalibrate. On Windows, if clicks are consistently off, set display scaling to 100% in Settings, then System, then Display.

**Emoji show up as blank or question marks**
Emoji are pasted through the clipboard, which needs `pyperclip`. Make sure the Step 3 install included it.

**It will not stop**
Fling the mouse hard into the very top-left corner of the screen. If all else fails, close the terminal window.
