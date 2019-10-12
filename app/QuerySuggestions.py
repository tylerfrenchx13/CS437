import pickle

pre_calculated_suggestions = pickle.load(open("app/data/query_suggestions.p", "rb"))

class QuerySuggestions:

    def GetCandidates(q, n=10):
        if q in pre_calculated_suggestions:
            return pre_calculated_suggestions[q][:n]
        else:
            return []