# Study the effect of different shoe sizes (number of decks of cards in the shoe when replenished) and different
# penetration setting (percentage of cards in shoe left to trigger replenishment).

import blackjack
import csv
from statistics import mean
from statistics import stdev

class Shoe_Experiment:

    def __init__(self, sessions, rounds_per_session, decks, penetration):
        self.strategy_name = "Hi-Lo Card Count"
        self.win_loss = []                              # List of percentage win(+ve) or loss(-ve) per session.
        self.sessions = sessions                        # Number of sessions (visits to table) to do in this study.
        self.rounds_per_session = rounds_per_session    # Number of rounds to be played in each session.
        self.decks = decks                              # Number of decks put in shoe when it is replenished.
        self.penetration = penetration                  # Penetration percentage that causes shoe to be replenished.
        self.player_hands = 0                           # Number of hands that the player has played in the study.
        self.grand_total_staked = 0                     # Grand total of money staked in all games in all sessions.
        self.min_player_edge = 0                        # Stats calculated by analysing items in win_loss list...
        self.max_player_edge = 0
        self.average_player_edge = 0
        self.standard_deviation_edge = 0                # ...

        self.run()                                      # Run the shoe study.
        self.analyse()                                  # Analyse the shoe study.

    # Run the study.
    def run(self):
        for experiments in range(self.sessions):
            this_table = blackjack.Table(self.decks, self.penetration)

            for games in range(self.rounds_per_session):
                this_table.play_one_round(self.strategy_name)

            self.win_loss.append(this_table.amount_won_or_lost / this_table.total_staked)

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
        print("Decks:", self.decks)
        print("Penetration: %.2f%%" % (100.0 * self.penetration))
        print("Total number of player hands:", self.player_hands)
        print("Total money staked=£%d" % self.grand_total_staked)
        print("Min player edge: %.2f%%" % (100.0 * self.min_player_edge))
        print("Max player edge: %.2f%%" % (100.0 * self.max_player_edge))
        print("Average player edge: %.2f%%" % (100.0 * self.average_player_edge))
        print("(-ve means house is ahead, +ve means player is ahead)")
        print("Standard deviation: %.2f" % (100 * self.standard_deviation_edge))
        print()

        return self

class Shoe_Study:

    def __init__(self, sessions, rounds_per_session):
        self.experiments = []

        for d in [1, 2, 4, 6, 8]:
            for p in [0.50, 0.75, 0.85]:
                self.experiments.append(Shoe_Experiment(sessions, rounds_per_session, d, p))

    def write_to_file(self):
        with open('shoe_study_results.csv', newline='', mode='w') as results:
            experiment_writer = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            experiment_writer.writerow(["decks", "penetration", "average_player_edge"])

            for ex in self.experiments:
                experiment_writer.writerow([ex.decks, ex.penetration, ex.average_player_edge])

blackjack.verbose = False

this_study = Shoe_Study(10, 100000)
this_study.write_to_file()
