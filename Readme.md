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
##install
Thanks to @ywangd for this method.

```python
import requests as r; exec r.get('https://raw.githubusercontent.com/jsbain/vdb/master/get_vdb.py').text
``` 
