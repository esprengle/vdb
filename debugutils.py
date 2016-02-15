#
# coding: utf-8
# 
import os

MENUTAG=hash('EDITORMENU')
GUTTERTAG=hash('GUTTER')
HIGHLIGHTTAG=hash('HIGHLIGHT')
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
		self.file=os.path.abspath(file) if file else None
		ed=self.editorView()
		self.highlight=LineHighlighter(ed.textView().textStorage(),(.8,.8,0))
	def editorView(self):
		''' return the tabvc for th current file
		'''
		if not self.file:
			self.file=str(tabVC.selectedFilePath())
		for t in tabVC.tabViewControllers():
			if os.path.samefile(self.file,str(t.filePath())):
				return t.editorView()
	def highlight_line(self,lineno):
		self.highlight.setLine(lineno)
	def unhighlight(self):
		self.highlight.removeLine()
	def show_menu(self,menubar):
		ed=self.editorView()
		tv=ed.textView()
		editormenu = ed.viewWithTag_(MENUTAG)
		if not editormenu:
			editormenu=ui.View(frame=(0,0,tv.frame().size.width,32),bg_color=(.24,.2,.24))
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
		ed=self.editorView()
		editormenu = ed.viewWithTag_(MENUTAG)
		if editormenu:
			editormenu.removeFromSuperview()
	def button_img(self,size,color='red'):
		'''create breakpoint stopsign image'''
		w,h=size
		d=min(w,h)
		x0=0
		with ui.ImageContext(w,h) as ctx:
			pth=ui.Path()
			pth.move_to(x0,d/4.)
			pth.line_to(x0+d/4.,0)
			pth.line_to(x0+3*d/4.,0)
			pth.line_to(x0+d,d/4.0)
			pth.line_to(x0+d,3.*d/4.0)
			pth.line_to(x0+3*d/4,d)
			pth.line_to(x0+d/4,d)
			pth.line_to(x0,3*d/4.0)
			ui.set_color(color)
			pth.fill()
			return ctx.get_image()
	def add_breakpoint_button(self, lineno):
				#FIXME: BREAKPOINT FOR FILE
		if [b for f,l,b in bps if f==self.file and l==lineno]:
			return
		ed=self.editorView()
		tv=ed.textView()
		ts=tv.textStorage()
		bbox= ts.paragraphs()[lineno].boundingBox()
		y=bbox.origin.y
		h=bbox.size.height
		w=tv.gutterView().frame().size.width
		b=ui.Button(frame=(0,y,w,h),image=self.button_img((w-10,h)),
					tint_color='red')
		b.width=w
		b.height=bbox.size.height
		b.center.y+=(bbox.size.height-b.height)/2
		b.tint_color='red'
		b.bg_color=(1,1,1,.05)
		b.alpha=.5
		#b_obj=ObjCInstance(b)
		#tv.contentView().addSubview_(b_obj)
		self.gutter.add_subview(b)
		bps.append((self.file,lineno,b))
		b.lineno=lineno
		b.action=self.remove_breakpoint
		
		return b
	def remove_breakpoint(self,sender):
		#todo: lookup breakpoint amd delete it
		bps.remove((self.file,sender.lineno,sender))
		ObjCInstance(sender).removeFromSuperview()
	def add_gutter_overlay(self):
		if hasattr(self,'gutter'):
			return
		ed=self.editorView()
		tv=ed.textView()
		g=gutterCover(tv,action=self.add_breakpoint_button)
		self.gutter=g
		g.hidden=True
	def show_breakpoints(self):
		ed=self.editorView()
		tv=ed.textView()
		m=tv.margins()
		m.left=32
		m.top=44
		tv.margins=m
		self.gutter.hidden=False
	def hide_breakpoints(self):
		self.gutter.hidden=False
		ed=self.editorView()
		tv=ed.textView()
		m=tv.margins()
		m.left=0
		tv.margins=m
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

	


tv=misc()
#ts.addAttribute_value_range_('NSBackgroundColor',UIColor.colorWithHexString_('e8eac3'),ts.paragraphs()[1].range())
#ts.removeAttribute_range_('NSBackgroundColor',ts.paragraphs()[1].range())

class LineHighlighter(ui.View):
	def __init__(self,ts, color=(1,0,0)):
		oldhighlight= ts.textView().viewWithTag_(HIGHLIGHTTAG)
		if oldhighlight:
			oldhighlight.removeFromSuperview()
		self.border_color=color
		self.bg_color=color
		self.alpha=0.2
		self.border_width=1
		self.touch_enabled=False
		self.obj=ObjCInstance(self)
		self.obj.tag=HIGHLIGHTTAG
		self.flex='wh'
		self.ts=ts
	def setLine(self,lineno):
		line=self.ts.paragraphs()[lineno]
		self.setLineObj(line)
	def setLineObj(self,line):
		self.frame=rect_to_tuple(line.boundingBox())
		self.x+=self.ts.gutterWidth()
		self.width+=self.ts.gutterWidth()
		if not self.obj.superview():
			line.textStorage().textView().addSubview_(self.obj)
		self.line=line
	def removeLine(self):
		self.obj.removeFromSuperview()
	def layout(self):
		if True:
			self.setLineObj(self.line)
class gutterCover(ui.View):
	def __new__(cls,tv,*args,**kwargs):
		existing_cover=tv.contentView().viewWithTag_(GUTTERTAG)
		if existing_cover:
			existing_cover.removeFromSuperview()
		return  super(gutterCover, cls).__new__(cls,tv,*args,**kwargs)
	def __init__(self,tv,action=None):
		self.ts=tv.textStorage()
		self.frame=(0,0,
						tv.gutterWidth(),tv.contentSize().height)
		self.flex='hb'
		self.bps=[]

		ObjCInstance(self).tag=GUTTERTAG
		tv.contentView().addSubview_(ObjCInstance(self))
		self.bring_to_front()
		self.action=action
	def touch_began(self,touch):
		ts=self.ts
		line=ts.paragraphAtPoint_(CGPoint(ts.gutterWidth()+15,touch.location.y))
		lineno=ts.paragraphRangeForCharacterRange_(line.range()).location
		#print lineno, touch.location.y,line.boundingBox().origin.y
		#self.highlight.setLine(line)
	def touch_ended(self,touch):
		ts=self.ts
		line=ts.paragraphAtPoint_(CGPoint(ts.gutterWidth()+15,touch.location.y))
		lineno=ts.paragraphRangeForCharacterRange_(line.range()).location
		if callable(self.action):
			self.action(lineno)
	def layout(self):
		#todo: think about what belongs here
		# relayout breakpoints
		pass
		
bps=[]
e=EditorOverlay()
e.add_gutter_overlay()
e.add_breakpoint_button(200)
e.show_breakpoints()


	
#create buttons
playbtn=ui.ButtonItem(image=ui.Image.named('iob:play_24'))
stopbtn=ui.ButtonItem(image=ui.Image.named('iob:stop_24'))
stackupbtn=ui.ButtonItem(image=ui.Image.named('iob:ios7_upload_outline_24'))
stackdownbtn=ui.ButtonItem(image=ui.Image.named('iob:ios7_download_outline_24'))
stepin=ui.ButtonItem(image=ui.Image.named('debug-step-into-24-000000.png'))
stepout=ui.ButtonItem(image=ui.Image.named('debug-step-out-24-000000.png'))
stepover=ui.ButtonItem(image=ui.Image.named('debug-step-over-24-000000.png'))
stepover=ui.Button(image=ui.Image.named('debug-step-over-24-000000.png'))


debugmenu=ui.View(frame=(0,0,tv.frame().size.width,44),bg_color=(.19, .3, .38))
debugmenu.left_button_items=[playbtn,stopbtn,stepin]
debugmenunav=ui.NavigationView(debugmenu,frame=(0,0,tv.frame().size.width,44))
#tv.superview().addSubview_(ObjCInstance(debugmenu))
if 0:
	debugmenu.add_subview(playbtn);playbtn.x+=36
	debugmenu.add_subview(stopbtn);stopbtn.x=playbtn.x+36
	debugmenu.add_subview(stepin);stepin.width=24;stepin.x=stopbtn.x+36+36
	debugmenu.add_subview(stepover);stepover.width=24;stepover.x= stepin.x+36
	debugmenu.add_subview(stepout);stepout.width=24;stepout.x=stepover.x+36
	
	debugmenu.add_subview(stackupbtn);stackupbtn.width=24;stackupbtn.x=stepout.x+36+36
	debugmenu.add_subview(stackdownbtn);stackdownbtn.width=24;stackdownbtn.x=stackupbtn.x+36

debugmenu.border_color=debugmenu.tint_color
debugmenu.border_width=1

e.show_menu(debugmenunav)
#breakpointmanager
#currentlinehighlighter
#debugoverlay
#.   pinnable overlay!
#locals
#immediatein