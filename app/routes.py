from flask import render_template
from app import app
from .TextManager import TextManager
from .QuerySuggestions import QuerySuggestions
from flask import jsonify

@app.route('/')
def index():
	#TextManager.processText()
	return render_template('index.html', data=None)

@app.route('/query_suggestion/<string:query>', methods=['GET'])
def query_suggestion(query):
    #print(QuerySuggestions.GetCandidates('tiger'))
	return jsonify(QuerySuggestions.GetCandidates(query))