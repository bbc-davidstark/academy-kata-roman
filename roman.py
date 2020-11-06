#!/usr/bin/env python
# Test: pytest roman.py
# Run: ./roman.py <numeral string>
import sys
import pytest

numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def is_five_num(n):
    x = numerals[n]
    while x >= 10:
        x = x // 10
    if x == 5:
        return True
    else:
        return False


def scan_numeral(l):
    if l[0] not in numerals:
        raise Exception("Bad numeral in input")


def scan_numeral_rep(l):
    if len(l) < 4:
        return
    t = []
    for i in range(4):
        t.append(l[i])
    if len(set(t)) == 1:
        raise Exception("Numeral repeated >3 times")


def scan_five_rep(l):
    if len(l) < 2:
        return
    if is_five_num(l[0]) and is_five_num(l[1]):
        raise Exception("Repeated five-number")


def scan(l):
    if not l:
        return
    for key, f in globals().items():
        if callable(f) and f.__module__ == __name__ and key.startswith("scan_"):
            f(l)
    l.pop(0)
    scan(l)


# returns next (value, subtracted_num, remaining list)
def next_atom(l):
    if len(l) == 1:
        return (numerals[l[0]], None, None)
    if numerals[l[0]] >= numerals[l[1]]:
        return (numerals[l.pop(0)], None, l)
    else:
        a_numeral = l.pop(0)
        if is_five_num(a_numeral):
            raise Exception("Five-number used to subtract")
        a = numerals[a_numeral]
        b = numerals[l.pop(0)]
        if b > (10 * a):
            # You can only subtract a unit from next highest five/unit
            raise Exception("Attempted to subtract from too high a numeral")
        return (b - a, a, l)


def main(input):

    scan(list(input))

    l = list(input)
    number = 0
    value = None
    sub = None
    while l:
        prev_value = value
        prev_sub = sub
        (value, sub, l) = next_atom(l)
        if prev_value and value > prev_value:
            # You can only subtract a single unit
            # Except for subtractions, all digits are in nonincreasing order
            raise Exception(
                "Numbers not decreasing left to right, or multiple subtractions"
            )
        if prev_sub and value >= prev_sub:
            # You can’t subtract and add units to same number
            raise Exception("Attempted to add to a previously subtracted-from numeral")
        number = number + value
    return number


if __name__ == "__main__":
    print(str(main(sys.argv[1])))


def test_repeated_numeral():
    with pytest.raises(Exception):
        main("IIII")
    with pytest.raises(Exception):
        main("XIIII")


def test_repeated_five():
    with pytest.raises(Exception):
        main("VV")
    with pytest.raises(Exception):
        main("LL")
    with pytest.raises(Exception):
        main("DD")


def test_subtract_unit():
    with pytest.raises(Exception):
        main("IL")
    with pytest.raises(Exception):
        main("MIL")


def test_sub_and_add():
    with pytest.raises(Exception):
        main("IXI")
    with pytest.raises(Exception):
        main("IXIX")


def test_increasing_order():
    with pytest.raises(Exception):
        main("IXCM")


def test_nonsense():
    with pytest.raises(Exception):
        main("Romanes eunt domus")


def test_invalid():
    with pytest.raises(Exception):
        main("ABCDE")


def test_malformed():
    with pytest.raises(Exception):
        main("ICXXXXIIVV")


def test_ok():
    assert main("I") == 1
    assert main("MDCCCLXXXVIII") == 1888
    assert main("MMMCMXCIX") == 3999
