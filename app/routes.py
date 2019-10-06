from flask import render_template
from app import app
from .TextManager import TextManager

@app.route('/')
def index():
	TextManager.processText()
	
	
	#return render_template('index.html', data=data)