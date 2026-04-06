from unittest import TestCase

from mancala_logic import MancalaBoard

class MancalaLogicTestCase(TestCase):
    def setUp(self):
        self.board = MancalaBoard()

class ConstructSideTestCase(MancalaLogicTestCase):
    def test_construct_side_default(self):
        """test that it constructs a board using various parameters"""
        side = self.board.construct_side(6,4)
        
        self.assertTrue(isinstance(side, list))
        self.assertEqual(len(side), 6)
        for val in side:
            self.assertEqual(val, 4)
            
    def test_construct_side_short(self):
        """test that it can construct sides with very short arrays"""
        side = self.board.construct_side(1, 4)
        
        self.assertTrue(isinstance(side, list))
        self.assertEqual(len(side), 1)
        for val in side:
            self.assertEqual(val, 4)
        
    def test_construct_side_long(self):
        """test that it can construct sides with longer arrays"""
        side = self.board.construct_side(20, 4)
        
        self.assertTrue(isinstance(side, list))
        self.assertEqual(len(side), 20)
        for val in side:
            self.assertEqual(val, 4)
        
    def test_construct_side_empty(self):
        """test if it can leave starting houses empty
        we're not testing if it realizes that that makes a broken game, just that it makes the board"""
        side = self.board.construct_side(6, 0)
        
        self.assertTrue(isinstance(side, list))
        self.assertEqual(len(side), 6)
        for val in side:
            self.assertEqual(val, 0)
        
    def test_construct_side_many_seeds(self):
        # test if it can have houses start with many many seeds
        side = self.board.construct_side(6, 999)
        
        self.assertTrue(isinstance(side, list))
        self.assertEqual(len(side), 6)
        for val in side:
            self.assertEqual(val, 999)

class NewGameTestCase(MancalaLogicTestCase):
    def test_new_game(self):
        """tests that new_game fills in the values for sides, score, turn and move_count appropriately"""
        
        # clear the values from the board we're given (new_game is called by __init__)
        self.board.sides = None
        self.board.scores = None
        self.board.turn = None
        self.board.move_count = None
        
        self.board.new_game(6, 4) # calling new_game with parameters set so that the test case doesn't test or import the constants from the file being tested
        
        self.assertTrue(isinstance(self.board.sides), list)
        self.assertEqual(len(self.board.sides), 2)
        for side in self.board.sides:
            self.assertTrue(isinstance(side, list))
            self.assertEqual(len(side), 6)
            for val in side:
                self.assertEqual(val, 4)
        
        self.assertTrue(isinstance(self.board_scores), list)
        self.assertEqual(len(self.board.scores), 2)
        for score in self.board.scores:
            self.assertEqual(score, 0)
        
        self.assertNotEqual(self.board.turn, None)
        self.assertFalse(self.board.turn)
        
        self.assertNotEqual(self.board.turn, None)
        self.assertEqual(self.board.move_count, 0)

class InitTestCase(MancalaLogicTestCase):
    def test_init_default(self):
        """tests the default init parameters"""
        # using the board made in setup directly and testing if new_game was called
        
        self.assertTrue(isinstance(self.board.sides), list)
        
        # we're not testing the constants, so instead we test that the sides are the same length
        # and that all houses have the same number of seeds
        self.assertEqual(len(self.board.sides), 2)
        self.assertEqual(len(self.board.sides[0]), len(self.board.sides[1]))
        for side in self.board.sides:
            self.assertTrue(isinstance(side, list))
            for val in side:
                self.assertEqual(val, self.board.sides[0][0])
        
        self.assertTrue(isinstance(self.board_scores), list)
        self.assertEqual(len(self.board.scores), 2)
        for score in self.board.scores:
            self.assertEqual(score, 0)
        
        self.assertNotEqual(self.board.turn, None)
        self.assertFalse(self.board.turn)
        
        self.assertNotEqual(self.board.turn, None)
        self.assertEqual(self.board.move_count, 0)
        
        self.assertEqual(self.board.id, None)
        self.assertEqual(self.board.challenger, "")
        self.assertEqual(self.board.challenged, "")
    
    def test_distinct_challenger_challenged(self):
        """tests if we can make a new board with a distinct challenger and challenged"""
        
        new_board = MancalaBoard(challenger = "challenger", challenged = "challenged")
        self.assertEqual(new_board.challenger, "challenger")
        self.assertEqual(new_board.challenged, "challenged")
        
    def test_construct_board_from_repr(self):
        """tests if we can construct a board from a __repr__ output"""
        side0 = [4, 2, 0, 11, 3, 2]
        side1 = [0, 2, 7, 0, 0, 0]
        scores = [11, 0]
        new_board = MancalaBoard(id=1, sides=[side0, side1], scores=scores, challenger='p1', challenged='p2', move_count=13, turn=True)
        
        self.assertEqual(new_board.id, 1)
        self.assertEqual(new_board.sides[0], side0)
        self.assertEqual(new_board.sides[1], side1)
        self.assertEqual(new_board.scores, scores)
        self.assertEqual(new_board.challenger, 'p1')
        self.assertEqual(new_board.challenged, 'p2')
        self.assertEqual(new_board.move_count, 13)
        self.assertTrue(new_board.turn)
    
    def test_construct_board_from_moves(self):
        """tests if we can construct a board from a list of moves"""
        class Move():
            """quick and dirty mock of the database move model"""
            def __init__(self, house, player):
                self.house = house
                self.player = player
        
        moves = [
            Move(3, False),
            Move(2, False),
            Move(3, True),
            Move(4, True)
        ]
        
        new_board = MancalaBoard(moves=moves)
        self.assertEqual(new_board.sides[0], [4,4,0,0,6,6])
        self.assertEqual(new_board.sides[1], [5,1,1,6,6,6])
        self.assertEqual(new_board.move_count, 4)
        self.assertEqual(new_board.scores, [2, 1])
        self.assertFalse(new_board.turn)
        
                
        
class TestInvalidateMove(MancalaLogicTestCase):
    def test_valid_move(self):
        """tests a valid move"""
        
    def test_empty_house(self):
        """tests an attempt to sow from an empty house"""
        
    def test_nonexistent_house(self):
        """tests an attempt to sow from beyond the length of the board"""
        
class TestMove(MancalaLogicTestCase):
    def test_valid_move(self):
        """tests a valid move and sees if it changes the board"""
        
    def test_mismatched_turn(self):
        """tests a move made by the player whose turn is not the turn the board thinks it is"""
        
    def test_empty_house(self):
        """tests a move made from an empty house"""
        
    def test_capture(self):
        """tests a move that captures"""
        
    def test_win(self):
        """tests a move that wins the game"""
        
    def test_turn_handover(self):
        """tests a move that's supposed to end the player's turn"""
        
    def test_bonus_turn(self):
        """tests a move that's supposed to result in a bonus turn"""
        
class TestMiscFunctions(MancalaLogicTestCase):
    def test_is_solitaire(self):
        """test the is_solitaire function"""
        
    def test_get_opponent(self):
        """test the get_opponent function"""
        
    def test_turn_int(self):
        """test the turn_int function"""
        
    def test_tally_lead(self):
        """test the tally_lead function"""
        
    def test_house_to_emoji(self):
        """test that the house_to_emoji function returns an emoji"""
        
    def test_score_to_emoji(self):
        """test the score_to_emoji function"""
    
    def test_side_to_string(self):
        """test the side_to_string function"""
        
class TestStringFunctions(MancalaLogicTestCase):
    def test_str(self):
        """a few tests for the __str__ function"""
        
    def test_repr(self):
        """a few tests for the __repr__ function"""