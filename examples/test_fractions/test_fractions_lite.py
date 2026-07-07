from fractions_lite import Fraction

def test_reduction():
    assert Fraction(2, 4) == Fraction(1, 2)

def test_addition():
    assert Fraction(1, 2).add(Fraction(1, 3)) == Fraction(5, 6)

def test_multiplication():
    assert Fraction(1, 2).multiply(Fraction(2, 3)) == Fraction(1, 3)
