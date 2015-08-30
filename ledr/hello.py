#!/usr/bin/env python3
from flask import Flask
from flask import request
from flask import render_template

from Adafruit_Raspberry_Pi_Python_Code.Adafruit_PWM_Servo_Driver.Adafruit_PWM_Servo_Driver import PWM
import time

app = Flask(__name__)

@app.route("/")
def hello():
	return "no World!"

@app.route("/blink")
def blink():
	for x in range(1, 100):
		pwm.setAllPWM(0, x)
		time.sleep(0.01)
	for x in range (1, 100):
		pwm.setAllPWM(0, 100-x)
		time.sleep(0.01)
	return "it Blinked!"

@app.route("/blinkMultiple")
def blinkMultiple():
	for _ in range(0, 5):
		blink()
	return "it blinked 5 times"

@app.route("/setColor")
def setColor():
	red = request.args.get('red')
	green = request.args.get('green')
	blue = request.args.get('blue')
	white = request.args.get('white')

	channels = [red, green, blue, white]

	for ch, val in enumerate(channels):
		if val is not None:
			pwm.setPWM(ch, 0, int(val))
		else:
			channels[ch] = 'None'		# set it to none so we can print it out below
	return "rgb %s" % (channels)

@app.route("/sliders")
def sliders():
	return render_template('sliders.html')

@app.route("/resetI2C")
def resetI2C():
	pwm = PWM(0x70)
	return "reset"


if __name__ == "__main__":
	pwm = PWM(0x70)
	pwm.setPWM(4, 0, 100)
	app.run(debug=True)

