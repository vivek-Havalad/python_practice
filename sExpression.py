import sys
from enum import Enum
import json

class Type(Enum):
    '''constructor'''
    leftparentheses = 0
    rightparentheses = 1
    operator = 2
    empty = 3
    operand = 4

OPERATORS = {
    "&": "AND",
    "|": "OR",
}

class exp(Exception):
    def __init__(self, e):
        self.ex = e
    def getExp(self):
        return self.ex

def textOperator(string):
    if string not in OPERATORS:
        sys.exit("Unknown operator: " + string)
    return OPERATORS[string]

def typeof(string):
    if string == '(':
        return Type.leftparentheses
    elif string == ')':
        return Type.rightparentheses
    elif string in OPERATORS:
        return Type.operator
    elif string == '=' or string == ' ':
        return Type.empty
    else:
        return Type.operand

def process(tokens,cnt):
    '''Convert infix to prefix expression'''
    stack = []

    while tokens:
        try:
            token = tokens.pop()
        except Exception as e:
            raise exp('Syntax invalid')
        
        category = typeof(token)
        if token == '=':
            try:
                s = stack.pop()
                e = ':'
                n = tokens.pop()
                if n == ' ' or n == ')' or s == ' ' :
                    raise exp('Syntax invalid')
            except Exception as e:
                raise exp('Syntax invalid')
            stack.append(s+e+n)
        if category == Type.operand:
            stack.append(token)
        elif category == Type.operator:
            try:
                stack.append((textOperator(token), stack.pop(), process(tokens, cnt)))
            except Exception as e:
                raise exp('Syntax invalid')
        elif category == Type.leftparentheses:
            cnt['cnt']+=1
            stack.append(process(tokens,cnt))
        elif category == Type.rightparentheses:
            cnt['cnt']-=1
            try:
                return stack.pop()
            except Exception as e:
                raise exp('Syntax invalid')
        elif category == Type.empty:
            continue
    try:
        return stack.pop()
    except Exception as e:
        raise exp('Syntax invalid')

''' Construct Json from expression '''
def getJson(prefixExp, res={}):
    base = prefixExp[0]
    for ch in prefixExp:
       if type(ch) != tuple:
           res.setdefault(ch, [])
           base = ch
       else:
            dic = dict()
            [ls, eq , rs] = ch[1]
            dic1 = dict()
            dic1[ls] = rs
            [ls, eq , rs] = ch[2]
            dic1[ls] = rs
            dic[ch[0]] = dic1
            res[base].append(dic)
    return res

if __name__ == "__main__":
    INFIX = "(( A=5 || B=6) && (C=3 || D=5))"
    ''' Replace all logical expression to bitwise '''
    INFIX = INFIX.replace('&&', '&')
    INFIX = INFIX.replace('||', '|')
    cnt = {'cnt':0}
    try:
        postfix = process(list(INFIX[::-1]), cnt)
    except Exception as e:
        print(e.getExp())
    if type(postfix) != str:
        res = getJson(postfix)
    else:
        print(postfix)
    if cnt['cnt'] != 0:
        print("imbalanced")
    else:
        print({'query': res})
    
