
import re


def line_score_to_ints(s: str) -> list[int]:
    """
    The line score for a game is stored as a string, one character for
    each inning, except for the case where the team scored more than 9
    runs. In that case, the inning is represented as "(nn)", where 'nn'
    is the number of runs scored.
    Example: 000320(12)10 (They scored 12 in the 7th.)
    The string will end with 'x' if the home team didn not bat in the 9th.

    Convert this string into a list of integers, one for each inning.
    Remove that 'x' before converting.
    """
    if s.endswith('x'):
        s = s[0:-1]
    count = s.count('(')
    if count == 0:
        return [int(c) for c in s]

    if s.count('(') > 1:
        print('Bad line score:', s)
        assert False

    pat = '([0-9]*)(\(..\))([0-9]*)$'
    p = re.compile(pat)
    m = p.match(s)
    if not m:
        print('Bad line score:', s)
        assert False
    else:
        s1 = m.group(1)  # just digits
        s2 = m.group(2)  # parenthesized
        s3 = m.group(3)  # just digits
        if len(s1) > 0:
            list1 = [int(c) for c in s1]
        else:
            list1 = []
        if len(s3) > 0:
            list3 = [int(c) for c in s3]
        else:
            list3 = []
        list2 = [int(s2[1:3])]
        return list1 + list2 + list3


if __name__ == '__main__':
    s = '123456789'
    print(s, '->', line_score_to_ints(s))
    s = '123(15)56789'
    print(s, '->', line_score_to_ints(s))
    s = '(15)23456789'
    print(s, '->', line_score_to_ints(s))
    s = '12345678(15)'
    print(s, '->', line_score_to_ints(s))
    s = '1(15)345678x'
    print(s, '->', line_score_to_ints(s))
    print('FAIL:')
    s = '123(12)5678(12)'
    print(s, '->', line_score_to_ints(s))