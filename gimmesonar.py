import serial
from ipdb import set_trace
import matplotlib.pyplot as plt
import IPython
from numpy import *

# open serial to sonar
ser = serial.Serial(
	port="/dev/ttyUSB0",  # this might need to change,
	baudrate=115200, # DO NOT CHANGE
	timeout=5
	)
ser.close()

# Define switch data command bytes
HEADER_1 = 0xFE # DO NOT CHANGE
HEADER_2 = 0x44 # DO NOT CHANGE
HEAD_ID = 0x11 # 0x11, 0x12, 0x13 allowed
RANGE = 0x05 # 5, 10, 20, 30, 40, 50 meters allowed
RESERVED = 0x00 # DO NOT CHANGE
MASTER_SLAVE = 0x00 # probably shouldn't change
START_GAIN = 0x06 # 0 to 40dB in 1dB increments
ABSORPTION = 0x14 # 20=0.2dB/m
PULSE_LENGTH = 0x64 # length of acoustic tx pulse, 1 to 255 microseconds in 1us increments
PROFILE_MINRANGE = 0x00 # 0 to 25 (0 to 25 meters in 0.1 meter increments) Min range for profile point digitization
EXT_TRIGGER = 0x00 # don't change (our model doesn't support this)
DATA_POINTS = 0x19 # number of data points returned by head (0x19 -> 250 data points, 0x32 -> 500 data points)
PROFILE = 0x00 # if 1 the return data will have an ASCII 'IPX' header
SWITCH_DELAY = 0x01 # how long to pause before head sends data (0 to 255 in 2msec increments. DO NOT USE VALUE OF 253)
FREQUENCY = 0x64 # 675kHz
TERMINATE = 0xFD # DO NOT CHANGE

# Create packet to send to sonar
command_to_send = bytearray([
	HEADER_1,
	HEADER_2,
	HEAD_ID,
	RANGE,
	RESERVED,
	RESERVED,
	MASTER_SLAVE,
	RESERVED,
	START_GAIN,
	RESERVED,
	ABSORPTION,
	RESERVED,
	RESERVED,
	RESERVED,
	PULSE_LENGTH,
	PROFILE_MINRANGE,
	RESERVED,
	RESERVED,
	EXT_TRIGGER,
	DATA_POINTS,
	RESERVED,
	RESERVED,
	PROFILE,
	RESERVED,
	SWITCH_DELAY,
	FREQUENCY,
	TERMINATE
	])

plt.ion()
plt.figure()
plt.title('Sonar Return')
plt.xlabel('Distance (meters)')
plt.ylabel('Return')
plt.show()

for a in range(5555555):
	ser.open()
	ser.write( command_to_send )

	readback = ser.read(size=265)
	ser.close()

	range_returns = zeros(252)
	range_bins = linspace(0.0, 5.0, 252)
	range_returns = fromstring(readback[12:-1], dtype='int8')

	#IPython.embed()
	plt.plot(range_bins,range_returns)
	plt.pause(0.5)
