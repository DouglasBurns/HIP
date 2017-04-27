# import os
from subprocess import call

def main():

	tknesss = [
		# '300', 
		'500',
	]
	occs 	= [
		'0.005', 
		'0.010', 
		'0.015', 
		'0.020', 
		# '0.040',
	]
	taus	= [
		'5', 
		'10',
		'20',
		'50',
	]
	bss 	= [
		# '0', 
		'1', 
		# '2',
	]


	for bs in bss:
		for tkness in tknesss:
			for tau in taus:
				for occ in occs:
					command = ''
					command_base = 'python ResponseSimulator.py -n'
					tk = ' -S '+tkness
					o  = ' -O '+occ
					b  = ' -B '+bs
					t  = ' -T '+tau
					n  = ' -N 10000'
					bl = ' -b'
					command = command_base + tk + o + b + t + n
					print "Running : {}".format(command)
					command = command.split(' ')
					call(command)
					command = command_base + tk + o + b + t + n + bl
					print "Running : {}".format(command)
					command = command.split(' ')
					call(command)
	return

if __name__ == "__main__":
	main()