<p align="center">
  <img src="https://files.catbox.moe/7ycsbb.png" width="120" alt="Onion Logo">
</p>

<h2 align="center">Onion UI Webhook Spammer</h2>

<p align="center">
  <strong>Open-source Ready-to-use webhook spammer with a clean UI</strong>
  <br><br>
  <a href="https://discord.gg/onionvin">Support Server</a>
  ·
  <strong>Support the project by starring ⭐</strong>
</p>

---

## About

Hello!

This project is a Webhook Spammer built with a graphical user interface.
The full Python source code is included and can be freely edited or extended.

For convenience, a pre-compiled Windows executable is also provided for users who
do not want to compile the project themselves.

---

## Features

- **UI-Based**  
  Simple and clean graphical interface

- **Fast Spamming**  
  Quick and responsive webhook sending

- **Editable Source**  
  Full Python source code included

- **EXE Included**  
  Ready-to-use Windows executable

---

## Files

- `main.py` Python source code  
- `main.exe` Pre-compiled Windows executable  
- `onion.png` Application logo  
- `ui-spammer-screenshot.png` UI preview  
- `README.md` Project documentation  

---

## Screenshot

  <img src="https://files.catbox.moe/4eeyfc.png" width="1020" alt="Onion Logo">

---

## Compile with (Nuitka)

```bash
py -3.10 -m nuitka ^
--standalone ^
--onefile ^
--windows-console-mode=disable ^
--enable-plugin=pyside6 ^
--windows-icon-from-ico=onion.ico ^
main.py
