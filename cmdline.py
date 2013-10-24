import sys
import cmd
import os
import os.path

"""
Created by Joshua Malo
"""

class CmdLine(cmd.Cmd):
	"""Wrapper for cmd.Cmd class to allow for dynamically adding and removing command line interpreter commands.
	
	In this wrapper, functions for using normal cmdline (shell) based commands are enabled as well as the exit command.
	
	This class can be subclassed and used like the cmd.Cmd class with the added dynamic functionalities.
	"""
	default_prompt = 'mediaManager>'
	reg = {}
	
	def __init__(self, prompt=None, shell_access=True):
		"""Required setup for superclass cmd.Cmd
		"""
		if prompt:
			self.prompt = prompt
		else:
			self.prompt = self.default_prompt
		self.shell_access = shell_access
		cmd.Cmd.__init__(self)

	def get_names(self):
		"""Redefinition of cmd.Cmd.get_names() to include the names of the commands created here
		
		Special Note
		cmd.Cmd.get_names() uses dir(self.__class__) to identify the functions, this however does not
		get names from the __dict__ class attribute which is where these functions are stored.
		"""
		ls = []
		for k in self.reg.keys():
			ls.append('do_'+k)
			if self.reg[k]:
				ls.append('help_'+k)
		return ls + cmd.Cmd.get_names(self)

	def cmdloop(self, intro=None):
		"""Redefinition of cmd.Cmd.cmdloop to include additional checks if necessary
		"""
		cmd.Cmd.cmdloop(self, intro)

	def dyncmd(self, **kwargs):
		"""Adds a function dynamically to the interpreter
		
		kwargs represents key-value pairs in the form of (func_name=func)
		"""
		for k,v in kwargs.iteritems():
			setattr(self,'do_'+k,v)
			self.reg[k] = False
	
	def getdyncmd(self):
		"""Returns all dynamic functions
		"""
		return self.reg.keys()

	def dynhelp(self, **kwargs):
		"""Adds the help function for an already existing function
		Pass as key-value pair (func_name=func)
		"""
		for k,v in kwargs.iteritems():
			if k in self.reg.keys():
				setattr(self,'help_'+k,v)
				self.reg[k] = True

	def getnohelp(self):
		"""Returns list of undocumented commands
		"""
		ls = []
		for k in self.reg.keys():
			if not self.reg[k]: ls.append(k)
		return ls
	
	def remdyncmd(self, *args):
		"""Removes a dynamic command added by dyncmd
		"""
		for k in args:
			if k in self.reg:
				del self.reg[k]
			if hasattr(self,'do_'+k):
				delattr(self,'do_'+k)
			if hasattr(self,'help_'+k):
				delattr(self,'help_'+k)
	
	def remhelp(self, *args):
		"""Removes only the help function added with the function
		"""
		for k in args:
			if k in self.reg:
				del self.reg[k]
			if hasattr(self,'help_'+k):
				delattr(self,'help_'+k)
	
	def do_shell(self, s):
		"""Access shell/cmdline commands using 'shell' or '!'
		"""
		if shell_access:
			os.system(s)
		else:
			self.stdout.write('Shell Commands Not Allowed')
	
	def help_shell(self):
		self.stdout.write('Execute shell command')
	
	def can_exit(self):
		return True
	
	def do_exit(self, s):
		return True
	
	def help_exit(self):
		self.stdout.write('Will exit the mediamanager interpreter')

	def postcmd(self, stop, line):
		"""Hook method executed just after a command dispatch is finished.
		This hook implementation simply verifies if the user wishes to exit the program upon the quit condition
		which is stop == True.  For everything else it will do
		"""
		if stop:
			prompt = ''
			while not prompt == 'y' and not prompt == 'n':
				#The following 13 lines of code are taken from cmd.Cmd.cmdloop for consistency in user input(line -> prompt)
				if self.use_rawinput:
					try:
						prompt = raw_input('Are you sure you wish to quit?(y/n): ')
					except EOFError:
						prompt = 'EOF'
				else:
					self.stdout.write('Are you sure you wish to quit?(y/n): ')
					self.stdout.flush()
					prompt = self.stdin.readline()
					if not len(prompt):
						prompt = 'EOF'
					else:
						prompt = prompt.rstrip('\r\n')
			if prompt == 'n':
				stop = False
		return stop
