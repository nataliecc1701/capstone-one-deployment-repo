'''Logic for the mancala game'''

# set our constants: the number of houses on each side of the board, and the number of
# seeds that begin in each house
BOARD_HOUSES = 6
SEEDS_PER_HOUSE = 4

class MancalaBoard:
    def __init__(self, id = None, sides = [], scores = [], moves = [], challenger = "", challenged = "", move_count = 0, turn = False):
        self.id = id
        self.challenger = challenger
        self.challenged = challenged
        self.new_game()
        if sides:
            self.sides = sides
            if scores:
                self.scores = scores
            self.move_count = move_count
            self.turn = turn
        elif moves:
            # Construct a board from a list of past moves. Only happens if the board state is not given
            for move in moves:
                self.move(int(move.house), move.player)
            self.move_count = len(moves)
        
    def new_game(self, houses = BOARD_HOUSES, seeds = SEEDS_PER_HOUSE):
        self.sides = [self.construct_side(houses,seeds), self.construct_side(houses,seeds)]
        self.scores = [0,0]
        self.turn = False
        self.move_count = 0
        
        # index of 0 for challenger, 1 for challenged
        
        # doing this with array indices and a bool for turn status is perhaps prematurely
        # optimized. I could do this with dictionaries (keys "challenger", "challenged")
        # and the turn being a key
        
    def construct_side(self, houses,seeds):
        side = []
        for i in range(houses):
            side.append(seeds)
        return side
    
    def invalidate_move(self, position, turn = None):
        """Checks if a move can be made: takes position as an array index.
        Returns an error string, or false for valid moves"""
        
        if turn == None:
            turn = self.turn
            
        side = 1
        if turn:
            side = 0
        
        if position >= BOARD_HOUSES:
            return "House does not exist"
        if self.sides[side][position] == 0:
            return "Cannot take from empty house"
        return False
    
    def move(self, house, turn = None):
        """Makes a move from the given house. Defaults to being for the player whose turn it is
        
        Returns a tuple of status code, string. String is usually empty for successful moves.
        
        Status codes:
        Starting with 1: Successful move
        10: Successful move, end turn
        11: Successful move, same player's turn
        12: Successful move, end game
        
        Starting with 2: Failed move and error message
        20: Error"""
        
        # figure out which side of the board we're on
        if turn == None:
            turn = self.turn
        
        seeds_in_hand = 0
        position = house - 1
        # house comes in as a human-readable number, converts to an array index
        
        side = 1
        if turn:
            side = 0
        
        seeds_in_hand = self.sides[side][position]
        self.sides[side][position] = 0
        
        if seeds_in_hand == 0:
            return (20, "cannot take from empty house")
        while seeds_in_hand > 0:
            position += 1
            if position >= BOARD_HOUSES*2 + 1:
                position = position % 13
            
            if position < BOARD_HOUSES:
                self.sides[side][position] += 1
            elif position == BOARD_HOUSES:
                self.scores[side] += 1
            else:
                self.sides[side-1][position-BOARD_HOUSES-1] += 1
            seeds_in_hand -= 1
        
        # capturing
        if position < BOARD_HOUSES and self.sides[side][position] == 1:
            self.scores[side] += self.sides[side-1][-position-1]
            self.sides[side-1][-position-1] = 0
        
        # win detection
        if not any(self.sides[0]) or not any(self.sides[1]):
            return (12, "Game over!")
        
        # turn handover
        if position != BOARD_HOUSES:
            self.turn = not self.turn
            return (10, "")
        else:
            return (11, "")
    
    def is_solitaire(self):
        return self.challenger == self.challenged
    
    def get_opponent(self, turn = None):
        """gets the current player's opponent. Returns a username string"""
        if turn == None:
            turn = self.turn
        
        if turn:
            return self.challenged
        else:
            return self.challenger
    
    def turn_int(self):
        """returns 0 for the challenger's turn, 1 for the challenged's turn. Used to construct status codes"""
        if self.turn:
            return 0
        return 1
            
    def tally_lead(self):
        """Tallies the scores and all seeds in people's houses to determine who's ahead. Returns 0 for the challenger and 1 for the challenged.
        If one side of the board is empty, then whoever is ahead now is the winner."""
        final_scores = (self.scores[0] + sum(self.sides[0]), self.scores[1] + sum(self.sides[1]))
        if final_scores[0] > final_scores[1]:
            return 0
        return 1
    
    def __repr__(self):
        return f"MancalaBoard(id={self.id}, sides={self.sides}, scores={self.scores}, challenger={self.challenger}, challenged={self.challenged}, move_count={self.move_count}, turn={self.turn})"
    
    def __str__(self):
        '''the emojified string of the board'''
        sep = "⬛" # separator character: black square emoji
        i = 1
        if self.turn:
            i = -1
        scores = [self.score_to_emoji(s) for s in self.scores[::i]]
        sides = self.sides[::i]
        
        top_line = f"{scores[0][0]}{sep}{self.side_to_string(sides[0], reverse=True)}{sep}{scores[1][0]}"
        bottom_line = f"{scores[0][1]}{sep}{self.side_to_string(sides[1])}{sep}{scores[1][1]}"
        
        return f"{top_line}\n{bottom_line}"
    
    def house_to_emoji(self, num: int):
        emoji_list = ["🔵","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        if num <= 10:
            return emoji_list[num]
        else: return "🍿"
    
    def score_to_emoji(self, score: int):
        emoji_list = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
        places = (score//10, score%10)
        emoji = []
        for digit in places:
            emoji.append(emoji_list[digit])
        return emoji
    
    def side_to_string(self, side, reverse = False):
        side_str = ""
        if reverse:
            internal_side = side[::-1]
        else:
            internal_side = side
        for house in internal_side:
            side_str += self.house_to_emoji(house)
        return side_str