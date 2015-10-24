#!/usr/bin/env python3

from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from models import User

@app.route("index.html")
def index():
	return render_template("index.html")

@app.route("/edit<id>")
def edit(id):
	MyForm = model_form(User, Form)
	model = MyModel.get(id)
	form = MyForm(request.form, model)

	if form.validate_on_submit():
		form.populate_obj(model)
		model.put()
		flash("MyModel updated")
		return redirect(url_for("index"))
	return render_template("edit.html", form=form)
