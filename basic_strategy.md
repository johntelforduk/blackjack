

#### Basic Strategy Section 1

This strategy is based on the first section of the Basic Strategy For Blackjack described here,

https://www.ebay.co.uk/itm/303101632202

This strategy builds on the Dealer Strategy, by taking into account the Dealer's up card as follows,

|     | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
|-----|---|---|---|---|---|---|---|---|----|---|
| **17+** | S | S | S | S | S | S | S | S | S | S |
| **16**  | S | S | S | S | S | H | H | H | H | H |
| **15**  | S | S | S | S | S | H | H | H | H | H |
| **14**  | S | S | S | S | S | H | H | H | H | H |
| **13**  | S | S | S | S | S | H | H | H | H | H |
| **12**  | H | H | S | S | S | H | H | H | H | H |

H = "Hit", S = "Stand".

Each row is a different value of the Player's hand. Each column is a different value of the Dealer's up card.


#### Basic Strategy Section 2

This strategy is based on the second section of the Basic Strategy For Blackjack.

This strategy builds on the Section 1 Strategy and the Dealer Strategy, by taking into account the Dealer's up card to make a decision about whether to Double Up the stake after seeing the first 2 cards of the hand. Note, that Blackjack rules says that after Doubing Up, the player receives just 1 more card; further Hitting is not permitted. Whenever this strategy decides not to Double Up, it reverts to Section 1 Strategy for playing the rest of the hand.

|     | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
|-----|---|---|---|---|---|---|---|---|----|---|
| **11** | D | D | D | D | D | D | D | D | D | H |
| **10**  | D | D | D | D | D | D | D | D | H | H |
| **9**  | H | D | D | D | D | H | H | H | H | H |
| **5-8**  | H | H | H | H | H | H | H | H | H | H |

H = "Hit", D = "Double Down".

Each row is a different value of the Player's hand. Each column is a different value of the Dealer's up card.

#### Basic Strategy Section 3

This strategy is based on the third section of the Basic Strategy For Blackjack.

This strategy builds on the Section 1 & 2 Strategies and the Dealer Strategy, by adding special rules when one of the player's cards is an ace. 

|     | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
|-----|---|---|---|---|---|---|---|---|----|---|
| **A, 8-10** | S | S | S | S | S | S | S | S | S | S |
| **A, 7**  | S | D | D | D | D | S | S | H | H | H |
| **A, 6**  | H | D | D | D | D | H | H | H | H | H |
| **A, 5**  | H | H | D | D | D | H | H | H | H | H |
| **A, 4**  | H | H | D | D | D | H | H | H | H | H |
| **A, 3**  | H | H | H | D | D | H | H | H | H | H |
| **A, 2**  | H | H | H | D | D | H | H | H | H | H |

H = "Hit", D = "Double Down", S = "Stand".

Each row is a different value of the Player's hand. Each column is a different value of the Dealer's up card.

#### Basic Strategy Section 4

This strategy is based on the fourth section of the Basic Strategy For Blackjack.

This strategy builds on Sections 1, 2 & 3 Strategies and the Dealer Strategy, by adding special rules when both of the player's first 2 cards in a hand are of equal value. Amongst other things, the player has the option to Split their hand if their first two cards are of equal value.

|     | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | A |
|-----|---|---|---|---|---|---|---|---|----|---|
| **A, A or 8, 8** | SP | SP | SP | SP | SP | SP | SP | SP | SP  | SP |
| **10, 10**  | S | S | S | S | S | S | S | S | S  | S |
| **9, 9**  | SP | SP | SP | SP | SP | S | SP | SP | S | S |
| **7, 7**  | SP | SP | SP | SP | SP | SP | H | H | H | H |
| **6, 6**  | SP | SP | SP | SP | SP | H | H | H | H  | H |
| **5, 5**  | D | D | D | D | D | D | D | D | H | H |
| **4, 4**  | H | H | H | SP | SP | H | H | H | H | H |
| **3, 3**  | SP | SP | SP | SP | SP | SP | H | H | H | H |
| **2, 2**  | SP | SP | SP | SP | SP | SP | H | H | H | H |

SP = "Split, H = "Hit", D = "Double Down", S = "Stand".

Each row is a different value of the Player's hand. Each column is a different value of the Dealer's up card.