# coding: utf-8
import ui,editor

def test():
	import vdb
	vdb.set_trace()
	# create some variables to try watch window
	a=1
	b={'key':{'b':['c','d','e']},'anotherkey':'anothervalue'}
	c='a string'
	#test stepping over
	test2()
	# step into anothe file
	editor.get_path()
	return 10
def test2():
	d=1
	print(d)
	test3()
@ui.in_background
def test3():
	d=2
test()
b=9
