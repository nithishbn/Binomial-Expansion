from math import factorial
import re
from fractions import Fraction


class Parser:
    def __init__(self, string):
        self.string = string

    def parse(self):
        exponent = re.findall("(?:\^\()(.+\)?)(?:\))", self.string)[0]
        xValue = re.findall("(?:[+,-])[0-9].*(?=x)", self.string)[0]
        if "+" in xValue:
            xValue = xValue[1::]
            print(xValue)
        if '/' in exponent:
            ints = exponent.split("/")
            exponent = float(ints[0]) / float(ints[1])
        dictionary = {}
        dictionary['exponent'] = exponent
        dictionary['xValue'] = xValue
        return dictionary


class Expander:
    def __init__(self, func, expansionSet):
        self.func = func
        self.expansionSet = int(expansionSet)

    def expand(self):
        result = "1"

        for i in range(self.expansionSet):
            numerator = float(self.func["exponent"])
            factori = factorial(i + 1)
            if i == 0:
                numerator = float(self.func["exponent"])
            else:
                for j in range(1, i + 1):
                    numerator *= float("{}".format(str(float(self.func["exponent"]) - j)))
                    print("Loop numerator:", numerator)
            fraction = numerator / factori
            fraction = Fraction(fraction)
            exponent = Fraction(self.func["xValue"]) ** (i + 1)
            totalFraction = fraction * exponent
            print("Fraction: ", fraction)
            if totalFraction < 0:
                sign = ""
            else:
                sign = "+"
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
