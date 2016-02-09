#
# coding: utf-8
# todo: best way to find editor tabs?
# 
import os

MENUTAG=hash('EDITORMENU')
from objc_util import *


def rect_to_tuple(rect):
	return (rect.origin.x, rect.origin.y, rect.size.width, rect.size.height)
app=UIApplication.sharedApplication()
rootVC = app.keyWindow().rootViewController()
tabVC = rootVC.detailViewController()
cvc=rootVC.accessoryViewController().consoleViewController()
dvc=rootVC.accessoryViewController().documentationViewController()

tabVC.allOpenFilePaths()
tabvcs=tabVC.tabViewControllers()
class EditorOverlay(object):
	def __init__(self,file=None):
		'''find the tab with the named file, and attach an overlay to it.  
		An editor OverLay will have the following features:
			* set/clear breakpoints
			* setline highlight
			* get / set line number
		Also, will install a user defined menu under main tabbar.
		Be sure to check for existing overlay.
		If file is None, use current tab.
		Think about "delegate" methods:
			fileoverlay_will_load
			fileoverlay_did_load
			overlay_did_close
			fileoverlay_did_setb
			fileoverlay_did_clearbp
			fileoverlay_did_changetabs

		'''
		self.file=file
		tab_vc=self._get_tab_vc()
		
	def _get_tab_vc(self):
		''' return the tabvc for th current file
		'''
		if not self.file:
			self.file=str(tabVC.selectedFilePath())
		for t in tabVC.tabViewControllers():
			if os.path.samefile(self.file,str(t.filePath())):
				return t

	def show_menu(self,menubar):
		tvc=self._get_tab_vc()
		ed=tvc.editorView()
		tv=ed.textView()
		editormenu = ed.viewWithTag_(MENUTAG)
		if not editormenu:
			editormenu=ui.View(frame=(0,0,tv.frame().size.width,32),bg_color=(.14,.2,.24))
			editormenu.flex='wh'
			editormenu.bg_color=None
			ed.addSubview_(ObjCInstance(editormenu))
			#tv.frameOrigin=CGPoint(0,32)
			ObjCInstance(editormenu).tag=MENUTAG
			editormenu=ObjCInstance(editormenu)
		for sv in editormenu.subviews():
			sv.removeFromSuperview()
		editormenu.addSubview_(ObjCInstance(menubar))
		menubar.frame=rect_to_tuple(editormenu.bounds())
		ts=ed.textView().textStorage()
	def hide_menu(self):
		tvc=self._get_tab_vc()
		ed=tvc.editorView()
		editormenu = ed.viewWithTag_(MENUTAG)
		if editormenu:
			editormenu.removeFromSuperview()
	def add_gutter_overlay(self):
		pass
e=EditorOverlay()

def misc():
	dvc=rootVC.accessoryViewController().documentationViewController()

	tabVC.allOpenFilePaths()
	tabvcs=tabVC.tabViewControllers()
	tabVC.selectedTabViewController()
	tvc=tabVC.selectedTabViewController()
	ed=tvc.editorView()
	tv=ed.textView()
	ts=tv.textStorage()
	return tv
def add_breakpoint(lineno):
	tvc=tabVC.selectedTabViewController()
	ed=tvc.editorView()
	tv=ed.textView()
	ts=tv.textStorage()
	bb= ts.paragraphs()[lineno].boundingBox()
	y=bb.origin.y
	h=w=min(bb.size.height,bb.size.width)
	with ui.ImageContext(w,h) as ctx:
		pth=ui.Path()
		pth.move_to(0,h/4.)
		pth.line_to(w/4.,0)
		pth.line_to(3*w/4.,0)
		pth.line_to(w,h/4.0)
		pth.line_to(w,3.*h/4.0)
		pth.line_to(3*w/4,h)
		pth.line_to(w/4,h)
		pth.line_to(0,3*h/4.0)
		ui.set_color('red')
		pth.fill()
		img = ctx.get_image()
	b=ui.Button(frame=(0,y,h,h),
					image=img,
					tint_color='red')
	b.width=32
	b.height=32
	b.center.y+=(bb.size.height-b.height)/2
	b.tint_color='red'
	b.alpha=.5
	bb=ObjCInstance(b)
	tv.contentView().addSubview_(bb)
tv=misc()
#ts.addAttribute_value_range_('NSBackgroundColor',UIColor.colorWithHexString_('e8eac3'),ts.paragraphs()[1].range())
#ts.removeAttribute_range_('NSBackgroundColor',ts.paragraphs()[1].range())
def rect_to_tuple(r):
	return (r.origin.x,r.origin.y,r.size.width,r.size.height)
class LineHighlighter(ui.View):
	def __init__(self,color=(1,0,0),y_offset=20):
		self.border_color=color
		self.bg_color=color
		self.alpha=0.2
		self.border_width=1
		self.touch_enabled=False
		self.obj=ObjCInstance(self)
		self.y_offset=y_offset
		self.flex='wh'
	def setLine(self,line):
		
		self.frame=rect_to_tuple(line.boundingBox())
		self.y+=self.y_offset
		self.width+=ts.gutterWidth()
		if not self.obj.superview():
			line.textStorage().textView().addSubview_(self.obj)
		self.line=line
	def removeLine(self):
		self.obj.removeFromSuperview()
	def layout(self):
		if True:
			self.setLine(self.line)
class gutterCover(ui.View):
	def __init__(self,tv):
		
		self.frame=(0,tv.contentView().frameOrigin().y,
						tv.gutterWidth(),tv.contentSize().height)
		self.flex='hb'
		self.bps=[]
		self.highlight=LineHighlighter((.8,.8,0),self.y)
		self.ts=tv.textStorage()
	def touch_began(self,touch):
		ts=self.ts
		line=ts.paragraphAtPoint_(CGPoint(ts.gutterWidth()+15,touch.location.y))
		lineno=ts.paragraphRangeForCharacterRange_(line.range()).location
		#print lineno, touch.location.y,line.boundingBox().origin.y
		self.highlight.setLine(line)
	def layout(self):
		print 'layedout'
		
	
g=gutterCover(tv)
tv.contentView().addSubview_(ObjCInstance(g))

#try to register for changes to text
class BreakPointManager(object):
	def __init__(self, bps):
		#bps is list of line numbers in current file with bps
		self.bps=bp
		self.buttons=[]
	def append(self,bp):
		self.bps.append(bp)
		self.buttons()
	
	
#create buttons
playbtn=ui.Button(image=ui.Image.named('iob:play_24'))
stopbtn=ui.Button(image=ui.Image.named('iob:stop_24'))
stackupbtn=ui.Button(image=ui.Image.named('iob:ios7_upload_outline_24'))
stackdownbtn=ui.Button(image=ui.Image.named('iob:ios7_download_outline_24'))
stepin=ui.Button(image=ui.Image.named('debug-step-into-24-000000.png'))
stepout=ui.Button(image=ui.Image.named('debug-step-out-24-000000.png'))
stepover=ui.Button(image=ui.Image.named('debug-step-over-24-000000.png'))
stepover=ui.Button(image=ui.Image.named('debug-step-over-24-000000.png'))

debugmenu=ui.View(frame=(0,0,tv.frame().size.width,44),bg_color=(.14,.2,.24))
#tv.superview().addSubview_(ObjCInstance(debugmenu))
debugmenu.add_subview(playbtn);playbtn.x+=36
debugmenu.add_subview(stopbtn);stopbtn.x=playbtn.x+36
debugmenu.add_subview(stepin);stepin.width=24;stepin.x=stopbtn.x+36+36
debugmenu.add_subview(stepover);stepover.width=24;stepover.x=stepin.x+36
debugmenu.add_subview(stepout);stepout.width=24;stepout.x=stepover.x+36

debugmenu.add_subview(stackupbtn);stackupbtn.width=24;stackupbtn.x=stepout.x+36+36
debugmenu.add_subview(stackdownbtn);stackdownbtn.width=24;stackdownbtn.x=stackupbtn.x+36
debugmenu.border_color=debugmenu.tint_color
debugmenu.border_width=1
#breakpointmanager
#currentlinehighlighter
#debugoverlay
#.   pinnable overlay!
#locals
#immediatein