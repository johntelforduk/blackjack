# Do a study of several different strategies.

import blackjack
import csv
from statistics import mean
from statistics import stdev

class Experiment:

    def __init__(self, strategy_name, sessions, rounds_per_session):
        self.strategy_name = strategy_name          # Name of the player strategy to be tested.
        self.win_loss = []                          # List of percentage win(+ve) or loss(-ve) per session.
        self.sessions = sessions                    # Number of sessions (visits to table) to do in this study.
        self.rounds_per_session = rounds_per_session  # Number of rounds to be played in each session.
        self.player_hands = 0                       # Number of hands that the player has played in the study.
        self.grand_total_staked = 0                 # Grand total of money staked in all games in all sessions.
        self.min_player_edge = 0
        self.max_player_edge = 0
        self.average_player_edge = 0
        self.standard_deviation_edge = 0
        self.run()
        self.analyse()

    # Run the study.
    def run(self):
        for experiments in range(self.sessions):
            this_table = blackjack.Table(4,             # 4 Decks in the shoe.
                                         0.75)          # Shoe replenished when 75% penetration reached.

            for games in range(self.rounds_per_session):
                this_table.play_one_round(self.strategy_name)

            # Multiply by 100 to make it a percentage.
            self.win_loss.append(100 * this_table.amount_won_or_lost / this_table.total_staked)

            self.player_hands += this_table.hands_played_by_player
            self.grand_total_staked += this_table.total_staked

            del this_table

    # Print out analysis of the results of the study.
    def analyse(self):

        self.min_player_edge = min(self.win_loss)
        self.max_player_edge = max(self.win_loss)
        self.average_player_edge = mean(self.win_loss)
        self.standard_deviation_edge = stdev(self.win_loss)

        print("Player strategy:", self.strategy_name)
        print("Number of sessions:", self.sessions)
        print("Games per session:", self.rounds_per_session)
        print("Total number of player hands:", self.player_hands)
        print("Total money staked=£%d" % self.grand_total_staked)
        print("Min player edge: %.2f%%" % self.min_player_edge)
        print("Max player edge: %.2f%%" % self.max_player_edge)
        print("Average player edge: %.2f%%" % self.average_player_edge)
        print("(-ve means house is ahead, +ve means player is ahead)")
        print("Standard deviation: %.2f" % self.standard_deviation_edge)
        print()

        return self

class Study:

    def __init__(self, sessions, rounds_per_session):
        self.experiments = []

        # (Strategy Name, Number of Sessions, Rounds per Session)
        for ex in ["Dealer", "Basic Strategy Section 1", "Basic Strategy Section 2", "Basic Strategy Section 3",
                   "Basic Strategy Section 4", "Hi-Lo Card Count"]:

            self.experiments.append(Experiment(ex, sessions, rounds_per_session))

    def write_to_file(self):
        with open('study_results.csv', newline='', mode='w') as results:
            experiment_writer = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            experiment_writer.writerow(["strategy_name", "min_player_edge", "max_player_edge",
                                        "average_player_edge"])

            for ex in self.experiments:
                experiment_writer.writerow([ex.strategy_name, ex.min_player_edge, ex.max_player_edge,
                                            ex.average_player_edge])

blackjack.verbose = False

this_study = Study(10, 100000)
this_study.write_to_file()
