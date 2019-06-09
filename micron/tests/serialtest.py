import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
	port='COM1',
	baudrate= 9600, #19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
	)

# ser.open()
if not ser.isOpen():
	ser.open()

print(ser.name)

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

# input=1
while True :
	# get keyboard input
	# Python 3 users
	_input = input(">> ")
	if _input == 'exit':
		ser.close()
		exit()
	else:
		# send the character to the device
		# (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
		cmd = _input.encode() + bytes([13])
		print(cmd)
		ser.write(cmd)
		out = b''
		# let's wait one second before reading output (let's give device time to answer)
		time.sleep(1)
		while ser.inWaiting() > 0:
			out += ser.read(1)
			
		if out != '':
			print(">>", out)