from math import gcd

class Fraction:
    def __init__(self, numerator: int, denominator: int):
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        g = gcd(numerator, denominator)
        self.numerator = numerator // g
        self.denominator = denominator // g
        # Keep denominator positive
        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

    def add(self, other: 'Fraction') -> 'Fraction':
        num = self.numerator * other.denominator + other.numerator * self.denominator
        den = self.denominator * other.denominator
        return Fraction(num, den)

    def multiply(self, other: 'Fraction') -> 'Fraction':
        return Fraction(
            self.numerator * other.numerator,
            self.denominator * other.denominator
        )

    def __eq__(self, other):
        if not isinstance(other, Fraction):
            return NotImplemented
        return (self.numerator == other.numerator and
                self.denominator == other.denominator)

    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"
