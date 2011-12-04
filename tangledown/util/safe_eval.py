
from __future__ import division
from math import *
from copy import deepcopy
from random import random


safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh',
	'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot',
	'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh',
	'sqrt', 'tan', 'tanh', 'random'] 

safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ]) 
safe_dict['abs'] = abs
safe_dict['int'] = int

def safe_eval(expression, context={}):
	ctxt = deepcopy(context)
	ctxt.update({"__builtins__":None})
	result = eval(expression.strip(), ctxt, safe_dict)
	return result