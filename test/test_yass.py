
import sys
import unittest

sys.path.append('../yass')

from yass import yass

class TestYass(unittest.TestCase):

    def test_parse(self): 
        puzzle = "003020600\n900305001\n001806400\n008102900\n700000008\n006708200\n002609500\n800203009\n005010300\n"
        expected = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"
        self.assertEqual(yass.parse(puzzle), expected)

        puzzle = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
        expected = "400000805030000000000700000020000060000080400000010000000603070500200000104000000"
        self.assertEqual(yass.parse(puzzle), expected)

    def test_load(self):


        games1 = yass.load('test/test1.txt', r'Grid\s\d+\n')
        self.assertEqual(next(games1), "003020600900305001001806400008102900700000008006708200002609500800203009005010300")
        self.assertEqual(next(games1), "200080300060070084030500209000105408000000000402706000301007040720040060004010003")

        games2 = yass.load('test/test2.txt', r'\n')
        self.assertEqual(next(games2), "400000805030000000000700000020000060000080400000010000000603070500200000104000000")
        self.assertEqual(next(games2), "520006000000000701300000000000400800600000050000000000041800000000030020008700000")

    def test_deserialize(self):
        deserialized = yass.deserialize("200080300060070084030500209000105408000000000402706000301007040720040060004010003")
        expected = [
                       ['2', '0', '0', '0', '8', '0', '3', '0', '0'],
                       ['0', '6', '0', '0', '7', '0', '0', '8', '4'],
                       ['0', '3', '0', '5', '0', '0', '2', '0', '9'],
                       ['0', '0', '0', '1', '0', '5', '4', '0', '8'],
                       ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
                       ['4', '0', '2', '7', '0', '6', '0', '0', '0'],
                       ['3', '0', '1', '0', '0', '7', '0', '4', '0'],
                       ['7', '2', '0', '0', '4', '0', '0', '6', '0'],
                       ['0', '0', '4', '0', '1', '0', '0', '0', '3'],
                   ]

        self.assertEqual(deserialized, expected)

    def test_serialize(self):
        puzzle1 = [
                       ['2', '0', '0', '0', '8', '0', '3', '0', '0'],
                       ['0', '6', '0', '0', '7', '0', '0', '8', '4'],
                       ['0', '3', '0', '5', '0', '0', '2', '0', '9'],
                       ['0', '0', '0', '1', '0', '5', '4', '0', '8'],
                       ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
                       ['4', '0', '2', '7', '0', '6', '0', '0', '0'],
                       ['3', '0', '1', '0', '0', '7', '0', '4', '0'],
                       ['7', '2', '0', '0', '4', '0', '0', '6', '0'],
                       ['0', '0', '4', '0', '1', '0', '0', '0', '3'],
                 ]

        serialized = yass.serialize(puzzle1)
        expected = "200080300060070084030500209000105408000000000402706000301007040720040060004010003"
        self.assertEqual(serialized, expected)

        puzzle2 = [
                    ['2', 'xxx', 'xx', 'xx', '8', 'xxxx', '3', 'xxx', 'aaaa'],
                    ['kj', '6', 'akdfj', 'ahdf', '7', 'ajs', 'dkjf', '8', '4'],
                    ['skj', '3', 'dks', '5', 'dkf', 'adkf', '2', 'aldkf', '9'],
                    ['dsa', 'dfj', 'dfk', '1', 'djks', '5', '4', 'dsj', '8'],
                    ['sk', 'kdf', 'dk', 'df', 'dkf', 'skd', 'dkj', 'lf', 'dj'],
                    ['4', 'kdk', '2', '7', 'jkf', '6', 'jdf', 'jkdf', 'kdjfs'],
                    ['3', 'kdj', '1', 'jkk', 'kdjf', '7', 'dfjk', '4', 'jdf'],
                    ['7', '2', 'kjfj', 'klk', '4', 'kdf', 'kdjd', '6', 'dfjk'],
                    ['?~:+_', 'kjd', '4', 'kdd', '1', 'kjf', 'kd', 'dfj', '3'],
                 ]

        serialized = yass.serialize(puzzle2)
        self.assertEqual(serialized, expected)

    def test_prettyprint(self):

        puzzle = "200080300060070084030500209000105408000000000402706000301007040720040060004010003"

        line = 19 * '-'
        expected = line
        expected += '\n' + "|2|0|0|0|8|0|3|0|0|" + '\n' + line
        expected += '\n' + "|0|6|0|0|7|0|0|8|4|" + '\n' + line
        expected += '\n' + "|0|3|0|5|0|0|2|0|9|" + '\n' + line
        expected += '\n' + "|0|0|0|1|0|5|4|0|8|" + '\n' + line
        expected += '\n' + "|0|0|0|0|0|0|0|0|0|" + '\n' + line
        expected += '\n' + "|4|0|2|7|0|6|0|0|0|" + '\n' + line
        expected += '\n' + "|3|0|1|0|0|7|0|4|0|" + '\n' + line
        expected += '\n' + "|7|2|0|0|4|0|0|6|0|" + '\n' + line
        expected += '\n' + "|0|0|4|0|1|0|0|0|3|" + '\n' + line

        self.assertEqual(yass.prettyprint(puzzle), expected)

#    def test_peers_indices():
#
#        observed = yass.peers_indices((0, 3), 'row')
#        expected = [(0, 0), (0, 1), (0, 2), (0, 4),
#                        (0, 5), (0, 6), (0, 7), (0, 8)]
#
#        self.assertEquals(observed, expected)
#
#        observed = yass.peers_indices((0, 3), 'row', True)
#        expected = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
#                        (0, 5), (0, 6), (0, 7), (0, 8)]
#
#        self.assertEquals(observed, expected)
#
#        observed = yass.peers_indices((7, 1), 'column', True)
#        expected = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
#                        (5, 1), (6, 1), (7, 1), (8, 1)]
#
#        observed = yass.peers_indices((7, 1), 'column', False)
#        expected = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
#                        (5, 1), (6, 1), (8, 1)]
#
#        self.assertEquals(observed, expected)
      

if __name__ == '__main__':
    unittest.main()

