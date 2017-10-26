from math import factorial, pow
import re
from fractions import Fraction
import sys

import time


class Parser:
    def __init__(self, string):
        self.string = string

    def parse(self):
        exponent = re.findall("(?:\^\()(.+\)?)(?:\))", self.string)[0]
        xValue = re.findall("(?:[+,-])[0-9].*(?=x)", self.string)
        constant = re.findall("[0-9](?=[+-])", self.string)[0]
        potentialMultiplier = re.findall(".*[0-9](?=\()", self.string)
        if len(potentialMultiplier) == 0:
            potentialMultiplier = 1
        else:
            potentialMultiplier = potentialMultiplier[0]
        if len(xValue) == 0:
            xValue = 1
        else:
            xValue = xValue[0]
        if "+" in str(xValue):
            xValue = xValue[1::]
            # print(xValue)
        if '/' in exponent:
            ints = exponent.split("/")
            exponent = float(ints[0]) / float(ints[1])
        dictionary = {}
        dictionary['exponent'] = exponent
        dictionary['xValue'] = xValue
        dictionary['constant'] = constant
        dictionary['potentialMultiplier'] = potentialMultiplier
        return dictionary


class Expander:
    def __init__(self, func, expansionSet):
        self.func = func
        if len(expansionSet) == 0:
            self.expansionSet = 0
        else:
            self.expansionSet = int(expansionSet)
        self.constant = float(self.func["constant"])
        self.exponent = float(self.func["exponent"])
        self.xValue = float(self.func["xValue"])
        self.potentialMultiplier = float(self.func["potentialMultiplier"])
        if self.exponent < 0:
            print("Route 1")
            print(self.expand())
        else:
            print("route 2")
            print(self.binomialExpand())

    def expand(self):
        potentialMultiplier = Fraction(self.potentialMultiplier)
        result = str(Fraction(potentialMultiplier * pow(self.constant, self.exponent)))
        for i in range(self.expansionSet):
            numerator = self.exponent
            exponentAgain = self.exponent
            xValue = Fraction(self.func["xValue"])
            factori = factorial(i + 1)
            constant = Fraction(self.constant)
            if i != 0:
                for j in range(1, i + 1):
                    numerator *= float("{}".format(str(exponentAgain - j)))
            fraction = Fraction(numerator / factori).limit_denominator(1000)

            exponent = Fraction(xValue, constant) ** (i + 1)
            constant = pow(Fraction(self.constant), self.exponent)
            totalFraction = Fraction(potentialMultiplier * fraction * exponent * constant).limit_denominator(1000)
            if totalFraction < 0:
                sign = ""
            else:
                sign = "+"
            if i == 0:
                result += "{sign}{fraction}x".format(fraction=totalFraction, sign=sign)
            else:
                result += "{sign}{fraction}x^{exponent}".format(fraction=totalFraction, exponent=i + 1, sign=sign)
        return result

    def binomialExpand(self):
        result = ""
        j = 0
        for i in range(int(self.exponent), 0, -1):
            ncr = self.ncr(i, j)
            multiplied = ncr * pow(self.constant, i) * pow(self.xValue, j)
            multiplied = Fraction(multiplied)
            if i == int(self.exponent):
                result += str("{value}x^{exponent}".format(value=multiplied, exponent=j))
            else:
                result += str("+{value}x^{exponent}".format(value=multiplied, exponent=j))
            j += 1
        return result

    def ncr(self, n, k):
        ret = 0
        if n == k:
            ret = 1
        elif k == 1:
            ret = n
        else:
            a = factorial(n)
            b = factorial(k)
            c = factorial(n - k)
            ret = a // (b * c)
        return ret


def runBinomial():
    func = input("Enter function: \n")
    expansionSet = input("Enter how many exponents to expand to or leave blank for regular binomial expansion: \n")
    p = Parser(func)
    funcParsed = p.parse()
    e = Expander(funcParsed, expansionSet)
    # print(e.expand())
    print()


print("Welcome!")
while True:
    try:
        runBinomial()
    except KeyboardInterrupt:
        print("Good bye? :(")
        time.sleep(2)
        sys.exit()
    except IndexError:
        print()
        print("Your format was incorrect!")
        print("Make sure you format it this way: a(b+cx)^(d) where 'a' is optional if it's a 1")
        continue
