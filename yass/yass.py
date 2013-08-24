
import re

def explode(puzzle):
    pass

def is_solved(puzzle):
    pass

def is_valid(puzzle):
    pass

def propagate_constraint(puzzle):
    pass

def constraint_propagation(puzzle):
    pass

def solve(puzzle_str):
    
    assert(len(puzzle_str)==81)
    puzzle = explode(deserialize(puzzle_str))
    assert(is_valid(puzzle))
    puzzle = constraint_propagation(puzzle)

    if not is_valid(puzzle):
        return False
    elif is_solved(puzzle):
        return serialize(puzzle)
    else:
        flattened = [(len(s), s) if len(s)>1 else (10, False) for s in row for row in puzzle]
        assert(len(flattened)==81)
        index, possible_values = min(flattened)
        assert(0<=index<81)
        assert(len(possible_values)>1)
        for possible_value in possible_values:
            result = solve(puzzle_str[:index] + possible_value + puzzle_str[index+1:])
            if result:
                return result

        return False
            
def peers_indices_row(cell):
    """
    returns the indices of cells who share same row
    """
    (r, c) = cell
    return {(r, i) for i in range(9)}

def peers_indices_column(cell):
    """
    returns the indices of cells who share same column
    """
    (r, c) = cell
    return {(i, c) for i in range(9)}

def peers_indices_unit(cell):
    """
    returns the indices of cells who share same unit
    """
    bins = lambda x: x//3*3
    (r, c) = cell
    return {(i, j) for i in range(bins(r), bins(r)+3) for j in range(bins(c), bins(c)+3)}

def peers_indices(cell, group, inclusive=False):
    """
    cell is a tuple (i, j) and
    group is one of 'row', 'column', 'unit', 'all'
    """
    if group == 'row':
        result = peers_indices_row(cell)
    elif group == 'column':
        result = peers_indices_column(cell)
    elif group == 'unit':
        result = peers_indices_unit(cell)
    elif group == 'all':
        result = peers_indices_row(cell)
        result |= peers_indices_column(cell)
        result |= peers_indices_unit(cell)

    if not inclusive:
        result.remove(cell)

    return result

def peers(cell, puzzle, group):
    """
    given a cell (i,j), a puzzle in the list of
    list of string representation, and a group
    (one of 'row', 'column', 'unit' or 'all'),
    return a set of the content of the peers
    cells of that group of that puzzle of that
    cell
    """
    return {puzzle[i][j] for (i, j) in peers_indices(cell, group)}

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

