
import re

def peers_indices(cell, group, inclusive=False):
    """
    cell is a tuple (i, j) and
    group is one of 'row', 'column', 'unit', 'all'
    """
    pass

def parse(puzzle):
    """
    standardize a puzzle string
    """
    nonints = re.compile(r'[^0-9]')
    game = nonints.sub('0', puzzle.replace('\n',''))
    return game

def load(filename, separator):
    """
    Takes the filename of a file with sudoku games
    separated by the separator regex pattern and then
    lazily returns sudoku games one by one in a
    standardized strings
    """

    sep = re.compile(separator, re.MULTILINE)

    fh = open(filename)
    games = fh.read()
    fh.close()

    for game in sep.split(games):
        if game:
            puzzle = parse(game)
            assert(len(puzzle)==81)
            yield puzzle

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
    assert(all([len(row)==9 for row in result]))

    return result

def serialize(puzzle):
    """
    Takes a list of list of string representation of a puzzle and
    return string representation of the puzzle. 1-character-long
    strings mean a cell is set, while longer strings represents
    undetermined cells and are thus converted to zeros
    """
    assert(len(puzzle)==9)
    assert(all([len(row)==9 for row in puzzle]))

    result = str()
    for row in puzzle:
        result += ''.join([str(s) if len(s)==1 else '0' for s in row])
    
    assert(len(result)==81)

    return result

def prettyprint(puzzle):
    """
    Takes a string representation of a puzzle and
    return a pretty print string representation of it. 
    """
    assert(len(puzzle)==81)
    line = 19 * '-'
    result = line
    for i in range(0, 81, 9):
        result += '\n|' + '|'.join(list(puzzle[i:i+9])) + '|\n' + line
    assert(len(result)==379)
    return result

