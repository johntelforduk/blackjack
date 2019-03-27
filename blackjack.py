# Blackjack simulator.
#
# Game terminology based upon intro section of,
# https://en.wikipedia.org/wiki/Blackjack
#

from statistics import mean
from statistics import stdev
import random


# See - https://en.wikipedia.org/wiki/Standard_52-card_deck
class Deck:

    # Create a new deck of cards.
    def __init__(self):

        # [(name of the rank, [list of possible values])]
        # For example, ("2", [2]), ("K", [10]), ("A", [1, 11])
        ranks = []

        # Add the pip ranks, 2 through 10.
        for i in range(2, 11):
            ranks.append((str(i), [i]))

        # Add the court ranks, Jack, Queen, King.
        court = ["J", "Q", "K"]
        for c in court:
            ranks.append((c, [10]))

        # Add the Ace.
        ranks.append(("A", [1, 11]))

        # Make 1 deck of cards.
        self.cards = []
        suits = ["♣", "♦", "♥", "♠"]

        for r in ranks:
            (name, value_list) = r

            for s in suits:
                card_name = name + s                        # For example "8" + "♥".
                self.cards.append((card_name, value_list))

    # Shuffle the deck.
    def shuffle(self):
        random.shuffle(self.cards)


# See - https://en.wikipedia.org/wiki/Shoe_(cards)
class Shoe:

    def __init__(self):
        self.cards = []                                     # Cards currently in the shoe.
        self.decks = 4                                      # Number of decks in the shoe when full.
        self.penetration = 75 / 100                         # Percentage of cards to be dealt before refilling shoe.

    # Print the first 10 cards in shoe, plus number of cards in shoe.
    def print(self):
        print("Shoe: ", end="")
        for c in self.cards[0:10]:
            (card, value_list) = c
            print(card, end=" ")
        print("Number of cards", len(self.cards))

    # Shuffle all of the cards in the shoe.
    def shuffle(self):
        random.shuffle(self.cards)

    # If the shoe of cards is getting small, then replenish it.
    def replenish(self):
        if len(self.cards) <= ((1 - self.penetration) * self.decks * 52):
            self.cards = []                                 # Remove the remaining cards from the shoe.
            for d in range(self.decks):
                new_deck = Deck()
                self.cards = self.cards + new_deck.cards

            self.shuffle()                                  # If cards were added, then shuffle the cards in the shoe.

    # Force some test cards on to the front of the shoe.
    def test_cards(self):
        self.cards =     [("A♥", [1, 11])]
        self.cards.append(("2♥", [2]))
        self.cards.append(("7♥", [7]))
        self.cards.append(("9♥", [9]))

        # Because more cards may be added to the shoe, add some normal cards to the end of the shoe.
        new_deck = Deck()
        new_deck.shuffle()
        self.cards = self.cards + new_deck.cards

        if verbose:
            self.print()

    # Remove the card from the front of the shoe. Return it as value.
    def draw_one_card(self):
        choice = self.cards.pop(0)                          # Take the first card off the front of the shoe.
        return choice                                       # Return the chosen card.


class Hand:
    def __init__(self, name, stake):
        self.name = name                        # User friendly name for the hand of cards.
        self.stake = stake
        self.cards = []                         # The hand starts with an empty list of cards.
        self.value = 0                     # Current value of the hand.
        self.busted = False                     # Is the hand busted?
        self.blackjack = False

    # Print a summary of the hand.
    def print(self):
        print(self.name, end=":")
        for c in self.cards:
            (card, value_list) = c
            print("", card, end="")
        print(", Value=%d" % self.value, end="")
        if self.busted:
            print(", Busted", end="")
        else:
            print(", Not-busted", end="")
        if self.blackjack:
            print(", Blackjack", end="")
        else:
            print(", No Blackjack", end="")
        print(", Stake=£%d" % self.stake, end="")
        print()


    def calculate_value(self):
        possible_values = [0]             # List of all possible values of this hand.

        for c in self.cards:
            (card, value_list) = c

            new_possible_values = []
            for p in possible_values:
                for v in value_list:
                    new_possible_values.append(p + v)
            possible_values = new_possible_values

        self.value = 0
        self.busted = True
        for p in possible_values:
            if p > self.value and p <=21:
                self.value = p         # We found a new higher, non-busted value.
                self.busted = False

        # If we busted, it is still nice to set the value to the lowest possible value the cards in the hand can make.
        if self.busted:
            self.value = min(possible_values)


    def check_blackjack(self):
        if self.value == 21:
            self.blackjack = True

    # Add the parm card to this hand.
    def receive_card(self, card):
        self.cards.append(card)         # Append the parm card to the list of cards in this hand.
        self.calculate_value()          # Recalculate the value of this hand.


# Parm is a card. Function returns a string which is the value of the card for purpose of looking
# it up on the "Basic Strategy For Blackjack" strategy card.
def card_value(card):
    (card, value_list) = card
    if value_list in [[2], [3], [4], [5], [6], [7], [8], [9]]:
        return card[0]                     # First char of card string, eg "3♥" returns "3"
    elif value_list == [10]:
        return "10"
    else:
        return "A"

class Table:

    # Deal one card from the front of the shoe to one of the hands.
    def deal_one_card(self, hand):
        card = self.shoe.draw_one_card()                # Draw a card from the shoe,
        hand.receive_card(card)                         # ... and add it to the parm hand.

    def __init__(self, testing):
        self.shoe = Shoe()                              # Create an empty card show.

        if testing:                                     # If this is a test table, fill the shoe with test cards.
            self.shoe.test_cards()
        else:                                           # If not testing...
            self.shoe.replenish()                       # ... fill the shoe with normal, randomised cards.

        self.table_stake = 10                           # Normal stake is £10.
        self.blackjack_value = 3 / 2                    # Eg. £10 bet wins £15.

        self.games_played = 0
        self.total_staked = 0
        self.amount_won_or_lost = 0                     # +ve number means the player is in profit, -ve means loss.

    # Update running totals to reflect money staked by player.
    def invest(self, stake):
        self.total_staked += stake
        self.amount_won_or_lost -= stake

    # Double down the stake on this hand.
    def double_down(self, hand):
        self.invest(hand.stake)
        hand.stake += hand.stake

    # Add parm winnings to player running total or money won (or lost).
    def win(self, winnings):
        self.amount_won_or_lost += winnings

    def print_table_status(self):
        print("Games played=%d, Total staked=£%d, Amount won or lost=£%d" % (self.games_played, self.total_staked, self.amount_won_or_lost))

    # This strategy is to Stand on 17 to 21, and to Hit on anything less than 17. In most casinos, this is also the
    # strategy that the Dealer is required to follow.
    def dealer_stategy(self, hand, dealer_up_card):
        while hand.value < 17 and not hand.busted:
            self.deal_one_card(hand)

    # This strategy looks at the dealer's up card to make a more nuanced decision about whether to Hit or Stand.
    def basic_strategy_section_1(self, hand, dealer_up_card):
        dealer_card = card_value(dealer_up_card)
        finished = False

        while not finished:
            if hand.value == 12 and dealer_card in ["2", "3"] \
               or (hand.value in [12, 13, 14, 15, 16] and dealer_card in ["7", "8", "9", "10", "A"]) \
               or hand.value <= 11:
                self.deal_one_card(hand)                # "Hit"
            else:
                finished = True                         # "Stand"


    def basic_strategy_section_2(self, hand, dealer_up_card):
        dealer_card = card_value(dealer_up_card)

        # It is only possible to Double Down with first 2 cards of the hand on table.
        double_down = False
        if hand.value == 11:
            if dealer_card != "A":
                double_down = True
        elif hand.value == 10:
            if not dealer_card in ["10", "A"]:
                double_down = True
        elif hand.value == 9 and dealer_card in ["3", "4", "5", "6"]:
            double_down = True

        if double_down:
            self.double_down(hand)
            self.deal_one_card(hand)  # One more card only, after Double Down.

        # If we are not doubling down, then play Basic Strategy Section 1.
        else:
            self.basic_strategy_section_1(hand, dealer_up_card)

    def basic_strategy_section_3(self, hand, dealer_up_card):

        other_card = ""
        decision = ""

        # Work out the values of both of the player's cards.
        player_card_1 = card_value(hand.cards[0])
        player_card_2 = card_value(hand.cards[1])

        if player_card_1 == "A":
            other_card = player_card_2
        elif player_card_2 == "A":
            other_card = player_card_1

        # Are either of the player's cards an ace?
        if other_card != "":
            dealer_card = card_value(dealer_up_card)

            if other_card in ["8", "9", "10"]:
                decision = "Stand"
            elif other_card == "7":
                if dealer_card in ["2", "7", "8"]:
                    decision = "Stand"
                elif dealer_card in ["9", "10", "A"]:
                    decision = "Hit"
                else:
                    decision = "Double Down"
            elif other_card == "6":
                if dealer_card in ["3", "4", "5", "6"]:
                    decision = "Double Down"
                else:
                    decision = "Hit"
            elif other_card in ["4", "5"]:
                if dealer_card in ["4", "5", "6"]:
                    decision = "Double Down"
                else:
                    decision = "Hit"
            elif other_card in ["2", "3"]:
                if dealer_card in ["5", "6"]:
                    decision = "Double Down"
                else:
                    decision = "Hit"

        if other_card == "":                                        # If neither card is an ace,
            self.basic_strategy_section_2(hand, dealer_up_card)     # ... continue with Section 2 strategy.

        elif decision == "Double Down":
            self.double_down(hand)                                  # Double stake.
            self.deal_one_card(hand)                                # One more card only, after Double Down.

        elif decision == "Hit":
            self.deal_one_card(hand)                                # "Hit",
            self.basic_strategy_section_2(hand, dealer_up_card)     # ... and then continue with Section 2 strategy.

        elif decision != "Stand":                                   # "Stand" means do nothing, but otherwise,
            self.basic_strategy_section_2(hand, dealer_up_card)     # ... continue with Section 2 strategy.






    def play_one_game(self, strategy):
        self.games_played += 1

        # Create a hand of cards for the dealer. Dealer has no money staked.
        self.dealer = Hand("Dealer", 0)

        self.invest(self.table_stake)
        self.h1 = Hand("Player Hand 1", self.table_stake)       # Create a hand of cards for player.

        # Deal first 4 cards in classic order (Player, Dealer, Player, Dealer).
        self.deal_one_card(self.h1)
        self.deal_one_card(self.dealer)
        self.deal_one_card(self.h1)
        self.deal_one_card(self.dealer)

        # Check both Player and Dealer's hands for Blackjack on original 2 cards only.
        self.dealer.check_blackjack()
        self.h1.check_blackjack()

        if self.h1.blackjack:                                   # Player has a Blackjack.
            if self.dealer.blackjack:                           # Dealer also has a Blackjack,
                self.win(self.h1.stake)                         # ... so player wins his stake back.
            else:                                               # Player has Blackjack, and dealer doesn't have one,
                # ... so he wins his stake back, plus his stake multiplied by Blackjack odds.
                self.win(self.h1.stake + self.blackjack_value * self.h1.stake)

        # No Blackjack for the player, so proceed to a playing strategy.
        else:
            # The Dealer's up card, is the first card in his hand. Some strategies vary their decisions based upon it.
            dealer_up_card = self.dealer.cards[0]

            strategy(self.h1, dealer_up_card)

            # If player has executed his strategy without busting, and the dealer doesn't have a Blackjack...
            # ... then it is the dealer's turn to play.
            if not self.h1.busted and not self.dealer.blackjack:
                self.dealer_stategy(self.dealer, dealer_up_card)

                # If Dealer has busted, or Player has higher score than Dealer, then pleyer wins.
                if self.dealer.busted or self.h1.value > self.dealer.value:
                    self.win(2 * self.h1.stake)                 # Win 1*stake as winnings, plus get stake back.

                # Dealer and Player have matching scores, so no winner... but Player does get his stake back.
                elif self.h1.value == self.dealer.value:
                    self.win(self.h1.stake)

        if verbose:
            self.h1.print()
            self.dealer.print()
            self.print_table_status()
            print()

        # Game is over, so Player & Dealer dispose of their hands of cards.
        del self.dealer
        del self.h1

        # Check if the shoe needs to be replenished.
        self.shoe.replenish()


class Test:
    def __init__(self, strategy):
        self.strategy = strategy

        print("Player strategy:", self.strategy)

        this_table = Table(True)                # Parm True is to indicate that it is a test table.

        if self.strategy == "Dealer":
            this_table.play_one_game(this_table.dealer_stategy)
        elif self.strategy == "Basic Strategy Section 1":
            this_table.play_one_game(this_table.basic_strategy_section_1)
        elif self.strategy == "Basic Strategy Section 2":
            this_table.play_one_game(this_table.basic_strategy_section_2)
        elif self.strategy == "Basic Strategy Section 3":
            this_table.play_one_game(this_table.basic_strategy_section_3)



class Study:

    def __init__(self, strategy, sessions, games_per_session):
        self.strategy = strategy                    # Name of the player strategy to be tested.
        self.win_loss = []                          # List of percentage win(+ve) or loss(-ve) per session.
        self.sessions = sessions                    # Number of sessions (visits to table) to do in this study.
        self.games_per_session = games_per_session  # Number of games to be started in each session.
        self.grand_total_staked = 0                 # Grand total of money staked in all games in all sessions.
        self.run()

    # Run the study.
    def run(self):
        for experiments in range(self.sessions):
            this_table = Table(False)           # "False" is to turn testing off for this table.

            for games in range(self.games_per_session):
                if self.strategy == "Dealer":
                    this_table.play_one_game(this_table.dealer_stategy)
                elif self.strategy == "Basic Strategy Section 1":
                    this_table.play_one_game(this_table.basic_strategy_section_1)
                elif self.strategy == "Basic Strategy Section 2":
                    this_table.play_one_game(this_table.basic_strategy_section_2)
                elif self.strategy == "Basic Strategy Section 3":
                    this_table.play_one_game(this_table.basic_strategy_section_3)


            self.win_loss.append(100 * this_table.amount_won_or_lost / this_table.total_staked)
            self.grand_total_staked += this_table.total_staked

            del this_table
        self.analyse()

    # Print out analysis of the results of the study.
    def analyse(self):
        print("Player strategy:", self.strategy)
        print("Number of sessions:", self.sessions)
        print("Games per session:", self.games_per_session)
        print("Total money staked=£%d" % self.grand_total_staked)
        print("Max house edge: %.2f%%" % max(self.win_loss))
        print("Min house edge: %.2f%%" % min(self.win_loss))
        print("Average house edge: %.2f%%" % mean(self.win_loss))
        print("(-ve means house is ahead, +ve means player is ahead)")
        print("Standard deviation: %.2f" % stdev(self.win_loss))
        print()


verbose = True
t1 = Test("Dealer")
t2 = Test("Basic Strategy Section 1")
t3 = Test("Basic Strategy Section 2")
t4 = Test("Basic Strategy Section 3")


verbose = False
s1 = Study("Dealer", 10, 10000)
s2 = Study("Basic Strategy Section 1", 10, 10000)
s3 = Study("Basic Strategy Section 2", 10, 10000)
s4 = Study("Basic Strategy Section 3", 10, 10000)
