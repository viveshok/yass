
import unittest

class TestLoad(unittest.TestCase):

    def test_load(self):

        games1 = load('test1.txt', r'Grid \d+\n')

"Grid 01  "
"003020600"
"900305001"
"001806400"
"008102900"
"700000008"
"006708200"
"002609500"
"800203009"
"005010300"
"Grid 02  "
"200080300"
"060070084"
"030500209"
"000105408"
"000000000"
"402706000"
"301007040"
"720040060"
"004010003"

        games1 = load('test2.txt', r'\n')

"4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
"52...6.........7.13...........4..8..6......5...........418.........3..2...87....."
