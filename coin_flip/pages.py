from otree.api import Page, WaitPage
import random

from .models import C, Player

P_FAIR = 0.5
P_BIASED = 0.55


# ──────────────────────────────────────────────────────────────────────────────
# Introduction
# ──────────────────────────────────────────────────────────────────────────────
class Introduction(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    def is_displayed(self):
        return self.round_number == 1


class Introduction1point5(Page):
    def is_displayed(self):
        return self.round_number == 2


class Introduction1point6(Page):
    def is_displayed(self):
        return self.round_number == 3


class Introduction2(Page):
    form_model  = 'player'
    form_fields = ['signature']
    template_name = 'coin_flip/Instructions2.html'

    def is_displayed(self):
        return self.round_number == 4

    def before_next_page(self):
        self.participant.vars['intro_completed'] = True






# ──────────────────────────────────────────────────────────────────────────────
# Comprehension Q1 + Feedback1
# ──────────────────────────────────────────────────────────────────────────────
class CompQuestion1(Page):
    form_model = 'player'
    form_fields = ['compq1']

    def is_displayed(self):
        return self.subsession.round_number == C.NUM_INTRO_PAGES + 1


class Feedback1(Page):
    form_model = 'player'
    form_fields = []
    template_name = 'coin_flip/Feedback1.html'

    def is_displayed(self):
        return self.subsession.round_number == C.NUM_INTRO_PAGES + 1


# ──────────────────────────────────────────────────────────────────────────────
# Comprehension Q2 + Feedback2
# ──────────────────────────────────────────────────────────────────────────────
class CompQuestion2(Page):
    form_model = 'player'
    form_fields = ['compq2']

    def is_displayed(self):
        return self.subsession.round_number == C.NUM_INTRO_PAGES + 1


class Feedback2(Page):
    form_model = 'player'
    form_fields = []
    template_name = 'coin_flip/Feedback2.html'

    def is_displayed(self):
        return self.subsession.round_number == C.NUM_INTRO_PAGES + 1


# ──────────────────────────────────────────────────────────────────────────────
# Comprehension Q3 + Feedback3
# ──────────────────────────────────────────────────────────────────────────────
class CompQuestion3(Page):
    form_model = 'player'
    form_fields = ['compq3']

    def is_displayed(self):
        return self.subsession.round_number == C.NUM_INTRO_PAGES + 1


class Feedback3(Page):
    form_model = 'player'
    form_fields = []
    template_name = 'coin_flip/Feedback3.html'

    def is_displayed(self):
        return self.subsession.round_number == C.NUM_INTRO_PAGES + 1


# ──────────────────────────────────────────────────────────────────────────────
# Practice Rounds
# ──────────────────────────────────────────────────────────────────────────────
class PracticeChooseCoin(Page):
    form_model = 'player'
    form_fields = ['coin_choice']
    template_name = 'coin_flip/PracticeChooseCoin.html'

    def vars_for_template(self):
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins
        self.player.coin_order = ','.join([coin[0] for coin in coins])
        pr = self.round_number - C.NUM_INTRO_PAGES
        return {
            'coins': coins,
            'practice_round_number': pr,
            'is_practice_round': True,
            'fair_coin_value': self.player.fair_coin_value,
            'biased_coin_value': self.player.biased_coin_value,
        }

    def before_next_page(self):
        self.player.chosen_coin = self.player.coin_choice
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return C.NUM_INTRO_PAGES < self.round_number <= C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS


class PracticeRevealCoinOutcome(Page):
    template_name = 'coin_flip/PracticeRevealCoinOutcome.html'

    def vars_for_template(self):
        pr = self.round_number - C.NUM_INTRO_PAGES
        return {
            'chosen_coin': self.player.chosen_coin.capitalize(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'practice_round_number': pr,
            'is_practice_round': True,
        }

    def is_displayed(self):
        return C.NUM_INTRO_PAGES < self.round_number <= C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS


class PracticeChoosePermutation(Page):
    form_model = 'player'
    template_name = 'coin_flip/PracticeChoosePermutation.html'

    def get_form_fields(self):
        coins = self.participant.vars['coin_order']
        return [f"{coin[0]}_outcome" for coin in coins]

    def vars_for_template(self):
        coins = self.participant.vars['coin_order']
        pr = self.round_number - C.NUM_INTRO_PAGES
        return {
            'coins': coins,
            'practice_round_number': pr,
            'is_practice_round': True,
            'fair_coin_value': self.player.fair_coin_value,
            'biased_coin_value': self.player.biased_coin_value,
        }

    def before_next_page(self):
        coins = self.participant.vars['coin_order']
        outcomes = [getattr(self.player, f"{coin[0]}_outcome") for coin in coins]
        self.player.coin_permutation_choice = ''.join(outcomes)

    def is_displayed(self):
        return C.NUM_INTRO_PAGES < self.round_number <= C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS


# ──────────────────────────────────────────────────────────────────────────────
# Real Rounds
# ──────────────────────────────────────────────────────────────────────────────
class RoundInfo(Page):
    template_name = 'coin_flip/RoundInfo.html'

    def vars_for_template(self):
        rr = self.round_number - C.NUM_INTRO_PAGES - C.PRACTICE_ROUNDS
        return {
            'real_round_number': rr,
            'is_practice_round': False,
        }

    def is_displayed(self):
        return self.round_number > C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS


class ChooseCoin(Page):
    form_model = 'player'
    form_fields = ['coin_choice']
    template_name = 'coin_flip/ChooseCoin.html'

    def vars_for_template(self):
        coins = [('fair', 'Fair'), ('biased', 'Biased')]
        random.shuffle(coins)
        self.participant.vars['coin_order'] = coins
        self.player.coin_order = ','.join([coin[0] for coin in coins])
        rr = self.round_number - C.NUM_INTRO_PAGES - C.PRACTICE_ROUNDS
        return {
            'coins': coins,
            'real_round_number': rr,
            'is_practice_round': False,
            'fair_coin_value': self.player.fair_coin_value,
            'biased_coin_value': self.player.biased_coin_value,
        }

    def before_next_page(self):
        self.player.chosen_coin = self.player.coin_choice
        self.player.flip_chosen_coin(p_fair=P_FAIR, p_biased=P_BIASED)

    def is_displayed(self):
        return self.round_number > C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS


class RevealCoinOutcome(Page):
    template_name = 'coin_flip/RevealCoinOutcome.html'

    def vars_for_template(self):
        rr = self.round_number - C.NUM_INTRO_PAGES - C.PRACTICE_ROUNDS
        return {
            'chosen_coin': self.player.chosen_coin.capitalize(),
            'chosen_coin_result': self.player.chosen_coin_result,
            'real_round_number': rr,
            'is_practice_round': False,
        }

    def is_displayed(self):
        return self.round_number > C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS


class ChoosePermutation(Page):
    form_model = 'player'
    template_name = 'coin_flip/ChoosePermutation.html'

    def get_form_fields(self):
        coins = self.participant.vars['coin_order']
        return [f"{coin[0]}_outcome" for coin in coins]

    def vars_for_template(self):
        coins = self.participant.vars['coin_order']
        rr = self.round_number - C.NUM_INTRO_PAGES - C.PRACTICE_ROUNDS
        return {
            'coins': coins,
            'real_round_number': rr,
            'is_practice_round': False,
            'fair_coin_value': self.player.fair_coin_value,
            'biased_coin_value': self.player.biased_coin_value,
        }

    def before_next_page(self):
        coins = self.participant.vars['coin_order']
        outcomes = [getattr(self.player, f"{coin[0]}_outcome") for coin in coins]
        self.player.coin_permutation_choice = ''.join(outcomes)
        self.player.calculate_winnings()

    def is_displayed(self):
        return self.round_number > C.NUM_INTRO_PAGES + C.PRACTICE_ROUNDS

class PostQuestion1(Page):
    form_model = 'player'
    form_fields = ['how_decisions']
    template_name = 'coin_flip/PostQuestion1.html'

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS


class PostQuestion2(Page):
    form_model = 'player'
    form_fields = ['experiment_purpose']
    template_name = 'coin_flip/PostQuestion2.html'
    
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS


class Results(Page):
    def vars_for_template(self):
        return {'winnings': self.player.total_winnings}

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS


page_sequence = [
    Introduction,
    Introduction1point5,
    Introduction1point6,
    Introduction2,

    # Comprehension checks (all before practice)
    CompQuestion1,
    Feedback1,
    CompQuestion2,
    Feedback2,
    CompQuestion3,
    Feedback3,

    # Practice rounds
    PracticeChooseCoin,
    PracticeRevealCoinOutcome,
    PracticeChoosePermutation,

    # Real rounds
    RoundInfo,
    ChooseCoin,
    RevealCoinOutcome,
    ChoosePermutation,
    # Debrief questions
    PostQuestion1,
    PostQuestion2,
    
    # Final
    Results,
]
