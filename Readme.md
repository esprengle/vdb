# Visual Debugger(vdb)
  interactive debugger inside pythonista editor

##features
* single stepping, step over, step out
* continue, or quit
* stack up, or stack down
* watch window (view only right now)
* During debugging, current line is highlighted, and editor opens new file if needed
* Stack up/ down buttons
* Create edit menu action to start debugging current script. Point to vdb.py with no arguments to run/debug script, use pm as argument to start post mortem of last traceback.
* Locals window has some primitave capability to modify variables : sequences, dicts, modules, many classes are supported.  Value changed must be eval-able.  Currently window does not update 
* 
##TODO:
- breakpoint set/clear by tapping line #s
- help menu
- optimizations for small devices

## usage (where debugging is needed)
```python
	import vdb
	vdb.set_trace()
```

In addition, the following will begin debugging at the last traceback.

```python
	import vdb
	vdb.pm()
``` 

##install
Thanks to @ywangd for this method.

```python
import requests as r; exec r.get('https://github.com/jsbain/vdb/blob/master/get-vdb.py').text
``` 
