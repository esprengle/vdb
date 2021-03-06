# coding: utf-8
# Visual Debugger
#   interactive debugger inside pythonista editor
#    currently supports:
#           single stepping, or step over
#           continue, or quit
#           watch window (view only right now)
#           During debugging, current line is highlighted, and editor opens new file if needed
#.  TODO:
#       breakpoint set/clear by tapping line #s
#.   launch script via menu
#.   stack up/down
#.   help menu
#.   optimizations for small devices

import editor,os
import ui
import console
import threading
from WatchWindow import dict_dialog
from debug_menu import create_menu
from objc_util import *
import bdb


class VDB(bdb.Bdb):
	def __init__(self, *args, **kwargs):
		bdb.Bdb.__init__(self, *args, **kwargs)
		self.event = threading.Event()
		self.curframe = None
		self.debugmenu = create_menu(self)

	def forget(self):
		self.lineno = None
		self.stack = []
		self.curindex = 0
		self.curframe = None

	def setup(self, frame, t):
		if frame and '<string>' not in frame.f_code.co_filename:
			self.forget()
			self.stack, self.curindex = self.get_stack(frame, t)
			self.setup_ui()
			
	def setup_ui(self):
		self.curframe = self.stack[self.curindex][0]
		# The f_locals dictionary is updated from the actual frame
		# locals whenever the .f_locals accessor is called, so we
		# cache it here to ensure that modifications are not overwritten.
		editor.clear_annotations()
		self.curframe_locals = self.curframe.f_locals
		frame=self.curframe
		
		editor.open_file(frame.f_code.co_filename)
		editor.annotate_line(frame.f_lineno,
									filename = frame.f_code.co_filename,
									scroll = True)
		self.show_menu()
		self.debugmenu['down'].enabled=self.curindex<len(self.stack)-1
		self.debugmenu['up'].enabled=self.curindex>0
		console.hide_output()

	#############################
	# debugger ui actions
	def step_in_action(self, sender):
		self.set_step()
		self.event.set()
		editor.clear_annotations()

	def step_over_action(self, sender):
		self.set_next(self.curframe)
		self.event.set()
		editor.clear_annotations()
		
	def step_out_action(self,sender):
		if self.curindex >0:
			self.set_next(self.stack[self.curindex-1][0])
		self.event.set()
		
	def up_action(self,sender):
		self.curindex -= 1
		self.setup_ui()
		
	def down_action(self,sender):
		self.curindex+=1
		self.setup_ui()
			
	def play_action(self, sender):
		editor.clear_annotations()
		self.hide_menu()
		self.set_continue()
		self.event.set()

	def watch_action(self, sender):
		dict_dialog({'Globals:': self.curframe.f_globals,
		'Locals:':  self.curframe_locals})

	def stop_action(self, sender):
		editor.clear_annotations()
		self.cancel()

	# #######################
	def cancel(self):
		self.set_quit()
		self.event.set()

	def user_call(self, frame, argument_list):
		'''This method is called from dispatch_call() when there is the possibility that a break might be necessary anywhere inside the called function.'''
		pass

	def interaction(self, frame):
			self.setup(frame,None)
			self.event.clear()
			try:
				while True:
					if self.event.wait(2):  # allow keyboard interrupt
						break
			finally:
				editor.clear_annotations()
				self.hide_menu()
			if self.quitting:
				self.hide_menu()

	def user_line(self, frame):
		'''This method is called from dispatch_line() when either stop_here() or break_here() yields True.'''
		self.interaction(frame)

	def user_return(self, frame, return_value):
		'''This method is called from dispatch_return() when stop_here() yields True.'''
		self.hide_menu()

	def user_exception(self, frame, exc_info):
		'''This method is called from dispatch_exception() when stop_here() yields True.'''
		self.hide_menu()

	def do_clear(self, arg):
		'''Handle how a breakpoint must be removed when it is a temporary one.
		This method must be implemented by derived classes.'''
		print arg

	@on_main_thread
	def show_menu(self):
		'''attach debuggermenu to current editorview, killing
		existing view if it exists.  TODO: reuse existing object.
		'''
		DEBUGMENUTAG = hash('DEBUGMENU')
		ed = editor._get_editor_tab().editorView()
		debugmenuobj = ed.viewWithTag_(DEBUGMENUTAG)
		try:
			if debugmenuobj:
				debugmenuobj.removeFromSuperview()
				ObjCInstance(self.debugmenu).removeFromSuperview()
		except AttributeError:
			pass
		ed.addSubview_(self.debugmenu)

	@on_main_thread
	def hide_menu(self):
		try:
			ObjCInstance(self.debugmenu).removeFromSuperview()
		except AttributeError:
			pass
def pm():
	dbg=	VDB()
	dbg.interaction(sys.last_traceback.tb_frame)
def runcall(*args,**kwargs):
	VDB().runcall(*args,**kwargs)
def set_trace():
	VDB().set_trace()
if __name__=='__main__':
	# when run from action menu, debug call current script
	import sys
	if len(sys.argv)==2 and sys.argv[1]=='pm':
		pm()
	else:
		currentfile=editor.get_path()
		dbg=VDB()
		dbg.runcall(execfile,currentfile)
