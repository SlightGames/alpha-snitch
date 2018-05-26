from game import presets
from game.game import Game
from players.player import Player

if __name__ == "__main__":
    # Select a game and play it
    game = presets.GAME_WITH_1_LAST_SNITCH_PLAYER
    game.play()
