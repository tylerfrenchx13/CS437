from flask import render_template
from app import app
from .QuerySuggestions import QuerySuggestions
from .SnippetGenerator import SnippetGenerator
from .RankMeUp import RankMeUp
from flask import jsonify
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logging.info("initializing")
print('initializing')
sys.stdout.flush()
ranker = RankMeUp()
qs = QuerySuggestions()

@app.route('/')
def index():
	#TextManager.processText()
	return render_template('index.html', data=None)

@app.route('/query_suggestion/<string:query>', methods=['GET'])
def query_suggestion(query):
    #print(QuerySuggestions.GetCandidates('tiger'))W
	return jsonify(qs.GetCandidates(query))

@app.route('/search/<string:query>', methods=['GET'])
def search_results(query):
	documents = ranker.rankMeUpScotty(query)
	snipgen = SnippetGenerator()
	real_data = {}
	real_data['query'] = query
	real_data['search_results'] = snipgen.getSnippets(query, documents)
	return render_template('search_results.html', data=real_data)