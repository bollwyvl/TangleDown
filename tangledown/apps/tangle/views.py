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

def solve(request, json_system):
    result = {}
    
    sys_def = json.loads(json_system)
    
    symbols = {}
    variables = find_variables(sys_def)
    
    for tv in variables:
        symbols[tv] = sympy.Symbol(tv)
        
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
            result['solution'] = dict(zip(sorted(symbols), map(float, solution[0])))
            result['constraints'] = [c[0] for c in constraints]
            return JsonResponse(result)
        except (NotImplementedError, sympy.DomainError), e:
            pass
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

def find_variables(sys_def):
    found_vars = set()
    for left, right in sys_def.get('constraints',[]) + sys_def.get('suggestions',[]):
        for found in re.finditer(VAR_RE, '%s %s' % (left, right)):
            found_vars.add(str(found.group(1)))
    return found_vars
        