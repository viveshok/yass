
import re
import copy

def explode(puzzle):
    """
    take a list of list of chars representation'
    of a sudoku puzzle and replace any '0' it
    encounters with '123456789'
    """
    assert(is_valid(puzzle))
    result = list()
    for row in puzzle:
        result.append(['123456789' if cell=='0' else cell for cell in row])
    return result

def well_formed(puzzle):
    if len(puzzle)==9:
        for row in puzzle:
            if len(row)!=9:
                return False
        return True
    else:
        return False

def follow_rules(puzzle):

    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    # make sure no row has duplicates
    for row in puzzle:
        set_cells = [c for c in row if c in values]
        if len(set(set_cells))!=len(set_cells):
            return False

    # make sure no column has duplicates
    for j in range(9):
        set_cells = [puzzle[i][j] for i in range(9) if puzzle[i][j] in values]
        if len(set(set_cells))!=len(set_cells):
            return False

    # make sure no unit has duplicates
    for i in [0, 3, 6]:
        for j in [0, 3, 6]:
            set_cells = [
                            puzzle[m][n]
                            for m in range(i, i+3)
                            for n in range(j, j+3)
                            if puzzle[m][n] in values
                        ]
            if len(set(set_cells))!=len(set_cells):
                return False

    # make sure no cell is empty
    if any([not cell for row in puzzle for cell in row]):
        return False

    return True

def is_valid(puzzle):
    """
    check if a sudoku puzzle is well formed, and doesn't
    break any rule
    """
    return well_formed(puzzle) and follow_rules(puzzle)

def is_solved(puzzle):
    """
    check if a sudoku puzzle in the list of list of string
    representation is solved or not
    """

    if not is_valid(puzzle):
        return False

    values = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

    # make sure all rows have all needed values
    for row in puzzle:
        if set(row)!=values:
            return False

    # make sure all columns have all needed values
    for j in range(9):
        if {puzzle[i][j] for i in range(9)} != values:
            return False

    # make sure all units have all needed values
    for i in [0, 3, 6]:
        for j in [0, 3, 6]:
            cells = {
                        puzzle[m][n]
                        for m in range(i, i+3)
                        for n in range(j, j+3)
                    }
            if cells != values:
                return False

    return True

def remove_impossibles(cell, puzzle):
    """
    takes a cell and a puzzle, remove realizations
    that are impossible for that cell to take because
    they are already taken by its peers, and return
    a string with possible realization for this cell
    """
    (i, j) = cell
    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    peers_ = {cell for cell in peers(cell, puzzle, 'all') if cell in values}
    result = ''.join(set(puzzle[i][j])-peers_)
    return result

def coerce_compelled(cell, puzzle):
    """
    takes a cell and a puzzle, and checks if that
    cell has a possible realization it is the only
    cell amongst its row peers, column peers or
    unit peers who can take that realization. If
    yes return that value, otherwise return initial
    string with possible values for that cell
    """

    # row
    (i, j) = cell
    peers_row = {x for c in peers(cell, puzzle, 'row') for x in c}
    diff = set(puzzle[i][j]) - peers_row
    if len(diff)==1:
        return ''.join(diff)

    # column
    (i, j) = cell
    peers_column = {x for c in peers(cell, puzzle, 'column') for x in c}
    diff = set(puzzle[i][j]) - peers_column
    if len(diff)==1:
        return ''.join(diff)

    # unit
    (i, j) = cell
    peers_unit = {x for c in peers(cell, puzzle, 'unit') for x in c}
    diff = set(puzzle[i][j]) - peers_unit
    if len(diff)==1:
        return ''.join(diff)

    return puzzle[i][j]

def propagate_constraint(puzzle):
    """
    one pass of constraint propagation for all cells
    """
    result = copy.deepcopy(puzzle)
    for i in range(9):
        for j in range(9):
            result[i][j] = remove_impossibles((i, j), result)
            result[i][j] = coerce_compelled((i, j), result)

    return result

def constraint_propagation(puzzle_str):
    """
    keep doing passes of constraint propagation
    till the puzzle is not changing any more
    """
    puzzle = explode(deserialize(puzzle_str))
    assert(is_valid(puzzle))

    different = True
    while different:
        puzzle = propagate_constraint(puzzle)
        serialized = serialize(puzzle)
        different = serialized != puzzle_str
        puzzle_str = serialized

    return puzzle

def solve_sudoku(grid):

    if not well_formed(grid):
        return None

    result = solve(serialize(grid))
    if result:
        result = deserialize(result)
        for row in result:
            row = [int(c) for c in row]

    return result

def solve(puzzle_str):
    
    assert(len(puzzle_str)==81)
    puzzle = constraint_propagation(puzzle_str)

    if not is_valid(puzzle):
        return False
    elif is_solved(puzzle):
        return serialize(puzzle)
    else:
        flattened = [
                        (len(s), s, 9*i+j)
                        if len(s)>1
                        else (10, False, 9*i+j)
                        for i, row in enumerate(puzzle)
                        for j, s in enumerate(row)
                    ]

        assert(len(flattened)==81)
        num_val, possible_values, index = min(flattened)
        assert(0<=index<81)
        assert(len(possible_values)>1)
        for possible_value in possible_values:
            trial = puzzle_str[:index] + possible_value + puzzle_str[index+1:]
            result = solve(trial)
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
    return {
                (i, j)
                for i in range(bins(r), bins(r)+3)
                for j in range(bins(c), bins(c)+3)
           }

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
    return a list of the content of the peers
    cells of that group of that puzzle of that
    cell
    """
    return [puzzle[i][j] for (i, j) in peers_indices(cell, group)]

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
        result += ''.join([str(s) if len(str(s))==1 else '0' for s in row])
    
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

