import pyparsing as pp
from pyparsing import *


class sExpressionParser:
    def __init__(self):
        pass


    def changeOperators(self, expr):
        # replace all substitue over load
        expr = expr.replace('==', ' eq ')
        expr = expr.replace('<>', ' ne ')
        expr = expr.replace('>' , ' gt ')
        expr = expr.replace('>=', ' ge ')
        expr = expr.replace('<' , ' lt ')
        expr = expr.replace('<=', ' le ')
        expr = expr.replace('&&' , ' and ')
        expr = expr.replace('||' , ' or ')
        expr = expr.replace('!=', ' not eq ')
        expr = expr.replace('!', ' not ')
        return expr

    def parseTheExpression(self, expression):
        string = self.changeOperators(expression)
        operator = pp.Regex(r">=|<=|!=|>|<|=|eq").setName("operator")
        variable = pp.Char(pp.alphas)
        identifier = pp.Word(pp.alphas, pp.alphanums + "_")
        and_ = CaselessLiteral("and").setResultsName("Logic")
        or_ = CaselessLiteral("or").setResultsName("Logic")
        not_ = CaselessLiteral("not").setResultsName("Logic")
        logic = [
                (and_, 2, (pp.opAssoc.LEFT),),
                (or_, 2, pp.opAssoc.LEFT,),
                (not_, 1, pp.opAssoc.RIGHT,),
                ]
        comparison_term = (variable | identifier)
        condition = pp.Group(comparison_term("Field") + operator("Operator") + comparison_term("Value"))
        expr = pp.operatorPrecedence(condition("Filters"), logic).setResultsName("Filter")
        pars = expr.parseString(string).dump()
        print pars

if __name__ == "__main__":
    obj = sExpressionParser()
    str = "((a && b) || (c && d))"
    obj.parseTheExpression(str)
