import pprint
import os

def p_dict(title, dictionary):
	pp = pprint.PrettyPrinter(indent=4)

	print "-"*50
	print title
	print "-"*50
	pp.pprint(dictionary)
	return

def make_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except:
            print "Could not create a folder ", folder
        