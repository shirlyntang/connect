import subprocess
p = subprocess.Popen(["ipython", "ipython.py"],stdout=subprocess.PIPE)

for line in iter(p.stdout.readline,''):
	print line.rstrip()
#	print "hi"
