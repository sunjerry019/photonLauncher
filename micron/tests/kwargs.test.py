#!/usr/bin/env python3

def foo(bar, barbar, *args, **kwargs):
	print(bar, barbar)
	foo2(bar=bar, *args, **kwargs)

def foo2(bar, haha):
	print(bar, haha)

a = ["bar", "barbar"]

# foo(a[1] = 1, a[0] = 0)
foo(**{
	a[1] : 1, 
	a[0] : 0,
	"haha": True
})