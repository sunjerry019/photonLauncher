def binary(s):
    return str(s) if s<=1 else bin(s>>1) + str(s&1)

# TEST if COM PORT IS WORKING
# Connect pins 2 and 3 on the female rs232 port and see if you receive what you send (COM PORT LOOPBACK TEST)


# print(x.send("-5000 -5000 5000 5000 setlimit"))

# print(x.send("1 1 setunit")) # x-axis
# print(x.send("1 2 setunit")) # y-axis
# print(x.send("1 0 setunit")) # velocity
# print(x.send("150 setvel"))
# print(x.send("500 500 r"))
# print(x.send("1000 1000 r"))


# , awaitCompletion = Fals

# if awaitCompletion:
# 	# we send a blocking command to block the FIFO stack so that
# 	# any further inputs into the stack is blocked
# 	self.dev.write("ge".encode("ascii") + self.Enter)