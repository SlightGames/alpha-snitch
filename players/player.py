from random import shuffle, randint
from card import Card
from game.round_info import RoundInfo

class Player(object):
    """ Represents a player. Base class for any potential future AI. """
    def __init__(self, name: str):
        self.short_name = name
        self.hand = []
        """ Player's current hand of cards """
        self.coins = 0
        """ Players number of coins """

    def set_up(self, hand, coins):
        self.hand = hand
        self.coins = coins

    def prepare(self):
        """ Called after the player has been given cards but before the first round starts. """
        shuffle(self.hand)

    def select_heist_difficulty(self, number_of_players: int):
        """ If this player is the round leader, returns the heist difficulty chosen. """
        return randint(1, number_of_players)

    def play_card(self, round_info: RoundInfo):
        """ Plays a card from the hand. """
        return self.hand.pop()

    def __repr__(self):
        return f"{self.short_name}: {self.coins}$ / {self.hand}"
