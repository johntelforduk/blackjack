import blackjack
from statistics import mean
from statistics import stdev

class Study:

    def __init__(self, strategy_name, sessions, games_per_session):
        self.strategy_name = strategy_name          # Name of the player strategy to be tested.
        self.win_loss = []                          # List of percentage win(+ve) or loss(-ve) per session.
        self.sessions = sessions                    # Number of sessions (visits to table) to do in this study.
        self.games_per_session = games_per_session  # Number of games to be started in each session.
        self.player_hands = 0                       # Number of hands that the player has played in the study.
        self.grand_total_staked = 0                 # Grand total of money staked in all games in all sessions.
        self.run()

    # Run the study.
    def run(self):
        for experiments in range(self.sessions):
            this_table = blackjack.Table()

            for games in range(self.games_per_session):
                this_table.play_one_game(self.strategy_name)

            # Multiply by 100 to make it a percentage.
            self.win_loss.append(100 * this_table.amount_won_or_lost / this_table.total_staked)
            self.player_hands += this_table.hands_played_by_player
            self.grand_total_staked += this_table.total_staked

            del this_table
        self.analyse()

    # Print out analysis of the results of the study.
    def analyse(self):
        print("Player strategy:", self.strategy_name)
        print("Number of sessions:", self.sessions)
        print("Games per session:", self.games_per_session)
        print("Total number of player hands:", self.player_hands)
        print("Total money staked=£%d" % self.grand_total_staked)
        print("Max house edge: %.2f%%" % max(self.win_loss))
        print("Min house edge: %.2f%%" % min(self.win_loss))
        print("Average house edge: %.2f%%" % mean(self.win_loss))
        print("(-ve means house is ahead, +ve means player is ahead)")
        print("Standard deviation: %.2f" % stdev(self.win_loss))
        print()


blackjack.verbose = False

s1 = Study("Dealer", 10, 10000)
s2 = Study("Basic Strategy Section 1", 10, 10000)
s3 = Study("Basic Strategy Section 2", 10, 10000)
s4 = Study("Basic Strategy Section 3", 10, 10000)
s5 = Study("Basic Strategy Section 4", 10, 10000)
