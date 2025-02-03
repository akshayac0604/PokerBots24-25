import random
import numpy as np
from g_state import G_State
from clusters import *
class Node:
    def __init__(self, game_state, type_of_node):
        self.player = game_state.player # current player
        cards = "".join(game_state.hands[self.player] + game_state.community_cards)
        closest_deck = Clusters.closest_cluster(cards)
        community_cards = closest_deck[4:]
        self.hand = [closest_deck[:2], closest_deck[2:4]] # current player's hand, change to nearest cluster
        self.bounty = game_state.bounties # array of bounties
        self.community_cards = [community_cards[i:i+2] for i in range(0, len(community_cards), 2)] # community cards, change to nearest cluster
        if len(game_state.history) > 0:
            self.history = game_state.history
        else:
            self.history = []
        self.type = type_of_node
        self.actions = G_State.get_available_actions(game_state, type_of_node) # possible actions that current player can take
        self.regret = {} # regrets
        self.strategy = {} # strategy
        self.strategySum = {} # strategy sum
        if len(self.actions) != 0:
            self.regret = {a: 0 for a in self.actions}
            self.strategy = {a: 1/len(self.actions) for a in self.actions} # strategy
            self.strategySum = {a: 0 for a in self.actions}
        self.p_sum = [0, 0] # sum of probabilities that players would play to this node
        self.visits = 0 # sum of possible paths to this node in this training iteration
        self.T = 0 # sum of visits across training iterations
        self.v = 0 # expected game value for current player at this node
    def __str__(self):
        return str(self.T)
    def __hash__(self):
        if len(self.community_cards) != 0:
            return hash((self.player,tuple(self.hand), tuple(self.bounty), tuple(self.community_cards), tuple(self.history), tuple(self.actions)))
        return hash((self.player, tuple(self.hand), self.bounty[self.player], tuple(self.community_cards), tuple(self.history), tuple(self.actions)))
    def convert(self):
        if len(self.community_cards) != 0:
            return (self.player,tuple(self.hand), tuple(self.bounty), tuple(self.community_cards), tuple(self.history), tuple(self.actions))
        return (self.player, tuple(self.hand), self.bounty[self.player], tuple(self.community_cards), tuple(self.history), tuple(self.actions))
    def getAverageStrategy(self): 
        num_actions = len(self.actions)
        avgStrategy = {}
        normalizingSum = 0
        for action in self.actions:
            normalizingSum += self.strategySum[action]
        for action in self.actions:
            if normalizingSum > 0:
                avgStrategy[action] = self.strategySum[action] / normalizingSum
            else:
                avgStrategy[action] = 1 / num_actions
        return avgStrategy
    def getStrategy(self, realization_weight):
        reg = self.regret
        strategy_sum = self.strategySum
        strat = self.strategy
        normalizingSum = 0
        num_actions = len(self.actions)
        for action in self.actions:
            if reg[action] > 0:
                strat[action] = reg[action]
            else:
                strat[action] = 0
            normalizingSum += strat[action]
        for action in self.actions:
            if normalizingSum > 0:
                strat[action] = strat[action]/normalizingSum
            else:
                strat[action] = 1/num_actions
            strategy_sum[action] += realization_weight * strat[action]
        return (strat, strategy_sum)
    def getAction(strategy, k):
        poss_actions = strategy[k]
        strat_keys = list(poss_actions.keys())
        strat_values = [poss_actions[k] for k in strat_keys]
        return random.choices(strat_keys, weights= strat_values, k=1)[0]

    
        


