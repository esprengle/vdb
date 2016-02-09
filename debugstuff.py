# coding: utf-8
# first test: 
from objc_util import *
app=ObjCClass('UIApplication').sharedApplication()
d=app.delegate()
vc=app.delegate().viewController()
#tvc=d.detailViewController()
import bdb
class PyDB(bdb.Bdb):

	def user_call(self,frame, argument_list):
		'''This method is called from dispatch_call() when there is the possibility that a break might be necessary anywhere inside the called function.'''
		print 'call'
		print '{} in {}'.format(frame.f_code.co_name,frame.f_code.co_filename)
		print 'args:    ',argument_list
		print 'locals:  ',frame.f_locals
		print 'lineno:', frame.f_code.co_firstlineno
		print 'linenotab:', frame.f_code.co_lnotab
		print 'current', frame.f_lineno
	def user_line(self,frame):
		'''This method is called from dispatch_line() when either stop_here() or break_here() yields True.'''
		print 'locals:  ',frame.f_locals
		print 'lineno:', frame.f_code.co_firstlineno
		print 'linenotab:', frame.f_code.co_lnotab
		print 'current', frame.f_lineno
		print 'curti',frame.f_lasti
	def user_return(self,frame, return_value):
		'''This method is called from dispatch_return() when stop_here() yields True.'''
		pass

	def user_exception(self,frame, exc_info):
		'''This method is called from dispatch_exception() when stop_here() yields True.'''
		pass

	def do_clear(self,arg):
		'''Handle how a breakpoint must be removed when it is a temporary one.
	This method must be implemented by derived classes.'''
		print arg
		
	
fr
		