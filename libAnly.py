import sys
import sympy


NUMPY_TRANSLATIONS = {
    'amax': 'max_',
    'amin': 'min_',
    'angle': 'arg',
    'arccos': 'acos',
    'arccosh': 'acosh',
    'arcsin': 'asin',
    'arcsinh': 'asinh',
    'arctan': 'atan',
    'arctan2': 'atan2',
    'arctanh': 'atanh',
    'ceil': 'ceiling',
    'e': 'E',
    'imag': 'im',
    'inf': 'oo',
    'log': 'ln',
    'matrix': 'Matrix',
    'real': 're'}

def getDiff(independentVars, function_string, varsDiff):
    
    diffs = []
    sympyVars = []
    # There is a problem if variables are not a list 
    independentVars = list(independentVars)
    varsDiff = list(varsDiff)
    # Define all the variables as sympy.Symbols
    for v in independentVars:
        sympy.var(v)
    for v in varsDiff:
        sympyVars.append(sympy.var(v))
    # Define the function "f" and change it into a sympy expression
    checkFunction = True
    while checkFunction:
        try:
            f = sympy.simplify(function_string)
            checkFunction = False
        except NameError as inst:
            
            op = inst.message.split("'")[1]
            if op in NUMPY_TRANSLATIONS:
                opNew = "sympy."+NUMPY_TRANSLATIONS[op]
            elif op in dir(sympy):
                opNew = "sympy."+ op
            else:
                print("Warning: %s does not exist in sympy" % op)
                print("No analytical derivatives are used")
                return None
            function_string = function_string.replace(op, opNew)
        except TypeError as inst:
            print inst
            print "You probably used a variable's name which is also a function (i.e. beta, etc)"
            sys.exit()
            
        
     # Do the loop over the variables varsDiff
    for variableToDiff in sympyVars:
        derivative = str(f.diff(variableToDiff))
        
        for var in independentVars:
            if var not in derivative:
                derivative = "%s*log(exp(%s))" % (derivative, var)
        diffs.append(derivative)
    return diffs

if __name__ == "__main__":
    f = 'A*T**(snz)*(1./(1+(T/T0)**(5*(snz-1))))**(1./5)'
    derivList = "A,snz,T0".split(",")
    
    f = "A*x**alpha + Beta"
    derivList = "A, alpha, Beta".split(",")
    derivs = getDiff("x",f, derivList)
    print f
    for d in derivs:
        print d