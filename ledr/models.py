#!/usr/bin/env python3

from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy as sq
from flask.ext.wtf import Form
#from flask.ext.wtf import CsrProtect
from wtforms.ext.sqlalchemy.orm import model_form
# from models import User

#csrf = CsrfProtect

app = Flask('__name__')
#csrf.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = 'Aasdf0897214fasdf08972134'
db = sq(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username, email):
		self.username = username
		self.email = email
		
	def __repr(self):
		return '<User %>' % self.username


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/edit<pk>.", methods=['GET','POST'])
def edit(pk):
	MyForm = model_form(User, base_class=Form)
	print("44$$$$$$$" + pk)
	model = User.query.get(pk)
	form = MyForm(request.form, model)

	if form.validate_on_submit():
		form.populate_obj(model)
		model.put()
		flash("MyModel updated")
		return redirect(url_for("index"))
	return render_template("edit.html", form=form)

if __name__ == '__main__':
	app.run(debug=True)
