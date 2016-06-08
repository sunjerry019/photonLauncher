# Linux Helper Files

Here, files that were used for customization or configuration is stored here.
This includes scripts, motd, etc.

Mostly for archival and backup purposes.

## Reverse SSH

Currently, robin is set up to use infocommsociety.com as an intermediary for SSH-ing from the outside world. Use PuTTY for Windows, the terminal for *Nix systems.

```ssh hcphotonics@infocommsociety.com```, with the usual password. Use ```./connect 2222``` or ```./connect 2223``` and the usual password, to enter the lab network.

### Technical Information

```
Local Account: robin
Remote Account: hcphotonics
Forwarded to port: 2222
```

Basic usage: ```ssh -R 2222:localhost:22 hcphotonics@infocommsociety.com```

Please remember to do ```sudo systemctl enable sshd``` and ```sudo systemctl start sshd``` on *fresh* linux installations as sshd is not enabled by default on Fedora.

Note that Ubuntu GNOME does not come with ssh, and you have to install it yourself.

As the server will end the ssh session should it be inactive, ```ServerAliveInterval 100``` has to be appended to ```/etc/ssh/ssh_config``` on robin to keep the connection alive.

Since the school network is temperamental: ```autossh -M 0 -vv -f -N -R 2222:localhost:22 hcphotonics@infocommsociety.com```

Use ```nohup``` to prevent autossh from dying should the parent spawning process (e.g. ```cron```) die.

Use ```screen``` to prevent processes from ending prematurely should the ssh tunnel die. This is important especially when running updates.

Usage of ```screen``` is as such: <br>
```
screen -S "[screen name]"         Start a screen with *[screen name]*
screen -ls                        List all screens
screen -r [name]                  Attach to *[name]* screen
screen -dRR                       Reattach  a  session  and if necessary detach or create it. Use the first session if more than one session is available.
```

For more, read ```man screen```

## users.txt

This file contains the info for users on all the computers. This is for easy ssh-ing.

## quotes.txt

Copy and pasted stuff. Need to update as time goes by.....

Arranged by time. Top is the earliest (2 Dec, 2013)
Some 2 liners are combined into 1 line just cus.
The following are generally not pasted in:
- Links
- Salutations (meows and other non-usual signoffs are however kept)
- Lines with just names of people (e.g. ```zy:```)
- "Thanks"s oneliners
- Random one-word-liners that don't make sense

Generally if lines are concatenated, ```;```(s) was/were used.
Context info might be added, but flanked with ```[[...]]```.

Lists might be irritating but I'm just gonna include

To be used by .bash_login on robin (or anywhere else should you wish)

Feel free to filter as you wish. Nobody's gonna bite you because you removed a few lines from that file.
