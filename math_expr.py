import re

def calc(expression):
    print(expression)
    EXPR, CLEAN_STR, STACK, PSTFX, NUMS = expression, '', [], [], map(lambda n : str(n), list(range(0,10)))
    
    class Operator():
        def __init__(self, prec, calc):
            self.prec = prec
            self.calc = calc
    
    OPR = {
        "+": Operator( 1, lambda a,b: a+b ),
        "-": Operator( 1, lambda a,b: a-b ),
        "/": Operator( 2, lambda a,b: a/b ),
        "*": Operator( 2, lambda a,b: a*b ),
    }
    
    # CLEANING STEP :
    
    EXPR = EXPR.replace(' ','')

    for i, char in enumerate(EXPR):
        if i == 0:
            if char == '-':
                if EXPR[ i+1 ] == '(':
                    CLEAN_STR += '-1 *'
                else: 
                    CLEAN_STR += '-'
            else:
                CLEAN_STR += char
    
        else :
    
            if re.compile("[\+\*/\(\)]").match(char):
                CLEAN_STR += ' ' + char
            
            else:
                
                if re.compile("[\d]").match(char):
    
                    if ( re.compile("[\d\.]").match( EXPR[ i-1 ] ) 
                    or ( i == 1 and EXPR[0] == '-' ) 
                    or (i - 2 >= 0 and re.compile("[\+\-\*\(/]\-\d").match(
                        EXPR[i-2] + EXPR[i-1] + EXPR[i]) ) 
                    ):
                        CLEAN_STR += char
    
                    else:
                        CLEAN_STR += ' ' + char
                else:

                    if EXPR[ i+1 ] == "(":

                        if re.compile('[\(\-\+]').match(EXPR[ i-1 ]):
                            CLEAN_STR += " -1 *"

                        elif re.compile('[\d\)]').match(EXPR[ i-1 ]):
                            CLEAN_STR += " + -1 *"

                        elif EXPR[i-1] == '/':
                            CLEAN_STR = CLEAN_STR[:-1]
                            CLEAN_STR += '* -1 /'

                        elif EXPR[i-1] == "*":
                            CLEAN_STR += ' -1 *'
                        
                    else:
                        CLEAN_STR += ' ' + char
    
    CLEAN_STR = CLEAN_STR.split(' ')
    
    # POSTFIX FORMATING STEP
    
    for char in CLEAN_STR:
    
        if len(char) > 1 or re.compile('[\d]').match(char):
        
            PSTFX.append( char )
        
        else:
            if char == '(':
                STACK.append('(')
    
            elif char == ')':
                while STACK[-1] != '(':
                    PSTFX.append(STACK.pop())
                STACK.pop()
            
            else:

                if len(STACK) == 0 or STACK[-1] == '(':
                    STACK.append( char )

                else:
                    if OPR[ char ].prec > OPR[ STACK[ -1 ] ].prec:
                        STACK.append( char )
                    else: 

                        while len(STACK) > 0 and STACK[-1] != '(' and OPR[char].prec <= OPR[ STACK[ -1 ] ].prec:
                            PSTFX.append( STACK.pop() )

                        STACK.append( char )
    
    while len(STACK) > 0:
    
        PSTFX.append( STACK.pop() )
    
    # EXPRESSION EVALUATING STEP:
    
    for char in PSTFX:
    
        if not char in OPR:
    
            STACK.append( float( char ) )
    
        else:
            if len(STACK) > 1:
                r , l = STACK.pop() , STACK.pop()
                STACK.append( OPR[ char ].calc( l , r ) ) 
    
    res = STACK.pop()
    if res == int(res):
        res = int(res)
    
    return res

print(calc('-7 * -(6 / 3)'))