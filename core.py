import sys
import cmd
import os
import os.path
from stat import *
import argparse
import ConfigParser
import logging
import logging.handlers
import cmdline


#TODO
# - cmdline interface argument (default = enable)

"""Initial command line interface.  Will re-factor later"""

class Core:
	
	def __init__(self):
		self.Paths = {}
		self.Functions = {}
		self.DbAuth = {}
		self.cmdLineArgs()
		
		
		self.Main()
		
	
	def cmdLineArgs(self): #TODO add layer of transparency to ease extendibility
		parser = argparse.ArgumentParser(description="Media organization")
		parser.add_argument("-v","--verbose",action="store_true",help="print program information to the command line",dest="verbose")
		parser.add_argument("-l","--logging",action="store_true",help="enable logging",dest="logging")
		parser.add_argument("-d","--debugging",action="store_true",help="enable debug logging",dest="debug")
		parser.add_argument("--config-path",nargs=1,help="path to config file.",dest="config_path",default="",metavar="PATH")
		parser.add_argument("--media-path",nargs=1,help="directory containing media files. default='E:\vids'",dest="media_path",metavar="PATH")
		parser.add_argument("--log-path",nargs=1,help="directory containing log files. default='log'",dest="log_path",metavar="PATH")
		parser.add_argument("-u",nargs=1,help="MySQL user name.",dest='user')
		parser.add_argument("-p",nargs=1,help="MySQL password.",dest='password')
		parser.add_argument("--host",nargs=1,help="MySQL host name.",dest='host')
		parser.add_argument("--db",nargs=1,help="MySQL database.",dest='db')
		args = parser.parse_args()

		self.getConfig(args.config_path)

		if args.logging: self.Functions['logging'] = args.logging
		if args.verbose: self.Functions['verbose'] = args.verbose
		if args.debug: self.Functions['debug'] = args.debug
		if args.media_path: self.Paths['media_path'] = args.media_path
		if args.log_path: self.Paths['log_path'] = args.log_path
		if args.user: self.DbAuth['user'] = args.user
		if args.password: self.DbAuth['password'] = args.password
		if args.host: self.DbAuth['host'] = args.host
		if args.db: self.DbAuth['db'] = args.db

	def createDefaultConfig(self):
		config = ConfigParser.RawConfigParser()
		config.add_section('Paths')
		config.set('Paths', 'media', 'E:\\vids')
		config.set('Paths', 'log', 'log')
		#config.set('Paths', 'media', ['E:\\vids','E:\\My Videos']) #change to E:\\My Videos and C:\\Users\\user\\My Videos
		config.add_section('Functions')
		config.set('Functions', 'verbose', False)
		config.set('Functions', 'logging', False)
		config.set('Functions', 'debug', False)
		config.add_section('DbAuth')
		config.set('DbAuth', 'user', 'user')
		config.set('DbAuth', 'password', 'password')
		config.set('DbAuth', 'host', '127.0.0.1')
		config.set('DbAuth', 'Db', 'media')
		with open('default.cfg', 'wb') as configfile:
			config.write(configfile)
		
	def getConfig(self, configpath=''):
		fp = None
		self.config = ConfigParser.RawConfigParser()
		if os.path.exists(configpath):
			fp = open(configpath)
		elif os.path.exists('default.cfg'):
			fp = open('default.cfg')
		else:
			self.createDefaultConfig() # create default cfg if no cfg exixts
			fp = open('default.cfg')
		if fp:
			self.config.readfp(fp)
			if self.config.has_section('Paths'):
				for path in self.config.items('Paths'):
					self.Paths[path[0]+'_path'] = path[1]
			if self.config.has_section('Functions'):
				for func in self.config.items('Functions'):
					self.Functions[func[0]] = func[1]
			if self.config.has_section('DbAuth'):
				for db in self.config.items('DbAuth'):
					self.DbAuth[db[0]] = db[1]
					
					
	def indexMedia(self):
		#get list of media files
		self.indexed = []
		os.path.walk(self.Paths['media_path'],self.indexing,self.indexed)
		print self.indexed

	def indexing(self,arg,dirname,names):
		for name in names:
			currentfile = os.path.join(dirname,name)
			if os.path.isfile(currentfile):
				newfile = os.path.join(dirname,name.replace(' ','.'))
				os.rename(currentfile,newfile)
				arg.append(newfile)
	
	
	def printIndex(self, s):
		print 'Printing Indexes'
	
	def Main(self):
		#main function.  Will work through command line prompts
		#self.indexMedia()
		comand = cmdline.CmdLine()
		comand.regf(p=self.printIndex)
		comand.regf(p=self.printIndex)
		print comand.getreg()
		introtext = 'Welcome!'
		comand.cmdloop(introtext)

	
if __name__ == '__main__':
    core = Core()

	
	
	
	
	
