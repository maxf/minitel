# Minitalk


<p align="center"><img src="./talk-minitel.jpg" width="50%" alt="picture of a minitel side by side with a laptop, both running minitalk"/></p>

[What it is](https://maxf.github.io/minitel/minitalk/)

## How to

[These are instructions for Linux, but should be easily portable to MacOS]

1. create a new user called `minitel` on your machine. It's not strictly necessary, you can use an existing user, but it's safer. Otherwise use that user's name below instead of minitel.

2. Change your sshd configuration file (typically at `/etc/ssh/sshd_config`) to add:
```
Match User minitel
        ForceCommand /[path]/client.py
```
then restart sshd, usually `sudo service sshd restart`.


3. Make sure both `server.py` and `client` are executable.

4. In a terminal run `server.py`


5. In another terminal (at least 80x25) on the same machine, run
```
> TERM=vt100 ssh minitel@localhost
```

Type a user name and you can start typing and moving with the arrow keys

or, on a Minitel with the ESP32 dongle, set the connection to be ssh and the url to be the IP address of your PC, e.g. `192.168.0.12:22`. Also select the 80-column mode.
