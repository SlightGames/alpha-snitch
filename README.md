# Alpha-Snitch

Simulates a game of [Snitch](http://slightgames.co.uk), a simple card-based bluffing game. 

Does not actually contain any AI yet! Coming soon.

## Run
Use `python3`. Try:
```sh
python simulate_1_game.py   # Single game
python simulate_n_games.py  # Runs multiple games with stats.
```

## Overview
`Player` contains player logic, such as choosing heist difficulty and selecting a card to play.

`Game` encodes the rules of the game and runs it. Each instance can only be used once.

```python
players=[Player("Anna"), Player("Ben"), AIPlayer("Charles")]
game = Game(players)
result = game.play()
```
This by default is fairly verbose. When running lots of simulations, use `game.play(silent=True)`. 