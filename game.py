# Game elements: players, cards and class for running a game

from enum import Enum
from random import shuffle, randint
from printer import Printer
from math import ceil
from profiler import Profiler

# Whether to enable logging of performance metrics to stdout
PERFORMANCE_LOGGING = True

# Number of Snitch cards each player starts with.
INITIAL_SNITCHES_PER_PLAYER = 3
# Total number of cards each player starts with.
INITIAL_CARDS_PER_PLAYER = 10
# Starting number of coins per player
INITIAL_COINS_PER_PLAYER = 3
# Game rounds
GAME_ROUNDS = 8

class Card(Enum):
    """ Card types """
    SNITCH = 1
    LOCKPICK = 2
    MUSCLE = 3
    LOOKOUT = 4
    DRIVER = 5
    CON_ARTIST = 6

    def __repr__(self):
        return self.name

INITIAL_SNITCH_HAND = [Card.SNITCH] * INITIAL_SNITCHES_PER_PLAYER

class Player(object):
    """ Represents a player. """
    def __init__(self, id: int):
        self.id = id
        self.hand: [Card] = []
        """ Player's current hand of cards """
        self.coins = INITIAL_COINS_PER_PLAYER
        """ Players number of coins """

    def reset(self):
        self.hand = []
        self.coins = INITIAL_COINS_PER_PLAYER

    def prepare(self):
        """ Called after the player has been given cards but before the first round starts. """
        shuffle(self.hand)

    @property
    def short_name(self):
        return f"Player #{self.id}"

    def select_heist_difficulty(self, number_of_players: int):
        """ If this player is the round leader, returns the heist difficulty chosen. """
        return randint(1, number_of_players)

    def play_card(self, contract_cards: [Card]):
        """ Plays a card from the hand. """
        return self.hand.pop()

    def __repr__(self):
        return f"{self.short_name}: {self.coins}$ / {self.hand}"

CHARACTER_CARDS = [Card.LOCKPICK, Card.MUSCLE, Card.LOOKOUT, Card.DRIVER, Card.CON_ARTIST]
""" List of all non-Snitch characters. """

class Game(object):
    @classmethod
    def with_number_of_players(cls, number_of_players):
        return Game(players=[Player(i) for i in range(number_of_players)])

    def __init__(self, players):
        pf = Profiler()
        pf.printer.indent()
        pf.printer.silent = not PERFORMANCE_LOGGING

        self.players = players

        # Set up the deck
        deck: [Card] = []
        for character_card in CHARACTER_CARDS:
            deck += [character_card] * 10

        pf.measure("Set up deck")
        shuffle(deck)

        pf.measure("Shuffle deck")

        self.deck = deck
        """ Current draw deck. Excludes Snitches. """

        self.discard_deck: [Card] = []
        """ Deck discarded (played) cards. Excludes Snitches. """

        pf.measure("Other set up")
        # Give each player the initial number of Snitches and deal the rest.
        for player in self.players:
            number_of_character_cards_to_deal = INITIAL_CARDS_PER_PLAYER - INITIAL_SNITCHES_PER_PLAYER
            player.hand = INITIAL_SNITCH_HAND + self.deck[:number_of_character_cards_to_deal]
            del self.deck[:number_of_character_cards_to_deal]
            player.prepare()
        
        pf.measure("Give players cards")

    def drawSafe(self):
        """ Draw from the deck and reshuffle the discard deck if needed. """
        if len(self.deck) == 0:
            # Reshuffle the discard deck into the main deck.
            shuffle(self.discard_deck)
            self.deck = self.discard_deck
            self.discard_deck.clear()
        return self.deck.pop()

    def play(self, silent=False):
        p = Printer(silent=silent)
        pf = Profiler()
        pf.printer.indent()
        pf.printer.silent = not PERFORMANCE_LOGGING
        for i in range(GAME_ROUNDS):
            p.print(f"-- Round {i} --")
            p.indent()
            pf.reset()

            # Select game leader
            leader_player = self.players[i % len(self.players)]
        
            # Leader player selects the number of players.
            heist_difficulty = leader_player.select_heist_difficulty(len(self.players))
            assert(heist_difficulty >= 1 and heist_difficulty <= len(self.players))
            p.print(f"{leader_player.short_name} selects difficulty of {heist_difficulty}")

            # Draw this many cards to form the contract
            contract_cards = [self.drawSafe() for _ in range(heist_difficulty)]
            p.print(f"Contract cards: {contract_cards}")

            # Ask each player to play a card
            player_cards = [(player, player.play_card(contract_cards)) for player in self.players]
            played_cards = []
            for (player, card) in player_cards:
                p.print(f"{player.short_name} plays {card}")
                played_cards.append(card)

            pf.measure("Draw cards")

            # Evaluate game
            heist_success = self.evaluate_contract(contract_cards, played_cards)
            if heist_success:
                p.print("Heist SUCCESS 🙌!")
                # All non-snitching players get reward
                for (player, card) in player_cards:
                    if card in CHARACTER_CARDS:
                        p.print(f"{player.short_name} contributed and wins {heist_difficulty}💰. Yay 😊")
                        player.coins += heist_difficulty
                    else:
                        p.print(f"{player.short_name} snitched and gets nothing. 🤥 ")
            else:
                p.print("Heist FAILED ❌!")
                
                if not Card.SNITCH in played_cards:
                    # There were no snitches. The heist simply failed due to lack of cards.
                    p.print("No one played a Snitch. All players retain their coins.") 
                elif len([card for card in played_cards if card == Card.SNITCH]) == len(self.players):
                    # Everyone played Snitch.
                    p.print("Everyone played a Snitch. All players retain their coins.") 
                else:
                    # All snitched-on players lose -1
                    pot = 0
                    snitch_players = []
                    for (player, card) in player_cards:
                        if card in CHARACTER_CARDS:
                            if player.coins > 0:
                                player.coins -= 1
                                pot += 1
                                p.print(f"{player.short_name} got betrayed and loses 1💰. Grr 😤")
                            else:
                                p.print(f"{player.short_name} got betrayed but has no money.")
                        else:
                            snitch_players.append(player)

                    # All snitching players (if any) split the reward, to a minimum of 1
                    reward = max(1, ceil(pot / len(snitch_players)))
                    for player in snitch_players:
                        player.coins += reward
                        p.print(f"{player.short_name} snitched and gets {reward}💰. Ha! 😆")
                        
            pf.measure("Evaluate")

            # Discard all cards
            self.discard_deck.extend(contract_cards)
            for (_, card) in player_cards:
                self.discard_deck.append(card)

            p.deindent()

        p.print("*** Game Summary ***")
        p.indent()
        # Sort by money.
        players = list(self.players)
        players.sort(key=lambda player: player.coins, reverse=True)
    
        # Determine winners
        winners = [player for player in players if player.coins == players[0].coins]
        if len(winners) == 1:
            p.print(f"{winners[0].short_name} wins with ${winners[0].coins}")
        elif len(winners) == len(players):
            p.print(f"All players draw.")
            winners = []
        else:
            winner_names = ", ".join(p.short_name for p in winners)
            p.print(f"{winner_names} drew with ${winners[0].coins}")
        p.deindent()

        # Return result and stats
        return {
            "winners": winners
        }

    def evaluate_contract(self, contract_cards: [Card], played_cards: [Card]):
        for card in contract_cards:
            if card in played_cards:
                played_cards.remove(card)
            else:
                # Contract card not fulfilled. Heist failes
                return False
        # All cards found. Heist succeeds
        return True