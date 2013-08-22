
import re

def load(filename, separator):
    """
    Takes the filename of a file with sudoku games
    separated by the separator regex pattern and then
    lazily returns sudoku games one by one in a
    standardized strings
    """

    sep = re.compile(separator, re.MULTILINE)
    nonints = re.compile(r'[^0-9]')

    fh = open(filename)
    games = fh.read()
    fh.close()

    for game in sep.split(games):
        if game:
            game = nonints.sub('0', game.replace('\n',''))
            assert(len(game)==81)
            yield game

def deserialize(puzzle):
    """
    Takes the serialized string representation of a puzzle and
    return a list of list of string representation of the puzzle
    """
    assert(len(puzzle)==81)
    result = list()
    for i in range(0, 81, 9):
        result.append(list(puzzle[i:i+9]))
    assert(len(result)==9)
    return result

