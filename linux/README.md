# Linux Helper Files

Here, files that were used for customization or configuration is stored here.
This includes scripts, motd, etc.

Mostly for archival and backup purposes.

## Reverse SSH

Currently, robin is set up to use infocommsociety.com as an intermediary for SSH-ing from the outside world.

### What is reverse SSH
*explained by depressedsheep*

usual SSH from Alice to Bob looks like: Alice --> Bob

now suppose there's a charlie

charlie lives in a cage. charlie can only send messages outside, but messages can't get in normally

Bob cannot ssh into charlie normally

now, charlie reverse ssh into bob

bob <-- charlie

alice can now talk to charlie through bob


### Technical Information

```
Local Account: robin
Remote Account: hcphotonics
Forwarded to port: 2222
```

Basic usage: ```ssh -R 2222:localhost:22 hcphotonics@infocommsociety.com```

As the server will end the ssh session should it be inactive, ```ServerAliveInterval 100``` has to be appended to ```/etc/ssh/ssh_config``` on robin to keep the connection alive.

Since the school network is temperamental: ```autossh -M 0 -vv -f -N -R 2222:localhost:22 hcphotonics@infocommsociety.com```

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
