import pprint

def p_dict(title, dictionary):
	pp = pprint.PrettyPrinter(indent=4)

	print "-"*50
	print title
	print "-"*50
	pp.pprint(dictionary)
	return