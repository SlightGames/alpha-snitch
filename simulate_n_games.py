from game.game import Game
from players.player import Player
from players.snitch_last import SnitchLastPlayer
from profiler import Profiler

NUMBER_OF_PLAYERS = 3
GAMES = 10000

if __name__ == "__main__":
    # Create players
    players = [
        Player("Anna"), 
        Player("Ben"), 
        SnitchLastPlayer("Charles"),
        SnitchLastPlayer("Dylan")
    ]

    pure_wins = 0  # i.e. exactly 1 person won
    shared_wins = 0  # i.e. where multiple but not all players won
    draws = 0  # i.e. all players drew.
    wins_per_player = { player: 0 for player in players }

    pf = Profiler()
    for _ in range(GAMES):
        game = Game(players)
        result = game.play(silent=True)
        # Record stats about the game
        winners = result["winners"]

        if len(winners) == 0:
            draws += 1
        else:
            for winner in winners:
                wins_per_player[winner] += 1
            if len(winners) == 1:
                pure_wins += 1
            else:
                shared_wins += 1
    pf.measure("Time taken")

    # Print stats
    print(f"Player {GAMES} games with {NUMBER_OF_PLAYERS} players")
    print(f"There were:")
    print(f"\t{pure_wins}\tPure wins")
    print(f"\t{shared_wins}\tShared wins")
    print(f"\t{draws}\tDraws")
    print(f"Wins per player:")
    for player, wins in wins_per_player.items():
        print(f"\t{wins}\t{player.short_name}")