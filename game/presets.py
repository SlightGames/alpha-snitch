from game.game import Game
from players.player import Player
from players.snitch_last import SnitchLastPlayer

# Game presets
SIMPLE_3P_GAME = Game.with_number_of_players(3)
GAME_WITH_1_LAST_SNITCH_PLAYER = Game(players=[Player("Anna"),Player("Ben"),SnitchLastPlayer("Charles")])