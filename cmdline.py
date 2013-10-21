import sys
import cmd
import os
import os.path



"""Initial command line interface.  Will re-factor later"""
class CmdLine(cmd.Cmd):
	prompt = 'mediaManager>'
	undoc_header = 'to doc'
	def __init__(self):
		cmd.Cmd.__init__(self)
		pass
	
	def do_list(self, s):
		print 'list'
	
	
	def do_shell(self, s):
		os.system(s)
	def help_shell(self):
		print 'Execute shell command'
	
	def can_exit(self):
		return True
	def do_exit(self, s):
		return True
	def help_exit(self):
		print 'Will exit the mediamanager interpreter'
	