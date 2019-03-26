# Blackjack
Simulation of Blackjack. Able to run experiments that play a large number of hands. Does calculation of house edge for a variety of strategies.

Rules of Blackjack based on https://youtu.be/XYgdLMcPspo

Basic Strategy For Blackjack https://www.ebay.co.uk/itm/303101632202

#### Cards

Cards are represented as tuples, `(name, value_list)`

For example,

~~~
("6♥", [6])
("10♣", [10])
("Q♦", [10])
("A♠", [1, 11])
~~~
#### Shoe

The [Shoe](https://en.wikipedia.org/wiki/Shoe_(cards) is configured to contain 4 packs of cards. It is configured to have remaining cards discarded, and the shoe re-filled with a fresh set of 4 packs of cards when the penetration level of 75% is reached. Both of these settings can be altered by changing these attributes of the `Shoe` class,

~~~
self.decks = 4                 # Number of decks in the shoe when full.
self.penetration = 75 / 100    # Percentage of cards to be dealt before refilling shoe.
~~~

At the end of each game, the `replnesh` method should be called, to check whether the shoe has been depleted below the penetration level. If it has, then the shoe will be re-filled and all cards in the shoe shuffled.

#### Blackjack Value

A Blackjack can only be won with first two cards of first hand of a game. The attribute `blackjack_value` of the `Table` class is set to "3 for 2", which is standard the standard value of a Blackjack value in Vegas casinos (stake also returned). 
~~~
self.blackjack_value = 3 / 2        # Eg. £10 bet wins £15.
~~~

## Strategies
#### Dealer Strategy
The most basic strategy. This is the strategy that dealers must follow in Vegas casinos. It is also possible to run experiments where the player uses this strategy too.

_If current value of hand is 16 or less, then Hit, otherwise Stand._

#### Basic Strategy Section 1

This strategy is based on the first section of the Basic Strategy For Blackjack described here,

https://www.ebay.co.uk/itm/303101632202

This strategy builds on the Dealer Strategy, by taking into account the Dealer's up card as follows,

|     | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
|-----|---|---|---|---|---|---|---|---|----|---|
| **17+** | S | S | S | S | S | S | S | S | S  | S |
| **16**  | S | S | S | S | S | H | H | H | H  | H |
| **15**  | S | S | S | S | S | H | H | H | H  | H |
| **14**  | S | S | S | S | S | H | H | H | H  | H |
| **13**  | S | S | S | S | S | H | H | H | H  | H |
| **12**  | H | H | S | S | S | H | H | H | H  | H |

H = "Hit", S = "Stand".

Each row is a different value of the Player's hand. Each column is a different value of the Dealer's up card.


#### Basic Strategy Section 2

This strategy is based on the second section of the Basic Strategy For Blackjack.

This strategy builds on the Section 1 Strategy and the Dealer Strategy, by taking into account the Dealer's up card to make a decision about whether to Double Up the stake after seeing the first 2 cards of the hand. Note, that Blackjack rules says that after Doubing Up, the player receives just 1 more card; further Hitting is not permitted. Whenever this strategy decides not to Double Up, it reverts to Section 1 Strategy for playing the rest of the hand.

|     | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
|-----|---|---|---|---|---|---|---|---|----|---|
| **11** | D | D | D | D | D | D | D | D | D  | H |
| **10**  | D | D | D | D | D | D | D | D | H  | H |
| **9**  | H | D | D | D | D | H | H | H | H  | H |
| **5-8**  | H | H | H | H | H | H | H | H | H  | H |

H = "Hit", D = "Double Down".

Each row is a different value of the Player's hand. Each column is a different value of the Dealer's up card.