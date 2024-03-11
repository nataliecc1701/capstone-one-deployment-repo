'''Logic for the mancala game'''

# set our constants: the number of houses on each side of the board, and the number of
# seeds that begin in each house
BOARD_HOUSES = 6
SEEDS_PER_HOUSE = 4

class MancalaBoard:
    def __init__(self, sides = [], scores = []):
        self.new_game()
        if sides:
            self.sides = sides
            if scores:
                self.scores = scores
        
    def new_game(self, houses = BOARD_HOUSES, seeds = SEEDS_PER_HOUSE):
        self.sides = [self.construct_side(houses,seeds), self.construct_side(houses,seeds)]
        self.scores = [0,0]
        self.turn = False
        
        # doing this with array indices and a bool for turn status is perhaps prematurely
        # optimized. I could do this with dictionaries (keys "challenger", "challenged")
        # and the turn being a key
        
    def construct_side(self, houses,seeds):
        side = []
        for i in range(houses):
            side.append(seeds)
        return side
    
    def move(self, house, turn = None):
        """Makes a move from the given house. Defaults to being for the player whose turn it is
        
        Status codes:
        Starting with 1: Successful move
        10: Successful move, end turn
        11: Successful move, same player's turn
        12: Successful move, end game
        
        Starting with 2: Failed move and error message
        20: Error"""
        # NOTE: REWORK THIS FUNCTION SO THAT IT RETURNS A STATUS CODE AND MESSAGE TUPLE PROBABLY
        
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
                
    
    def __repr__(self):
        return f"MancalaBoard({self.sides}, {self.score})"
    
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