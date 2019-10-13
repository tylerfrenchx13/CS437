from flask import render_template
from app import app
from .QuerySuggestions import QuerySuggestions
from .SnippetGenerator import SnippetGenerator
from flask import jsonify

@app.route('/')
def index():
	#TextManager.processText()
	return render_template('index.html', data=None)

@app.route('/query_suggestion/<string:query>', methods=['GET'])
def query_suggestion(query):
    #print(QuerySuggestions.GetCandidates('tiger'))
	return jsonify(QuerySuggestions.GetCandidates(query))


@app.route('/search/<string:query>', methods=['GET'])
def search_results(query):
	snipgen = SnippetGenerator()
	real_data = {}
	real_data['query'] = query
	# Get actual ranked search results here
	real_data['search_results'] = snipgen.getSnippets(query)
	return render_template('search_results.html', data=real_data)