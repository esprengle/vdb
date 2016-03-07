# coding: utf-8
import ui
import editor
from collections import OrderedDict

from objc_util import *
def expand_icon_path(image):
	os.path.join(os.path.split(__file__)[0],'Icons',image)
btn_dict = OrderedDict((
					('play', 'iob:play_24'),
					('stop', 'iob:stop_24'),
					('up', 'iob:ios7_upload_outline_24'),
					('down', 'iob:ios7_download_outline_24'),
					('step_in', expand_icon_path('debug-step-into-24-000000.png')),
					('step_out', expand_icon_path('debug-step-out-24-000000.png')),
					('step_over', expand_icon_path('debug-step-over-24-000000.png')),
					('watch', 'iow:ios7_glasses_outline_24'),
					('help', 'iow:help_circled_24')))

DEBUGMENUTAG = hash('DEBUGMENU')


@on_main_thread
def create_menu(debugger):
	'''create a menu, and bind to debugger.
	'''
	button_items = []
	for name, imagename in btn_dict.items():
		b = ui.Button(name=name, image=ui.Image.named(imagename))

		action = getattr(debugger, name+'_action', None)
		if callable(action):
			b.action = action
		else:
			b.enabled = False
		button_items.append(b)
	ed = editor._get_editor_tab().editorView()
	w,h = ed.frame().size.width, ed.frame().size.height
	debugmenu = ui.View(frame = (w-44, 0, 44, h),flex='LH')
	y = 10
	for b in button_items:
		b.y = y
		debugmenu.add_subview(b)
		y += b.height + 20
	ObjCInstance(debugmenu).tag = DEBUGMENUTAG
	editor.apply_ui_theme(debugmenu)
	return debugmenu
	

