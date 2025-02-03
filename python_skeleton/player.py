'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import pickle
from g_state import G_State
import time
import eval7
from node import *
from new_clusters import *
SCALE_FACTOR = 0.7
SCALE_RAISE = 1

import random


class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        self.prob_bounties = {"A":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1, "T":1, "J":1, "Q":1, "K":1}
        self.history = []
        self.num_round = [0, 0]
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.myscore = 0
        iter = 14760
        with open(f'convert_to_last_{iter}_1.pkl', 'rb') as file:
            self.avg_strategy_1 = pickle.load(file)
        with open(f'convert_to_last_{iter}_3.pkl', 'rb') as file:
            self.avg_strategy_3 = pickle.load(file)
        with open(f'convert_to_last_{iter}_1_without_actions.pkl', 'rb') as file:
            self.avg_strategy_1_without_actions = pickle.load(file)
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        pass

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        # with open("myhistory.txt", "w") as f:
        #     f.write("History: ")
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        self.round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your cards
        big_blind = bool(active)  # True if you are the big blind
        my_bounty = round_state.bounties[active]  # your current bounty rank
        if self.round_num % 25 == 1:
            self.prob_bounties = {"A":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1, "T":1, "J":1, "Q":1, "K":1}
            print(str(self.round_num) + " " + str((self.count1, self.count2, self.count3)))
        # with open("myhistory.txt", "w") as f:
        #     f.write("History: " + str([]))

        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        board_cards = previous_state.deck[:street]
        board_cards_rank = [card[0] for card in board_cards]
        my_cards = previous_state.hands[active]  # your cards
        my_cards_rank = [card[0] for card in my_cards]
        opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        opp_cards_rank = [card[0] for card in opp_cards]
        self.history = []
        self.num_round = [0, 0]
        self.myscore += my_delta
        my_bounty_hit = terminal_state.bounty_hits[active]  # True if you hit bounty
        round_num = game_state.round_num
        opponent_bounty_hit = terminal_state.bounty_hits[1-active] # True if opponent hit bounty
        bounty_rank = previous_state.bounties[active]  # your bounty rank
        if opponent_bounty_hit:
            if len(opp_cards) == 0: # they didn't show their cards
                for card in set(board_cards_rank):
                    if self.prob_bounties[card] != 0:
                        self.prob_bounties[card] += 0.6
            else:
                for card in self.prob_bounties:
                    if card in board_cards_rank + opp_cards_rank and self.prob_bounties[card] != 0:
                        self.prob_bounties[card] += 1
                    else:
                        self.prob_bounties[card] = 0
        else: # opponent bounty didn't hit
            if opp_cards: # didn't fold
                eval_my_cards = [eval7.Card(c) for c in my_cards + board_cards]
                eval_opp_cards = [eval7.Card(c) for c in opp_cards + board_cards]
                if eval7.evaluate(eval_my_cards) == eval7.evaluate(eval_opp_cards): # tie
                    for card in opp_cards_rank + board_cards_rank:
                        self.prob_bounties[card] = 0
                elif my_delta < 0: # lost
                    for card in opp_cards_rank + board_cards_rank:
                        self.prob_bounties[card] = 0
            else: # one of us folded
                if my_delta < 0: # I folded
                    for card in board_cards_rank:
                        self.prob_bounties[card] = 0

    def get_probabilities(self):
        sum_values = 0
        probabilities = {}
        for val in self.prob_bounties:
            sum_values += self.prob_bounties[val]
        if sum_values == 0:
            for val in self.prob_bounties:
                probabilities[val] = 1/13
        else:
            for val in self.prob_bounties:
                probabilities[val] = self.prob_bounties[val]/sum_values
        return probabilities
    
    def prob_bounty(self, round_state):
        street = round_state.street
        board_cards = round_state.deck[:street]
        board_cards = {card[0] for card in board_cards}
        probability_bounty = self.get_probabilities()
        prob_hole_cards = 0.15
        product_prob_board = 1
        for val in board_cards:
            product_prob_board = product_prob_board * (1 - probability_bounty[val])
        return prob_hole_cards + 0.85 * (1 - product_prob_board)
    
    def get_previous_move(self, round_state):
        prev_state = round_state.previous_state
        if prev_state == None:
            return []
        prev_active = prev_state.button % 2
        poss_actions = prev_state.legal_actions()
        if prev_state.street != round_state.street:
            if prev_state.previous_state == None:
                return [(prev_active, "check")]
            if prev_state.previous_state.stacks != round_state.stacks:
                return [(1-prev_active, "call")]
            return [(prev_active, "check")]
        if prev_state.stacks == round_state.stacks:
            return [(prev_active, "check")]
        if CallAction in poss_actions:
            if round_state.stacks[prev_active] == prev_state.stacks[1-prev_active] and round_state.stacks[1-prev_active] == prev_state.stacks[1-prev_active]:
                return [(prev_active, "call")]
        min_raise, max_raise = prev_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
        min_cost = min_raise - prev_state.pips[prev_active]  # the cost of a minimum bet/raise
        max_cost = max_raise - prev_state.pips[prev_active]  # the cost of a maximum bet/raise 
        amount_raise = prev_state.stacks[prev_active] - round_state.stacks[prev_active]
        ratio = max_cost//min_cost
        amount = min(ratio, 2) * min_cost
        if abs(amount_raise - amount) <= SCALE_FACTOR * abs(amount_raise - max_cost):
            return [(prev_active, "raise1")]
        return [(prev_active, "raise2")]
    
    def bounty_there(self, round_state, active):
        my_bounty = round_state.bounties[active]
        street = round_state.street
        board_cards = round_state.deck[:street]
        my_cards = round_state.hands[active]
        cards = [card[0] for card in board_cards + my_cards]
        # print("MB: " + str(my_bounty))
        # print("BC: " + str(board_cards))
        return str(my_bounty) in cards
    
    def get_raise_values(self, probabilties, min_cost, max_cost, max_raise, min_raise):
        ratio = max_cost // min_cost
        raise1_value = min(ratio, 2) * min_cost
        raise2_value = max_raise
        raise1_prob = probabilties["raise1"]
        raise2_prob = probabilties["raise2"]
        raise1_prob = raise1_prob/(raise1_prob+raise2_prob)    
        raise2_prob = raise2_prob/(raise1_prob+raise2_prob)
        amount = int((raise1_value*raise1_prob + raise2_prob*raise2_value)*SCALE_RAISE)    
        if amount > min_raise and amount < max_raise:
            return amount
        elif amount <= min_raise:
            return min_raise
        elif amount >= max_raise:
            return max_raise
    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        self.count3 += 1
        if self.myscore >= 3 * (1000 - self.round_num):
            return FoldAction()
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        if RaiseAction in legal_actions:
           min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
           min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
           max_cost = max_raise - my_pip  # the cost of a maximum bet/raise
        prev_move = self.get_previous_move(round_state)
        prev_state = round_state.previous_state
        if prev_state != None:
            prev_prev_state = prev_state.previous_state
            if prev_prev_state != None and prev_prev_state.street != prev_state.street:
                if self.history[-1][1] in {"raise1", "raise2"}:
                    self.num_round = [0, 0]
                    self.history.append((prev_move[0][0], "call"))
                elif self.history[-1][1] in {"check"}:
                    self.num_round = [0, 0]
                    self.history.append((prev_move[0][0], "check"))
                elif self.history[-1][1] in {"call"}:
                    if len(self.history) == 1:
                        self.history.append((prev_move[0][0], "check"))
                    self.num_round = [0, 0]
        if prev_move != [] and prev_move[0][0] != active:
            prev_move_tuple = prev_move[0]
            self.history.append(prev_move_tuple)
        if prev_state != None:
            if round_state.street != prev_state.street:
                self.num_round = [0, 0]
            else:
                self.num_round[1-active] += 1
        my_bounty_there = self.bounty_there(round_state, active)
        opp_bounty = False
        prob_of_bounty = self.prob_bounty(round_state)
        r = random.uniform(0, 1)
        if r < prob_of_bounty:
            opp_bounty = True
        new_history = self.history[-3:]
        if my_bounty_there == opp_bounty and len(board_cards) != 0:
            my_bounty_there, opp_bounty = True, True
        if active == 0:
            curr_game_state = G_State(round_state.hands, [my_bounty_there, opp_bounty], board_cards, new_history, round_state.stacks, self.num_round, active)
        else:
            curr_game_state = G_State(round_state.hands, [opp_bounty, my_bounty_there], board_cards, new_history, round_state.stacks, self.num_round, active)
        cards = "".join(round_state.hands[active] + board_cards)
        closest_deck = New_Clusters.closest_cluster(cards)
        community_cards = closest_deck[4:]
        my_cards = [closest_deck[:2], closest_deck[2:4]]
        community_cards = [community_cards[i:i+2] for i in range(0, len(community_cards), 2)]
        poss_actions = G_State.get_available_actions(curr_game_state, "player")
        if active == 0:
            if len(community_cards) != 0:
                info_dict_key = (active, tuple(my_cards), tuple([my_bounty_there, opp_bounty]), tuple(community_cards), tuple(new_history), tuple(poss_actions))
            else:
                info_dict_key = (active, tuple(my_cards), my_bounty_there, tuple(community_cards), tuple(new_history), tuple(poss_actions))
        else:
            if len(community_cards) != 0:
                info_dict_key = (active, tuple(my_cards), tuple([opp_bounty, my_bounty_there]), tuple(community_cards), tuple(new_history), tuple(poss_actions))
            else:
                info_dict_key = (active, tuple(my_cards), my_bounty_there, tuple(community_cards), tuple(new_history), tuple(poss_actions))
        if info_dict_key in self.avg_strategy_3:
            action = Node.getAction(self.avg_strategy_3, info_dict_key)
            self.count1 += 1
            if action == "fold" and FoldAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                return FoldAction()
            if action == "raise1" and RaiseAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                ratio = max_cost // min_cost
                raise1_value = min(ratio, 2) * min_cost
                return RaiseAction(raise1_value)
            if action == "raise2" and RaiseAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                raise_amount = self.get_raise_values(self.avg_strategy_3[info_dict_key], min_cost, max_cost, max_raise, min_raise)
                return RaiseAction(raise_amount)
            if action == "check" and CheckAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                return CheckAction()
            if action == "call" and CallAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                return CallAction()
        new_history = self.history[-1]
        if active == 0:
            if len(community_cards) != 0:
                info_dict_key = (active, tuple(my_cards), tuple([my_bounty_there, opp_bounty]), tuple(community_cards), (tuple(new_history),), tuple(poss_actions))
            else:
                info_dict_key = (active, tuple(my_cards), my_bounty_there, tuple(community_cards), (tuple(new_history),), tuple(poss_actions))
        else:
            if len(community_cards) != 0:
                info_dict_key = (active, tuple(my_cards), tuple([opp_bounty, my_bounty_there]), tuple(community_cards), (tuple(new_history),), tuple(poss_actions))
            else:
                info_dict_key = (active, tuple(my_cards), my_bounty_there, tuple(community_cards), (tuple(new_history),), tuple(poss_actions))
        if info_dict_key in self.avg_strategy_1:
            action = Node.getAction(self.avg_strategy_1, info_dict_key)
            self.count2 += 1
            # print("Actual History: " + str(self.history))
            if action == "fold" and FoldAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                return FoldAction()
            if action == "raise1" and RaiseAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                ratio = max_cost // min_cost
                raise1_value = min(ratio, 2) * min_cost
                return RaiseAction(raise1_value)
            if action == "raise2" and RaiseAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                raise_amount = self.get_raise_values(self.avg_strategy_1[info_dict_key], min_cost, max_cost, max_raise, min_raise)
                return RaiseAction(raise_amount)
            if action == "check" and CheckAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                return CheckAction()
            if action == "call" and CallAction in legal_actions:
                self.num_round[active] += 1
                self.history.append((active, action))
                return CallAction()
        if active == 0:
            if len(community_cards) != 0:
                info_dict_key = (active, tuple(my_cards), tuple([my_bounty_there, opp_bounty]), tuple(community_cards), (tuple(new_history),))
            else:
                info_dict_key = (active, tuple(my_cards), my_bounty_there, tuple(community_cards), (tuple(new_history),))
        else:
            if len(community_cards) != 0:
                info_dict_key = (active, tuple(my_cards), tuple([opp_bounty, my_bounty_there]), tuple(community_cards), (tuple(new_history),))
            else:
                info_dict_key = (active, tuple(my_cards), my_bounty_there, tuple(community_cards), (tuple(new_history),))
        if info_dict_key in self.avg_strategy_1_without_actions:
            action = Node.getAction(self.avg_strategy_1_without_actions, info_dict_key)
            self.count2 += 1
            if action == "fold" and FoldAction in legal_actions:
                self.history.append((active, action))
                self.num_round[active] += 1
                return FoldAction()
            if action == "raise1" and RaiseAction in legal_actions:
                self.history.append((active, action))
                self.num_round[active] += 1
                ratio = max_cost // min_cost
                raise1_value = min(ratio, 2) * min_cost
                return RaiseAction(raise1_value)
            if action == "raise2" and RaiseAction in legal_actions:
                self.history.append((active, action))
                self.num_round[active] += 1
                raise_amount = self.get_raise_values(self.avg_strategy_1_without_actions[info_dict_key], min_cost, max_cost, max_raise, min_raise)
                return RaiseAction(raise_amount)
            if action == "check" and CheckAction in legal_actions:
                self.history.append((active, action))
                self.num_round[active] += 1
                return CheckAction()
            if action == "call" and CallAction in legal_actions:
                self.history.append((active, action))
                self.num_round[active] += 1
                return CallAction()
            if CheckAction in legal_actions:
                self.history.append((active, "check"))
                self.num_round[active] += 1
                return CheckAction()
        if RaiseAction in legal_actions:
            if random.random() < 0.5:
                self.history.append((active, "raise1"))
                self.num_round[active] += 1
                ratio = max_cost // min_cost
                raise1_value = min(ratio, 2) * min_cost
                return RaiseAction(raise1_value)
        if CheckAction in legal_actions:
            self.history.append((active, "check"))
            self.num_round[active] += 1
            return CheckAction()
        if random.random() < 0.25:
            self.history.append((active, "fold"))
            self.num_round[active] += 1
            return FoldAction()
        self.history.append((active, "call"))
        self.num_round[active] += 1
        return CallAction()


if __name__ == '__main__':
    run_bot(Player(), parse_args())
