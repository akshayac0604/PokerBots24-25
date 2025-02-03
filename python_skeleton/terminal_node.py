import eval7
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from custom_types.card import *
import math
class Terminal_Node():
    def __init__(self, game_state):
        self.hands = game_state.hands
        self.bounties = game_state.bounties
        self.community_cards = game_state.community_cards
        self.stacks = game_state.stacks
        self.history = game_state.history[len(game_state.history)-1]
    def calc_utility(self):
        pot_size = 2*STARTING_STACK - sum(self.stacks)
        player_sb_cont = STARTING_STACK - self.stacks[0]
        player_bb_cont = STARTING_STACK - self.stacks[1]
        player_cont = [player_sb_cont, player_bb_cont]
        bounty = self.bounties
        if self.history[1] == "fold":
            player_fold = self.history[0]
            old_winnings = pot_size - player_cont[1-player_fold]
            if bounty[1-player_fold]:
                new_winnings = 1.5*old_winnings + 10
                if player_fold == 0:
                    new_winnings = math.ceil(new_winnings)
                    return [-new_winnings, new_winnings]
                else:
                    new_winnings = math.floor(new_winnings)
                    return [new_winnings, -new_winnings]
            return [-old_winnings, old_winnings] if player_fold == 0 else [old_winnings, -old_winnings]
        player_sb_hand = [eval7.Card(c) for c in self.hands[0] + self.community_cards]
        player_bb_hand = [eval7.Card(c) for c in self.hands[1] + self.community_cards]
        player_sb_bounty = self.bounties[0]
        player_bb_bounty = self.bounties[1]
        hand_sb = eval7.evaluate(player_sb_hand)
        hand_bb = eval7.evaluate(player_bb_hand)
        if hand_sb > hand_bb:
            old_winnings = pot_size - player_sb_cont
            if self.bounties[0]:
                new_winnings = math.floor(1.5*old_winnings+10)
                return [new_winnings, -new_winnings]
            return [old_winnings, -old_winnings]
        if hand_sb == hand_bb:
            old_winnings = pot_size/2
            if len(set(self.bounties)) == 1:
                return [old_winnings, -old_winnings]
            return [math.floor(3/8*pot_size + 10), math.ceil(1/4*pot_size)] if player_sb_bounty else [math.floor(1/4*pot_size), math.ceil(3/8*pot_size + 10)]
        old_winnings = pot_size - player_bb_cont
        if player_bb_bounty:
            new_winnings = math.ceil(1.5*old_winnings+10)
            return [-new_winnings, new_winnings]
        return [-old_winnings, old_winnings]

        

                 


