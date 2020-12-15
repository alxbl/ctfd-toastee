# Toastee - Real-time challenge solve feed

Uses SocketIO to notify browsers when a new solve happens in real time.
Meant to be used as a browser source in OBS.

This is a very primitive proof-of-concept that I might eventually improve upon.

## Installation

- Clone into `CTFd/CTFd/plugins/toastee` (**not** `ctfd-toastee`)
- In your CTFd virtualenv (or pipenv), run `pip install -r toastee/requirements.txt` (It's basically just flask-socketio)
- Restart CTFd
- Tweak toast.wav and splash.gif

## Usage

- The toast feed is at `http://ctfd/toasts` and requires no authentication
- Admins can trigger a test toast with `curl http://ctfd/toast` (Be mindful of the missing **s**)

----
Created for [Montréhack](https://montrehack.ca) for *h0h0h0day 2020*
