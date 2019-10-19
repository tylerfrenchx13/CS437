import pickle

pre_calculated_suggestions = pickle.load(open("app/data/query_suggestions.p", "rb"))

class QuerySuggestions:

    def __init__(self):
        pass

    def GetCandidates(self, q, n=10):
        if q in pre_calculated_suggestions:
            return pre_calculated_suggestions[q][:n]
        else:
            return []