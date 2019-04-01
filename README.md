# Blackjack
Simulation of Blackjack. Able to run experiments that play a large number of rounds. Does calculation of player edge for a variety of strategies.

#### Results

![results table](results_table.png)

![results graph](results_graph.png)

#### Player Edge

Player edge means the percentage advantage that the player can expect in the long-run when playing a particular strategy for many rounds in a long session. For most strategies, the Player Edge is negative, meaning that - in fact - the House has the edge.

For example a Player Edge of -1% means that. on average, the player will be down by 1% of their staked money by the end the session. In this case, if the player stakes a total of £100, they can expect to be left with just £99 at the end of the session.

A positive Player Edge means that the player is likely to be ahead at the end of the session :)

#### Studies

The program can be used to automatically do a Study, which consists of many sessions of Blackjack. Each session is like sitting down at a table and playing many rounds. Statistics about the sessions are stored, and then analysed.

In the program, during each session, the `amount_won_or_loss` is subtracted to or added to each time their is money staked or won. `total_staked` is added to each time money is staked.

When a study of many sessions is done, the `win_loss` list is appended to at then of each session.
~~~
# Multiply by 100 to make it a percentage.
self.win_loss.append(100 * this_table.amount_won_or_lost / this_table.total_staked)
~~~

#### Cards

Cards are represented as tuples, `(name, value_list), card_value)`.

For example,

~~~
("6♥", [6], "6")
("10♣", [10], "10")
("Q♦", [10], "10")
("A♠", [1, 11], "A")
~~~
`card_value` is used to lookup cards in the strategy tables described below. All cards worth 10 points have a card_value of "10". Aces have a`card_value` of "A".

#### Shoe

The [Shoe](https://en.wikipedia.org/wiki/Shoe_(cards) is configured to contain 4 packs of cards. It is configured to have remaining cards discarded, and the shoe re-filled with a fresh set of 4 packs of cards when the penetration level of 75% is reached. Both of these settings can be altered by changing these attributes of the `Shoe` class,

~~~
self.decks = 4                 # Number of decks in the shoe when full.
self.penetration = 75 / 100    # Percentage of cards to be dealt before refilling shoe.
~~~

At the end of each game, the `replenish` method should be called, to check whether the shoe has been depleted below the penetration level. If it has, then the shoe will be re-filled and all cards in the shoe shuffled.

#### Blackjack Value

A Blackjack can only be won with first two cards of first hand of a game. The attribute `blackjack_value` of the `Table` class is set to "3 for 2", which is standard the standard value of a Blackjack value in Vegas casinos (stake also returned). 
~~~
self.blackjack_value = 3 / 2        # Eg. £10 bet wins £15.
~~~

## Strategies

The following strategies are implemented in the program.

#### Dealer Strategy

Implemented in the `dealer_stategy` method. The most basic strategy; it is the strategy that dealers must follow when playing the House's hands in Vegas casinos. It is also possible to run experiments where the player uses this strategy too.

_If current value of hand is 16 or less, then Hit, otherwise Stand._

#### Basic Strategy

As illustrated on this card,
https://www.ebay.co.uk/itm/303101632202

More details here,
https://github.com/johntelforduk/blackjack/blob/master/basic_strategy.md

Basic strategy has 4 sections, implemented in 4 methods as follows,

`basic_strategy_section_1` : Basic rules about when to Hit or Stand.

`basic_strategy_section_2` : Double Down rules.

`basic_strategy_section_3` : Special rules when the player has an Ace in his first 2 cards of the hand.

`basic_strategy_section_4` : Rules for player hands with matching card values, which may be Split.

These rules form a hierachy. For example, if the conditions for Section 4's rules are not met, then Section 3 is tested, and so on.

#### Card Counting

Hi-Lo card counting is described here, https://youtu.be/G_So72lFNIU

The effectiveness of Hi-Lo card counting strategy can be tested by the program. A running count of cards dealt from the shoe (face up cards only) is kept. The true count and recommended bet size is also calculated.

Card counting varies the size of the initial bet in each round. But after the bet is made, Basic Strategy Section 4 is used to play the hand(s).

## Useful Resources
Rules of Blackjack https://youtu.be/XYgdLMcPspo

Blackjack terminology, https://en.wikipedia.org/wiki/Blackjack and https://www.blackjackapprenticeship.com/glossary-of-blackjack-terms/
