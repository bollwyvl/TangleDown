import re

import sympy

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext
from django.utils import simplejson as json

from util.shortcuts import context_response
from util.safe_eval import safe_eval
from util.json_response import JsonResponse

def syntax(request):
    ctxt = {}
    return context_response(request, 'tangle/syntax.html', ctxt)

def solve(request, json_system):
    result = {}
    
    sys_def = json.loads(json_system)
    
    symbols = {}
    variables = find_variables(sys_def)
    
    for tv, args in variables.items():
        symbols[tv] = sympy.Symbol(tv, **args)
        
    eq_sys = []
    for left, right in sys_def.get('constraints',[]) + sys_def.get('suggestions',[]):
        new_left, new_right = [str(x).replace('#','') for x in [left,right]]
        eq_sys.append(((left, right), safe_eval('%s - (%s)' % (new_left, new_right), symbols)))
    
    solution = None
    
    num_constraints = len(eq_sys)
    while num_constraints:
        constraints = eq_sys[0:num_constraints]
        try:
            solution = sympy.solve([c[1] for c in constraints], symbols.values())
            if not solution:
                raise sympy.DomainError
            result['solution'] = dict(zip(sorted(symbols), solution[0]))
            result['constraints'] = [c[0] for c in constraints]
            return JsonResponse(result)
        except (NotImplementedError, sympy.DomainError), e:
            print e
        num_constraints -= 1
    """
    except NotImplementedError, e:
        suggestion = {}
        for constraint, g in eq_sys.items():
            poly = g.as_poly(*symbols.values(), **{'extension': True})
            if poly is None:
                msg = 'Try simplifying: '
                if '/' in ''.join(constraint):
                    msg += 'Removing division might help.'
                suggestion['%s: %s' % constraint] = msg
                
        result = dict(
            error='Unsolveable',
            suggestion=suggestion,
            constraints=sys_def,
            )
    except sympy.DomainError, e:
        result = dict(
            error='Unsolveable',
            suggestion=e.message,
            constraints=sys_def
            )
    """
    
    return JsonResponse(result)

VAR_RE = re.compile(r'#([a-z\d_]*)', re.I)
INT_RE = re.compile(r'^\s*\-?\d+\s*$')
FLT_RE = re.compile(r'^\s*\-?(\d+\.\d+|\.\d+|\d+\.)\s*$')

def find_variables(sys_def):
    found_vars = {}
    for left, right in sys_def.get('constraints',[]) + sys_def.get('suggestions',[]):
        for found in re.finditer(VAR_RE, '%s %s' % (left, right)):
            var = str(found.group(1))
            var_type_args = {}
            
            # are they telling me somthing? left-hand assignment 
            # with a simple right-hand probably means something            
            if '#%s' % var == left:
                if isinstance(right, str) or isinstance(right, unicode):
                    if INT_RE.match(right):
                        var_type_args = {'integer':True}
                    elif FLT_RE.match(right):
                        var_type_args = {'float':True}
                        
                elif isinstance(right, float):
                    var_type_args = {'float':True}
                elif isinstance(right, int):
                    var_type_args = {'integer':True}
                    
            found_vars[var] = var_type_args
    return found_vars
        