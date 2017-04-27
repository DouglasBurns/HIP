import pandas as pd 
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 4096)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 1000)

def dict_to_df(d):
	'''
	Transform a dictionary nto a dataframe
	'''
	df = pd.DataFrame(d)
	return df

def df_to_file(filepath, filename, df):
	'''
	Save a dataframe to an output text file
	Nicely human readable
	'''
	make_folder_if_not_exists(filepath)
	filepath = os.path.join(filepath, filename)
	with open(filepath,'w') as f:
		df.to_string(f, index=True)
		f.write('\n')
		print('DataFrame written to {}'.format(f))
		f.close()
	return

def file_to_df(f):
	'''
	Read a dataframe from file
	'''
	if os.path.exists(f):
		with open(f,'r') as f:
			df = pd.read_table(f, delim_whitespace=True)    	
			print('DataFrame read form {}'.format(f))
			f.close()
	else:
		print "Could not find {} ".format(f)
		return
	return df

def append_to_df(df, df_new):
	'''
	Append something to dataframe.
	Must have the same number of indexes
	'''
	# Overwrite existing columns of the same name
	for newcols in df_new.columns:
		for cols in df.columns:
			if newcols == cols:
				del df[cols]
	df = pd.concat([df, df_new], axis=1)
	return df

def make_folder_if_not_exists(folder):
	try:
		os.makedirs(folder)
	except:
		print "Could not create {} ".format(folder)
	return
        
