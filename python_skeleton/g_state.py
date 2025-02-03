from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from custom_types.card import *
import random
class G_State:
    def __init__(self, hand, bounty, communitycards, hist, stack, num_actions_round, current_player): 
        self.hands = hand #hands of players
        self.bounties = bounty #bounties of players
        self.community_cards = communitycards # community cards
        self.history = hist # history of past actions
        self.stacks = stack #stacks of players
        self.num_round = num_actions_round # number of turns players has taken this round
        self.player = current_player # player 0 is SB, player 1 is BB
    def __str__(self):
        return str((self.hands, self.bounties, self.history, self.stacks, self.community_cards, self.num_round, self.player))
    def initial_game_state():
        all_cards = list(New_Card.all_Cards())
        random.shuffle(all_cards)
        hand_0 = all_cards[:2]
        hand_1 = all_cards[2:4]
        bounty_0 = 0
        bounty_1 = 0
        r1 = random.uniform(0,1)
        if r1 < 0.33:
            [bounty_0, bounty_1] = [True, True]
        elif r1 >= 0.33 and r1 < 0.66:
            [bounty_0, bounty_1] = [False, True]
        elif r1 >= 0.66:
            [bounty_0, bounty_1] = [True, False]
        return G_State([hand_0, hand_1], [bounty_0, bounty_1], [], [], [STARTING_STACK-1, STARTING_STACK-2], [0, 0], 0)
    def get_betting_pos(self): # who goes first in each round
        if self.player == 0 and len(self.community_cards) == 0: # small blind and preflop
            return 0
        if self.player == 1 and len(self.community_cards) > 0: # big blind and postflop
            return 0
        return 1 #0 if went first, 1 if went second in betting round
    def get_available_actions(self, type_of_node):
        curr_player = self.player
        avail_actions = []
        if type_of_node == "terminal":
            return []
        num_this_round = self.num_round[curr_player]
        if self.stacks[curr_player] == self.stacks[1-curr_player]:
            avail_actions.append("check")
            if self.stacks[curr_player] != 0:
                if num_this_round == 0 or (num_this_round == 1 and self.get_betting_pos() == 0): # first time this round
                    avail_actions.append("raise1")
                    avail_actions.append("raise2")
        else:
            avail_actions.append("fold")
            avail_actions.append("call")
            if self.stacks[1-curr_player] != 0:
                if num_this_round == 0: # first time this round
                    avail_actions.append("raise1")
                    avail_actions.append("raise2")
        return avail_actions
    def get_raise_costs(self):
        curr_player = self.player
        continue_cost = self.stacks[curr_player] - self.stacks[1-curr_player]
        max_contribution = min(self.stacks[curr_player], self.stacks[1-curr_player] + continue_cost)
        min_contribution = min(max_contribution, continue_cost + max(continue_cost, BIG_BLIND))
        return (min_contribution, max_contribution)
    def new_stacks(self, amount):
        curr_player = self.player
        n_stacks = [0, 0]
        n_stacks[1-curr_player] = self.stacks[1-curr_player]
        n_stacks[curr_player] = self.stacks[curr_player] - amount
        return n_stacks
    def new_history(self, action):
        n_history = [self.history[i] for i in range(len(self.history))]
        n_history.append((self.player, action))
        return n_history
    def new_num(self):
        n_num = [self.num_round[i] for i in range(2)]
        n_num[self.player] += 1
        return n_num    
    def proceed_street(self):
        if len(self.community_cards) == 5:
            return (self, "terminal")
        old_street = len(self.community_cards)
        new_street = 3 if len(self.community_cards) == 0 else len(self.community_cards)  + 1
        new_deck = [c for c in list(New_Card.all_Cards()) if c not in self.hands[0] + self.hands[1] + self.community_cards]
        new_community_cards = new_deck[:new_street - old_street]
        return (G_State(self.hands, self.bounties, self.community_cards + new_community_cards, self.history, self.stacks, [0, 0], 1), "player")
    def update_state(self, action):
        curr_player = self.player
        n_history = self.new_history(action)
        n_num = self.new_num()
        current_raise_costs = self.get_raise_costs()
        min_contribution = current_raise_costs[0]
        max_contribution = current_raise_costs[1]
        if action == "raise1":
            ratio = max_contribution//min_contribution
            amount = min(ratio, 2) * min_contribution
            n_stacks = self.new_stacks(amount)
            return (G_State(self.hands, self.bounties, self.community_cards, n_history, n_stacks, n_num, 1-curr_player), "player")
        elif action == "raise2":
            amount = max_contribution
            n_stacks = self.new_stacks(amount)
            return (G_State(self.hands, self.bounties, self.community_cards, n_history, n_stacks, n_num, 1-curr_player), "player")
        elif action == "call":
            n_stacks = self.new_stacks(self.stacks[curr_player] - self.stacks[1-curr_player])
            if self.player == 0 and len(self.community_cards) == 0 and self.num_round[0] == 0: #SB calls BB
                return (G_State(self.hands, self.bounties, self.community_cards, n_history, n_stacks, n_num, 1-curr_player), "player")
            else:
                new_state = G_State(self.hands, self.bounties, self.community_cards, n_history, n_stacks, n_num, 1-curr_player)
                return new_state.proceed_street()
        elif action == "check":
            if sum(n_num) >= 2:
                new_state = G_State(self.hands, self.bounties, self.community_cards, n_history, self.stacks, n_num, 1)
                return new_state.proceed_street()
            return (G_State(self.hands, self.bounties, self.community_cards, n_history, self.stacks, n_num, 1-curr_player), "player")
        elif action == "fold":
            return (G_State(self.hands, self.bounties, self.community_cards, n_history, self.stacks, n_num, 1-curr_player), "terminal")
            
        
        
        

        
         
        
        

        
        






    



            















        
