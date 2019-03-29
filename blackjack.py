# Blackjack simulator.
#
# Game terminology based upon intro section of,
# https://en.wikipedia.org/wiki/Blackjack
#

import random

# See - https://en.wikipedia.org/wiki/Standard_52-card_deck
class Deck:

    # Create a new deck of cards.
    def __init__(self):

        # [(name of the rank, [list of possible values], card_value)]
        # For example, ("2", [2]), ("K", [10]), ("A", [1, 11])
        ranks = []

        # Add the pip ranks, 2 through 10.
        for i in range(2, 11):
            ranks.append((str(i), [i], str(i)))

        # Add the court ranks, Jack, Queen, King.
        court = ["J", "Q", "K"]
        for c in court:
            ranks.append((c, [10], "10"))

        # Add the Ace.
        ranks.append(("A", [1, 11], "A"))

        # Make 1 deck of cards.
        self.cards = []
        suits = ["♣", "♦", "♥", "♠"]

        for r in ranks:
            (name, value_list, card_value) = r

            for s in suits:
                card_name = name + s                        # For example "8" + "♥".
                self.cards.append((card_name, value_list, card_value))

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
            (card, value_list, card_value) = c
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

    # Remove the card from the front of the shoe. Return it as value.
    def draw_one_card(self):
        choice = self.cards.pop(0)                          # Take the first card off the front of the shoe.
        return choice                                       # Return the chosen card.


class Hand:
    def __init__(self, name, stake, ancestors):
        self.name = name                        # User friendly name for the hand of cards.
        self.stake = stake
        self.ancestors = ancestors              # How many ancestors does this hand have?
        self.cards = []                         # The hand starts with an empty list of cards.
        self.value = 0                     # Current value of the hand.
        self.busted = False                     # Is the hand busted?
        self.blackjack = False

    # Print a summary of the hand.
    def print(self):
        print(self.name, end=":")
        for c in self.cards:
            (card, _, _) = c
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
            (_, value_list, _) = c

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
# def card_value(card):
#     (card, value_list) = card
#     if value_list in [[2], [3], [4], [5], [6], [7], [8], [9]]:
#         return card[0]                     # First char of card string, eg "3♥" returns "3"
#     elif value_list == [10]:
#         return "10"
#     else:
#         return "A"

class Table:

    # Deal one card from the front of the shoe to one of the hands.
    def deal_one_card(self, hand):
        card = self.shoe.draw_one_card()                # Draw a card from the shoe,
        hand.receive_card(card)                         # ... and add it to the parm hand.

    def __init__(self):
        self.shoe = Shoe()                              # Create an empty card shoe.
        self.shoe.replenish()                           # ... fill the shoe with normal, randomised cards.

        self.table_stake = 4 * 3 * 2                           # Normal stake is £24.
        self.blackjack_value = 3 / 2                    # Eg. £8 bet wins £12.

        self.games_played = 0
        self.hands_played_by_player = 0
        self.total_staked = 0
        self.amount_won_or_lost = 0                     # +ve number means the player is in profit, -ve means loss.

        self.dealer = None                              # The dealer's current hand on the table.
        self.player_hands = []                          # List of player hands currently on the table.

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
        print("Games played=%d, Total staked=£%d, Amount won or lost=£%d"
              % (self.games_played, self.total_staked, self.amount_won_or_lost))

    # This strategy is to Stand on 17 to 21, and to Hit on anything less than 17. In most casinos, this is also the
    # strategy that the Dealer is required to follow.
    def dealer_stategy(self, hand, dealer_up_card):
        while hand.value < 17 and not hand.busted:
            self.deal_one_card(hand)

    # This strategy looks at the dealer's up card to make a more nuanced decision about whether to Hit or Stand.
    def basic_strategy_section_1(self, hand, dealer_up_card):

        (_, _, dealer_card_value) = dealer_up_card
        finished = False

        while not finished:
            if hand.value == 12 and dealer_card_value in ["2", "3"] \
               or (hand.value in [12, 13, 14, 15, 16] and dealer_card_value in ["7", "8", "9", "10", "A"]) \
               or hand.value <= 11:
                self.deal_one_card(hand)                # "Hit"
            else:
                finished = True                         # "Stand"


    def basic_strategy_section_2(self, hand, dealer_up_card):
        (_, _, dealer_card_value) = dealer_up_card

        # It is only possible to Double Down with first 2 cards of the hand on table.
        double_down = False
        if hand.value == 11:
            if dealer_card_value != "A":
                double_down = True
        elif hand.value == 10:
            if not dealer_card_value in ["10", "A"]:
                double_down = True
        elif hand.value == 9 and dealer_card_value in ["3", "4", "5", "6"]:
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
        (_, _, player_card_1_value) = hand.cards[0]
        (_, _, player_card_2_value) = hand.cards[1]

        if player_card_1_value == "A":
            other_card = player_card_2_value
        elif player_card_2_value == "A":
            other_card = player_card_1_value

        # Are either of the player's cards an ace?
        if other_card != "":
            (_, _, dealer_card_value) = dealer_up_card

            if other_card in ["8", "9", "10"]:
                decision = "Stand"
            elif other_card == "7":
                if dealer_card_value in ["2", "7", "8"]:
                    decision = "Stand"
                elif dealer_card_value in ["9", "10", "A"]:
                    decision = "Hit"
                else:
                    decision = "Double Down"
            elif other_card == "6":
                if dealer_card_value in ["3", "4", "5", "6"]:
                    decision = "Double Down"
                else:
                    decision = "Hit"
            elif other_card in ["4", "5"]:
                if dealer_card_value in ["4", "5", "6"]:
                    decision = "Double Down"
                else:
                    decision = "Hit"
            elif other_card in ["2", "3"]:
                if dealer_card_value in ["5", "6"]:
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


    def basic_strategy_section_4(self, hand, dealer_up_card):

        # Work out the values of both of the player's cards.
        (_, _, player_card_1_value) = hand.cards[0]
        (_, _, player_card_2_value) = hand.cards[1]

        # Rule is that 1st hand can only be split twice. Ie. no more than 4 hands for 1 player in a single game.
        # And 1st hand can only be split if both cards are equal value.
        if hand.ancestors <= 1 and player_card_1_value == player_card_2_value:

            (_, _, dealer_card_value) = dealer_up_card

            decision_map = \
            {("A", "2"): "SP", ("A", "3"): "SP", ("A", "4"): "SP", ("A", "5"): "SP", ("A", "6"): "SP", ("A", "7"): "SP", ("A", "8"): "SP", ("A", "9"): "SP", ("A", "10"): "SP", ("A", "A"): "SP",
            ("10", "2"): "S", ("10", "3"): "S", ("10", "4"): "S", ("10", "5"): "S", ("10", "6"): "S", ("10", "7"): "S", ("10", "8"): "S", ("10", "9"): "S", ("10", "10"): "S", ("10", "A"): "S",
            ("9", "2"): "SP", ("9", "3"): "SP", ("9", "4"): "SP", ("9", "5"): "SP", ("9", "6"): "SP", ("9", "7"): "S", ("9", "8"): "SP", ("9", "9"): "SP", ("9", "10"): "S", ("9", "A"): "S",
            ("8", "2"): "SP", ("8", "3"): "SP", ("8", "4"): "SP", ("8", "5"): "SP", ("8", "6"): "SP", ("8", "7"): "SP", ("8", "8"): "SP", ("8", "9"): "SP", ("8", "10"): "SP", ("8", "A"): "SP",
            ("7", "2"): "SP", ("7", "3"): "SP", ("7", "4"): "SP", ("7", "5"): "SP", ("7", "6"): "SP", ("7", "7"): "SP", ("7", "8"): "H", ("7", "9"): "H", ("7", "10"): "H", ("7", "A"): "H",
            ("6", "2"): "SP", ("6", "3"): "SP", ("6", "4"): "SP", ("6", "5"): "SP", ("6", "6"): "SP", ("6", "7"): "H", ("6", "8"): "H", ("6", "9"): "H", ("6", "10"): "H", ("6", "A"): "H",
            ("5", "2"): "D", ("5", "3"): "D", ("5", "4"): "D", ("5", "5"): "D", ("5", "6"): "D", ("5", "7"): "D", ("5", "8"): "D", ("5", "9"): "D", ("5", "10"): "H", ("5", "A"): "H",
            ("4", "2"): "H", ("4", "3"): "H", ("4", "4"): "H", ("4", "5"): "SP", ("4", "6"): "SP", ("4", "7"): "H", ("4", "8"): "H", ("4", "9"): "H", ("4", "10"): "H", ("4", "A"): "H",
            ("3", "2"): "SP", ("3", "3"): "SP", ("3", "4"): "SP", ("3", "5"): "SP", ("3", "6"): "SP", ("3", "7"): "SP", ("3", "8"): "H", ("3", "9"): "H", ("3", "10"): "H", ("3", "A"): "H",
            ("2", "2"): "SP", ("2", "3"): "SP", ("2", "4"): "SP", ("2", "5"): "SP", ("2", "6"): "SP", ("2", "7"): "SP", ("2", "8"): "H", ("2", "9"): "H", ("2", "10"): "H", ("2", "A"): "H"}

            decision = decision_map.get((player_card_1_value, dealer_card_value))

            if decision == "SP":                                        # "Split"
                hand.stake = hand.stake / 2                             # Stake is split between parent and child hands.

                # Add the new child hand to the list of player's hands that are on the table.
                self.player_hands.append(Hand("Child of " + hand.name,
                                              hand.stake,               # New hand has same newly halved stake as parent.
                                              hand.ancestors + 1))      # It has 1 more ancestor than its parent.

                new_hand_index = len(self.player_hands) -1
                self.hands_played_by_player += 1

                # Move 2nd card from parent hand to child hand.
                second_card = hand.cards.pop(1)
                self.player_hands[new_hand_index].receive_card(second_card)

                # Deal a card to parent, so that it has 2 cards again.
                self.deal_one_card(hand)

                # The parent hand is now a child too.
                hand.ancestors += 1

                # Now apply this strategy to the new version of the parent hand.
                self.basic_strategy_section_4(hand, dealer_up_card)

                # Now work on the child hand.
                self.deal_one_card(self.player_hands[new_hand_index])

                # Now apply this strategy to the child hand.
                self.basic_strategy_section_4(self.player_hands[new_hand_index], dealer_up_card)

            elif decision == "D":                                       # "Double Down"
                self.double_down(hand)                                  # Double stake.
                self.deal_one_card(hand)                                # One more card only, after Double Down.

            elif decision == "H":                                       # "Hit"
                self.deal_one_card(hand)                                #
                self.basic_strategy_section_3(hand, dealer_up_card)     # ... and then continue with Section 3 strategy.

            elif decision != "S":                                       # "Stand" means do nothing, but otherwise,
                self.basic_strategy_section_3(hand, dealer_up_card)     # ... continue with Section 3 strategy.

        else:
            self.basic_strategy_section_3(hand, dealer_up_card)

    def play_one_game(self, strategy_name):

        self.games_played += 1                              # Increment number of games played on this table.

        # Create a hand of cards for the dealer. Dealer has no money staked.
        self.dealer = Hand("Dealer Hand",
                            0,                              # Dealer has now money staked.
                            0)                              # This hand has no ancestors.

        self.invest(self.table_stake)

        # Create a first hand of cards for the player.
        self.player_hands.append(Hand("Player Hand",
                                      self.table_stake,     # Player starts by staking the table stake.
                                      0))                   # The player's first hand has no ancestors.
        self.hands_played_by_player += 1

        # Deal first 4 cards in classic order (Player, Dealer, Player, Dealer).
        self.deal_one_card(self.player_hands[0])
        self.deal_one_card(self.dealer)
        self.deal_one_card(self.player_hands[0])
        self.deal_one_card(self.dealer)

        # Check both Player and Dealer's hands for Blackjack on original 2 cards only.
        self.dealer.check_blackjack()
        self.player_hands[0].check_blackjack()

        if self.player_hands[0].blackjack:                                   # Player has a Blackjack.
            if self.dealer.blackjack:                           # Dealer also has a Blackjack,
                self.win(self.player_hands[0].stake)                         # ... so player wins his stake back.
            else:                                               # Player has Blackjack, and dealer doesn't have one,
                # ... so he wins his stake back, plus his stake multiplied by Blackjack odds.
                self.win(self.player_hands[0].stake + self.blackjack_value * self.player_hands[0].stake)

        # No Blackjack for the player, so proceed to a playing strategy.
        else:
            # The Dealer's up card, is the first card in his hand. Some strategies vary their decisions based upon it.
            dealer_up_card = self.dealer.cards[0]

            # Convert the parm strategy string into a strategy function.
            strategy_map = {"Dealer": self.dealer_stategy,
                            "Basic Strategy Section 1": self.basic_strategy_section_1,
                            "Basic Strategy Section 2": self.basic_strategy_section_2,
                            "Basic Strategy Section 3": self.basic_strategy_section_3,
                            "Basic Strategy Section 4": self.basic_strategy_section_4}
            strategy = strategy_map.get(strategy_name)

            strategy(self.player_hands[0], dealer_up_card)

            # Does the player have any non-busted hands?
            all_player_hands_busted = True
            for ph in self.player_hands:
                if ph.busted == False:
                    all_player_hands_busted = False

            # If player has executed his strategy without busting all of his hands,
            # and the dealer doesn't have a Blackjack...
            # ... then it is the dealer's turn to play.
            if not all_player_hands_busted and not self.dealer.blackjack:
                self.dealer_stategy(self.dealer, dealer_up_card)

                # Compare each of the player's hands with the dealer's hand.
                for ph in self.player_hands:
                    if not ph.busted:           # Only interested in non-busted player hands.

                        # If Dealer has busted, or Player has higher score than Dealer, then pleyer wins.
                        if self.dealer.busted or ph.value > self.dealer.value:
                            self.win(2 * ph.stake)                 # Win 1*stake as winnings, plus get stake back.

                        # Dealer and Player have matching scores, so no winner... but Player does get his stake back.
                        elif ph.value == self.dealer.value:
                            self.win(ph.stake)

        if verbose:
            for ph in self.player_hands:
                ph.print()
            self.dealer.print()
            self.print_table_status()
            print()

        # Game is over, so Player & Dealer dispose of their hands of cards.
        del self.dealer
        self.player_hands = []

        # Check if the shoe needs to be replenished.
        self.shoe.replenish()

verbose = False