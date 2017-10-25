from math import factorial, pow
import re
from fractions import Fraction


class Parser:
    def __init__(self, string):
        self.string = string

    def parse(self):
        exponent = re.findall("(?:\^\()(.+\)?)(?:\))", self.string)[0]
        xValue = re.findall("(?:[+,-])[0-9].*(?=x)", self.string)
        constant = re.findall("[0-9](?=[+-])", self.string)[0]
        if len(xValue) == 0:
            xValue = 1
        else:
            xValue = xValue[0]
        if "+" in str(xValue):
            xValue = xValue[1::]
            print(xValue)
        if '/' in exponent:
            ints = exponent.split("/")
            exponent = float(ints[0]) / float(ints[1])
        dictionary = {}
        dictionary['exponent'] = exponent
        dictionary['xValue'] = xValue
        dictionary['constant'] = constant
        return dictionary


class Expander:
    def __init__(self, func, expansionSet):
        self.func = func
        self.expansionSet = int(expansionSet)
        self.constant = float(self.func["constant"])
        self.exponent = float(self.func["exponent"])

    def expand(self):
        result = str(Fraction(pow(self.constant, self.exponent)))
        for i in range(self.expansionSet):
            numerator = self.exponent
            exponentAgain = self.exponent
            xValue = Fraction(float(self.func["xValue"]))
            factori = factorial(i + 1)
            if i != 0:
                for j in range(1, i + 1):
                    numerator *= float("{}".format(str(exponentAgain - j)))
            fraction = Fraction(numerator / factori).limit_denominator(1000)
            constant = Fraction(self.constant)
            exponent = Fraction(xValue, constant) ** (i + 1)
            constant = pow(Fraction(self.constant), self.exponent)
            totalFraction = Fraction(fraction * exponent * constant)
            if totalFraction < 0:
                sign = ""
            else:
                sign = "+"
            if i == 0:
                result += "{sign}{fraction}x".format(fraction=totalFraction, sign=sign)
            else:
                result += "{sign}{fraction}x^{exponent}".format(fraction=totalFraction, exponent=i + 1, sign=sign)
        return result


def runBinomial():
    print("Initializing")
    func = input("Enter function: \n")
    expansionSet = input("Enter how many exponents to expand to: \n")
    p = Parser(func)
    funcParsed = p.parse()
    e = Expander(funcParsed, expansionSet)
    print(e.expand())


runBinomial()
