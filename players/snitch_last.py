# Player that always chooses to Snitch last
from card import Card
from game.round_info import RoundInfo
from game.game import GAME_ROUNDS
from players.player import Player

class SnitchLastPlayer(Player):
    """ Player who plays all their snitches at the end. """
    def __init__(self, name):
        super().__init__(f"Sneaky {name}")

    def prepare(self):
        super().prepare()
        self.snitches_left = 3

    def select_heist_difficulty(self, number_of_players: int):
        # This player always plays 1 to make sure they can make it.
        return 1

    def play_card(self, round_info: RoundInfo):
        # Strategy: select any contract card that the player has. Otherwise play Snitch.
        # Also towards end of the game, play all snitch cards.

        # Calculate rounds left, excluding this one
        rounds_left = GAME_ROUNDS - round_info.number - 1

        if self.snitches_left > rounds_left:
            self.hand.remove(Card.SNITCH)
            self.snitches_left -= 1
            return Card.SNITCH

        for card in round_info.contract_cards:
            if card in self.hand:
                self.hand.remove(card)
                return card
        
        # Card not available. Return any card but not Snitches.
        # Assumes all the snitches are at the front.
        card = self.hand[-1]
        del self.hand[-1]
        if card == Card.SNITCH:
            self.snitches_left -= 1
        return card
