# Do some tests.

import blackjack

class Test:
    def __init__(self, strategy_name):
        self.strategy_name = strategy_name

        print("Player strategy:", self.strategy_name)

        this_table = blackjack.Table()

        # Force some test cards on to the front of the shoe.
        this_table.shoe.cards =     [("6♥", [6], "6")]
        this_table.shoe.cards.append(("3♥", [3], "3"))
        this_table.shoe.cards.append(("6♥", [6], "6"))
        this_table.shoe.cards.append(("9♥", [9], "9"))

        # Because more cards may be needed to play a game, add some normal cards to the end of the shoe.
        new_deck = blackjack.Deck()
        new_deck.shuffle()
        this_table.shoe.cards = this_table.shoe.cards + new_deck.cards

        if blackjack.verbose:
            this_table.shoe.print()

        this_table.play_one_round(self.strategy_name)    # Play a game.


blackjack.verbose = True
t1 = Test("Dealer")
t2 = Test("Basic Strategy Section 1")
t3 = Test("Basic Strategy Section 2")
t4 = Test("Basic Strategy Section 3")
t5 = Test("Basic Strategy Section 4")
