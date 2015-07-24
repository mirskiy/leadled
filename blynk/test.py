#!/usr/bin/env python3

import socket
from Adafruit_Raspberry_Pi_Python_Code.Adafruit_PWM_Servo_Driver.Adafruit_PWM_Servo_Driver import PWM

# constants
HEADERLENGTH = 5

def dataToCommandList(data):
	""" takes in an data packet, outputs a list of commands """
	""" data packet should be a bytearray """
	""" recursive! """
	print('\t'+':'.join('{:02x}'.format(x) for x in data))

	# break up the header into the type, id, length
	# header is NOT ASCII, just ints
	hdrCmd = data[0]
	hdrId = (data[1]<<8) + data[2]
	hdrLen = (data[3]<<8) + data[4]  # this is the length of the body
	if( hdrCmd != 0x00 ):		# if this isn't a response, make sure specified length is < packet size (can have multiple packets in one recv)
		assert len(data) >= HEADERLENGTH+hdrLen, "failed: len %d" % len(data) 
	
	# get the body according to the length (body will be ascii)
	body = None
	if (hdrCmd!=0x00):		# if not response packet, get body
		assert len(data)>HEADERLENGTH, "packet isn't long enough!"
		print('\tdata is real!') #!!temp
		body = data[HEADERLENGTH:HEADERLENGTH+hdrLen]
		body = ''.join([chr(c) for c in body])
	else:
		print('\tdata is response')
	
	msg = {'cmd': hdrCmd, 'id': hdrId, 'len': hdrLen, 
			'body': body, }
	msgList = [msg]
	
	print("\tlen %d HDRLEN %d hdrLen %d" % (len(data), HEADERLENGTH, hdrLen) )
	if len(data) <= HEADERLENGTH + hdrLen:
		print("\t\tbase case") #!!temp
		return msgList
	else: # recurse!
		print("\t\trecurse") #!!temp
		msgList = msgList + dataToCommandList( data[HEADERLENGTH+hdrLen:] )
		return msgList

def setVirtualPort(singleCmd):
	""" whichever port was written to, set pwm on it """
	port = singleCmd[1]
	val = singleCmd[2]

	port = int(port)
	val = int(val)

	if port < 4:
		pwm.setPWM(port, 0, val)
	elif port < 16:
		pwm.setPWM(port, 0, 1000 if val else 0)
	else:
		port = port % 16
		pwm.setPWM(port, 0, 1000 if val else 0)

# all commands should take in a singleCmd
availableCommandsDict = { 
		'vw' : setVirtualPort,
		'pm' : lambda _: print("!!todoLater not yet implemented"),
		}

def executeCommandList(cmdList):
	""" ya know """

	print('\t----executing---- %s' % cmdList)
	for cmdDict in cmdList:
		# look at the type
		# call dict based on the type
		print("\tcmd: %d" % cmdDict['cmd'])
		print("\tbody %s" % cmdDict['body'])

		if cmdDict['body'] is None:  # skip response commands !!later should just have the funciton to parse them
			return

		cmd = cmdDict['body'].split('\x00')
		print('\t split command: %s' % cmd)
		availableCommandsDict[cmd[0]](cmd)

BUFFER_SIZE = 1024		# for socket
def connectSocket():
	# tcp setup, auth, print response
	TCP_IP = 'cloud.blynk.cc'
	TCP_PORT = 8442
	with open('auth.temp', 'r') as f:
		key = f.read()
		key = bytes(key.strip(), 'ascii')

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(bytes([0x02, 0x00, 0x01, 0x00, 0x20]))
	s.send(key)
	s.settimeout(5.0)  # set timeout so we can ping
	return s


if __name__ == "__main__":
	# pwm setup
	pwm = PWM(0x70)
	pwm.setPWM(4, 0, 100)

	s = connectSocket()

	loop=255
	while(1):
		loop += 1
		try:
			data = s.recv(BUFFER_SIZE)

			if( len(data)==0 ):		# this is a disconnect packet, we probably got kicked for being too quick. Let's restart connection
				print("disconnected! reconnecting")
				s = connectSocket()
				continue

			if( len(data)>0 ):  # if we got anything, print it
				dataHexString = ':'.join('{:02x}'.format(x) for x in data)
				print("got data %s!" % dataHexString)

			if( len(data)<HEADERLENGTH ):	# make sure the packet is long enough
				print("\tinvalid packet recieved, len %d" % len(data) )
				continue

			# if everything is ok, get the command and execute
			commandList = dataToCommandList(data)
			executeCommandList(commandList)

		except socket.timeout:
			print("timedout!")
			s.send(bytes([0x06, (loop&0xff00)>>8, loop&0x00ff, 0x00, 0x00]))
		except KeyboardInterrupt:
			print("clean exit")
			s.close()
			exit()


