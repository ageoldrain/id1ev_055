from otree.api import *
import random

doc = """
Curiosity and Information Demand
"""

debug = False

class C(BaseConstants):
    NAME_IN_URL = 'coin_flip'
    PLAYERS_PER_GROUP = None
    NUM_INTRO_PAGES = 4  # Number of introduction pages
    PRACTICE_ROUNDS = 3  # Number of practice rounds
    REAL_ROUNDS = 10     # Number of real rounds
    NUM_ROUNDS = NUM_INTRO_PAGES + PRACTICE_ROUNDS + REAL_ROUNDS

class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.fair_coin_value = cu(random.choice([1, 2]))
            player.biased_coin_value = cu(random.choice([1, 2]))

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Player's choice between 'fair' or 'biased' coin
    coin_choice = models.StringField(choices=['fair', 'biased'])
    chosen_coin = models.StringField()
    fair_coin_value = models.CurrencyField()
    biased_coin_value = models.CurrencyField()

    prolific_id = models.StringField(
        label="Please enter your unique Prolific ID here:",
        blank=False,
        max_length=100,
    )
    
    signature = models.StringField(
        label="Please sign (type your full name here)",
        blank=False,
        max_length=200,
    )

    # in coin_flip/models.py, inside class Player(BasePlayer):
    compq1 = models.StringField(
    choices=['True','False'], 
    label="Your answer to question 1"
    )
    compq2 = models.StringField(
    choices=['True', 'False'],
    label='Your answer to question 2'
    )
    compq3 = models.StringField(
    choices=['True', 'False'],
    label='Your answer to question 3'
    )

    how_decisions = models.LongStringField(
        label='How did you make your decisions?',
        blank=False,
        max_length=1000,
    )

    experiment_purpose = models.LongStringField(
        label='What do you think the experiment was about?',
        blank=False,
        max_length=1000,
    )    
    



    # Player's guesses for the outcome of each coin
    fair_outcome = models.StringField(
        choices=['H', 'T'],
        label="Your guess for the outcome of the Fair coin"
    )
    biased_outcome = models.StringField(
        choices=['H', 'T'],
        label="Your guess for the outcome of the Biased coin"
    )

    # Results
    chosen_coin_result = models.StringField()
    fair_coin_result = models.StringField()
    biased_coin_result = models.StringField()
    coin_permutation_choice = models.StringField()
    coin_permutation_result = models.StringField()
    coin_order = models.StringField()  # Store the order of the coins (e.g., 'fair,biased' or 'biased,fair')

    total_winnings = models.CurrencyField(initial=cu(0))

    def flip_chosen_coin(self, p_fair: float, p_biased: float):
        """
        Flip both coins and store the results.
        """
        assert 0 <= p_fair <= 1, "Probability for the fair coin must be between 0 and 1."
        assert 0 <= p_biased <= 1, "Probability for the biased coin must be between 0 and 1."

        # Flip the fair coin
        self.fair_coin_result = 'H' if random.random() < p_fair else 'T'
        # Flip the biased coin
        self.biased_coin_result = 'H' if random.random() < p_biased else 'T'

        # Store the result of the chosen coin
        if self.coin_choice == 'fair':
            self.chosen_coin_result = self.fair_coin_result
        elif self.coin_choice == 'biased':
            self.chosen_coin_result = self.biased_coin_result

        # Combine the coin outcomes into a permutation result
        self.coin_permutation_result = f"{self.fair_coin_result}{self.biased_coin_result}"

        if debug:
            print(f"Fair coin result: {self.fair_coin_result}")
            print(f"Biased coin result: {self.biased_coin_result}")
            print(f"Chosen coin: {self.coin_choice}")
            print(f"Chosen coin result: {self.chosen_coin_result}")
            print(f"Coin permutation result: {self.coin_permutation_result}")

    def calculate_winnings(self):
        real_round_number = self.round_number - C.NUM_INTRO_PAGES - C.PRACTICE_ROUNDS
        if real_round_number > 0:
            if self.fair_outcome == self.fair_coin_result and self.biased_outcome == self.biased_coin_result:
                round_winnings = self.fair_coin_value + self.biased_coin_value
            else:
                round_winnings = cu(0)
            previous_total = self.in_round(self.round_number - 1).total_winnings if self.round_number > 1 else cu(0)
            self.total_winnings = previous_total + round_winnings
        else:
            if debug:
                print(f"Round {self.round_number} is a practice round. No winnings added.")
