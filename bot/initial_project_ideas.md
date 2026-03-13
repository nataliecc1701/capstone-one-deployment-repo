# Project Ideas

In this file (but not restricted to), you can use to get used to working on this repository and jot down project ideas to easily be shared with your mentors and to keep the history of!

## Idea 1
I've already discussed this with my mentor and he's given me a tentative go-ahead to start working this way: A bot for a social media API (twitter, probably, but maybe mastodon, tumblr, or discord) which would serve games of reversi or mancala.

Posts directed to the bot (via the @ feature on the application in question) would be used to start games; replies to those threads would be used by players to communicate their moves and by the bot to display the state of the board.

A database would store the history of each game (who the players are, game status (active, abandoned, draw, or which player won), and each move made in the game on each turn)

If necessary, a site could be coded to show the games history to users via a jinja webpage (instead of e.g. asking a bot, or the database being visible only to me)