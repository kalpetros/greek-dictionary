import os
import shutil


def diceware(words):
    """
    Build the diceware list
    """
    results = []
    results_numbered = []

    with open('files/dicewarekit.txt', 'r') as file:
        for word in file:
            results.append(word.strip())

    for word in words:
        if len(word) > 3 and len(word) < 7:
            results.append(word)

    results.sort()

    inc_p2 = inc_p3 = inc_p4 = inc_p5 = 1
    itr_p2 = itr_p3 = itr_p4 = itr_p5 = 0
    for index, word in enumerate(results):
        if itr_p2 % 6 == 0:
            inc_p2 = inc_p2 + 6 + 1

        if itr_p3 % 6**2 == 0:
            inc_p3 = inc_p3 + 6**2 + 1

        if itr_p4 % 6**3 == 0:
            inc_p4 = inc_p4 + 6**3 + 1

        if itr_p5 % 6**4 == 0:
            inc_p5 = inc_p5 + 6**4 + 1

        if (itr_p2 % 6**2 == 0):
            itr_p2 = 0
            inc_p2 = 1

        if (itr_p3 % 6**3 == 0):
            itr_p3 = 0
            inc_p3 = 1

        if (itr_p4 % 6**4 == 0):
            itr_p4 = 0
            inc_p4 = 1

        if (itr_p5 % 6**5 == 0):
            itr_p5 = 0
            inc_p5 = 1

        p1 = index % 6 + 1  # resets every 6
        p2 = (itr_p2 % 6) + inc_p2 - itr_p2  # resets every 6^2 = 36
        p3 = (itr_p3 % 6**2) + inc_p3 - itr_p3  # resets every 6^3 = 216
        p4 = (itr_p4 % 6**3) + inc_p4 - itr_p4  # resets every 6^4 = 1296
        p5 = (itr_p5 % 6**4) + inc_p5 - itr_p5  # resets every 6^5 = 7776

        itr_p2 = itr_p2 + 1
        itr_p3 = itr_p3 + 1
        itr_p4 = itr_p4 + 1
        itr_p5 = itr_p5 + 1

        combinations = f'{p5}{p4}{p3}{p2}{p1}'
        results_numbered.append(f'{combinations}    {word}')

    return results, results_numbered
