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
		self.reg = {}
		self.helpreg = {}


	#register functions to be used in the interpreter as name=func
	def regf(self, **kwargs):
	#TODO - no duplicates (new overriding or not accepted?)
		for k,v in kwargs.iteritems():
			setattr(self,'do_'+k,v)
			self.reg[k] = False
	
	#return all registered functions
	def getreg(self):
		self.h = 123
		#print dir(self.__class__)
	
		return self.reg.keys()
	
	#register help for existing function only
	def regh(self, **kwargs):
		#TODO - no duplicates (new overriding or not accepted?)
		for k,v in kwargs.iteritems():
			setattr(self,'help_'+k,v)
			self.helpreg[k] = False
	
	#return all registered functions with no help
	def getunreghelp(self):
		#TODO work on better funct name
		ls = []
		for k in self.reg.keys():
			if not self.reg[k]: ls.append(k)
		return ls
	#return all registered functions with help
	def getreghelp(self):
		#TODO work on better funct name
		ls = []
		for k in self.reg.keys():
			if self.reg[k]: ls.append(k)
		return ls
	
	#Required hook for cmd.Cmd.get_names to include the functions that are added here
	def get_names(self):
		ls = []
		for k in self.reg.keys():
			ls.append('do_'+k)
		return ls + cmd.Cmd.get_names(self)
	
	#hook for cmdloop to make sure all function have been registered
	def cmdloop(self, intro=None):
		cmd.Cmd.cmdloop(self, intro)
	
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
	
	def cmdNone(self):
		print 'Command not initialized!'
	
	def do_list(self, s):
		#self.lscmd()
		func = getattr(self, 'help_list')
		func()
	
	def help_list(self):
		print 'Lists all media in the selected paths'
		