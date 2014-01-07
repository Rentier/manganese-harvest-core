import sys

from harvest.gui import wizard

if __name__ == "__main__":
	try:
		wizard.demo()
	except Exception, e:
		print e
		sys.exit(1)