#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy as sq
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
#from flask.ext.wtf import CsrProtect
from wtforms.ext.sqlalchemy.orm import model_form
# from models import User
from Adafruit_Raspberry_Pi_Python_Code.Adafruit_PWM_Servo_Driver.Adafruit_PWM_Servo_Driver import PWM

#csrf = CsrfProtect

app = Flask('__name__')
#csrf.init_app(app)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'Aasdf0897214fasdf08972134'
app.config['SECRET_KEY'] = 'Aasdf0897214fasdf08972134'
toolbar = DebugToolbarExtension(app)
db = sq(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username=None, email=None):
		self.username = username
		self.email = email
		
	def __repr__(self):
		return '<User %>' % self.username

class LightConfig(db.Model):
	pk = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	channels = db.Column(db.PickleType)		# No array type for slqlite, lets just pickle everything

	def __init__(self, name=None, channels=None):
		self.name = name
		self.channels = channels

	def __repr__(self):
		return '<LightConfig %s>' % self.name

class LightConfigForm(Form):
	name = StringField('Name', validators=[DataRequired()])
	channels = StringField('Channels (R, G, B, W)', validators=[DataRequired()])

@app.route("/lightConfig/", methods=['POST'])
@app.route("/lightConfig<pk>/", methods=['GET','POST'])
def lightConfig(pk=None):
	if pk is None:
		form = LightConfigForm()
	else:
		model = LightConfig.query.get(pk)
		form = LightConfigForm(obj=model)

	if form.validate_on_submit():
		if pk is None:
			model = LightConfig()
		form.populate_obj(model)
		model.channels = eval(model.channels)
		if pk is None:
			db.session.add(model)
		db.session.commit()
		return redirect(url_for("index"))
	return render_template("generic_edit.html", form=form, user=model)

@app.route("/lightConfig<pk>/delete", methods=['POST'])
def deleteLightConfig(pk):
	model = LightConfig.query.filter_by(pk=pk)
	model.delete()
	db.session.commit()
	return redirect(url_for("index"))


@app.route("/activateLightConfig<pk>")
def activateLightConfig(pk):
	model = LightConfig.query.get(pk)

	channels = []
	for ch, val in enumerate(model.channels):
		if val is not None:
			pwm.setPWM(ch, 0, int(val))
			channels.append("ch {} = {}".format(ch, val))
		else:
			channels.append("ch {} = {}".format(ch, None))
		
	return " | ".join(channels)

@app.route("/")
def index():
	users = User.query.all()
	lightConfigs = LightConfig.query.all()

	#MyForm = model_form(LightConfig, base_class=Form)
	#form = MyForm(request.form, model)
	form = LightConfigForm()

	return render_template("index.html", users=users, lightConfigs=lightConfigs, form=form, action="Add", data_type="a light config", form_action=url_for("lightConfig") )

@app.route("/user<pk>", methods=['GET','POST'])
def user(pk):
	MyForm = model_form(User, base_class=Form)
	print("44$$$$$$$" + pk)
	model = User.query.get(pk)
	form = MyForm(request.form, model)

	if form.validate_on_submit():
		form.populate_obj(model)
		db.session.commit()
		return redirect(url_for("index"))
	return render_template("edit.html", form=form, user=model)

@app.route("/resetI2C")
def resetI2C():
	pwm = PWM(0x70)
	return "reset"

if __name__ == '__main__':
	pwm = PWM(0x70)
	pwm.setPWM(4, 0, 100)
	app.run(host='0.0.0.0', port=80)
