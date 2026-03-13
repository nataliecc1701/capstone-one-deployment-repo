# Readme

This project is a discord bot that hosts mancala games, displaying a board made out of emoji in response to user commands.

## Using the Bot

### Installation

The existing bot can be added to a server by going to the URL https://discord.com/oauth2/authorize?client_id=1203620521808498709 and selecting the server there or in the Discord app for any server you have authorization to add bots to.

### Board Display

The board display will look something like this:

1️⃣⬛🔵🔵1️⃣🔵🔵🔵⬛2️⃣
8️⃣⬛2️⃣🔵🔵1️⃣4️⃣2️⃣⬛0️⃣

The leftmost column indicates the score of the opposing player (tens place on top, ones place on the bottom). The rightmost column indicates the score of the currrently active player in the same fashion.

The black square emoji are spacers separating the scoreboard from the game board itself.

The middle section shows the game board. The top row are the houses on your opponent's side. The bottom row are the houses on your side. Circles indicate empty houses, while numbers indicate the number of seeds in that house

#### popcorn emoji

The popcorn emoji is used to indicate a house that has more than ten seeds. Allocating a single digit per house does not allow for a more precise display of a large house.

### Commands

Bot commands are prefixed with a $

#### $challenge @\[user\]

Begins a game between you and the user mentioned. They must play the first move to accept the challenge. You may challenge yourself.

#### $listgames

Lists all games you are currently involved in

#### $showboard

Shows the board for your selected game, i.e., the one $move commands will apply to. It is advised to use this rather than firing off move commands without checking which board is selected first

#### $switchgame \[opponent\]

Selects the game (for $showboard and $move commands) to be whatever you are playing against the named opponent. If you don't have a game against that opponent, does nothing.

Note that this is _not_ a mention as in $challenge. Instead, the opponent should be referred to as the bot does in $listgames.

#### move \[number\]

takes a number between one and six and makes a move from that house (numbers run left to right) in the currently selected game, then, if you are not entitled to take another move immediately after, changes the currently selected game to whatever game most recently became your turn and shows you the board from that.

#### repr

Causes the bot to spit out some debug information about the current selected game (as for $showboard and $move)

### Game rules

The bot implements the rules of a simple 6,4 mancala game. These parameters (the number of houses on a side and the number of starting seeds per house) can be changed in mancala_logic.py

#### The board

The board is made up of two scoring cups, at the ends of the board (the scoring cup to your right is yours, the one to your left belongs to your opponent) and six houses on each side of the board (six for you, six for your opponent). In each house and scoring cup there are a number of seeds, which are the primary game piece and will change throughout the game.

"Left" and "Right" are defined on the assumption that the players are facing each other with the board in between them. The display from this bot is done on that basis, as though you are sitting at the bottom of the screen, looking up at an opponent above you (which means that left and right match what is displayed on screen)

#### Moving

On your turn, you must make a move. To do so, select a non-empty house from your side of the board. Remove all its seeds, then, moving to the right, place one in the next house, one in the next, and so on. When you get to the end, place a seed in your scoring cup; if you have seeds remaining, place them right to left into your opponent's houses. If you have seeds remaining after that, do not place one in the scoring cup, instead place them left to right into your houses, and so on.

#### Repeat turns

If the last seed you place on a turn goes into your scoring cup, you may take another turn immediately. Otherwise, play passes to your opponent

#### Capturing

If the last seed you place on a turn goes into an empty house on your side, and the corresponding house on your opponent's side has seeds in it, take the seeds from your opponent's house and add them to your score.

Note that houses correspond to the same position, though their numerical arrangements run opposite. For instance, the leftmost (first) house on your side of the board corresponds to the rightmost house on your opponent's side, 

#### Ending the game

When one side has no seeds in its houses, the game is over. Move all seeds on the other side into that side's scoring cup; whichever side has more seeds is the winner.