# Visual Debugger(vdb)
  interactive debugger inside pythonista editor

##features
* single stepping, or step over
* continue, or quit
* watch window (view only right now)
* During debugging, current line is highlighted, and editor opens new file if needed

##TODO:
- breakpoint set/clear by tapping line s
- launch script via menu
- stack up/down 
- help menu
- optimizations for small devices

## usage (where debugging is needed)
```python
	import vdb
	vdb.VDB().set_trace()
	
```
