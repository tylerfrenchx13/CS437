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


@app.route('/search/<string:query>', methods=['GET'])
def search_results(query):
	fake_data = {}
	fake_data['query'] = query
	# Get actual ranked search results here 
	fake_data['search_results'] = [
		{
			'title':'Tiger',
			'snippet':'The tiger (Panthera tigris) is the largest species among the Felidae and classified in the genus Panthera. It is most recognisable for its dark vertical',
		},
		{
			'title':'Topologically Integrated Geographic Encoding and Referencing (redirect from TIGER)',
			'snippet':'Topologically Integrated Geographic Encoding and Referencing, or TIGER, or TIGER/Line is a format used by the United States Census Bureau to describe'
		},
		{
			'title':'Tiger Tiger',
			'snippet':'Tiger Tiger may refer to: "The Tyger", a 1794 poem by William Blake, which opens with "Tyger Tyger" "Tiger! Tiger!" (Kipling short story), an 1893/1894'
		},
		{
			'title':'Tiger Shroff',
			'snippet':'Jai Hemant "Tiger" Shroff (born 2 March 1990) is an Indian film actor who works in Hindi-language films. The son of actor Jackie Shroff and producer Ayesha'
		},
		{
			'title':'White tiger',
			'snippet':'The white tiger or bleached tiger is a pigmentation variant of the Bengal tiger, which is reported in the wild from time to time in the Indian states'
		}

	]
	return render_template('search_results.html', data=fake_data)