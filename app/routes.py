from flask import render_template
from app import app
from .TextManager import TextManager

@app.route('/')
def index():
	data = TextManager.echo("I'm calling a method, and it's going to show up through the template.")
	return render_template('index.html', data=data)