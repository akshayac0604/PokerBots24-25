from enum import Enum
from enum import IntEnum
from collections import defaultdict
import eval7
import random
from eval7 import Card

class New_Card(Card):
    def convert(cards):
        suite = ""
        if eval7.Card(cards[0]).suit == eval7.Card(cards[1]).suit:
            suite = "s"
        else:
            suite = "o"
        if eval7.Card(cards[0]).rank >= eval7.Card(cards[1]).rank:
            return cards[0][0] + cards[1][0] + suite
        return cards[1][0] + cards[0][0] + suite
    def convert_back(pair):
        poss_suits = ["s", "d", "h", "c"]
        suit1 = "s"
        card1 = pair[0] + suit1
        if pair[2] == "s":
            card2 = pair[1] + suit1
        else:
            suit2 = "d"
            card2 = pair[1] + suit2
        return [card1, card2]
    def convert_back_avoid(pair, avoid_cards):
        poss_suits = ["s", "d", "h", "c"]
        poss_options = []
        for suit1 in poss_suits:
            card1 = pair[0] + suit1
            if pair[2] == "s":
                card2 = pair[1] + suit1
                if card1 not in avoid_cards and card2 not in avoid_cards and [card2, card1] not in poss_options and [card1, card2] not in poss_options:
                    poss_options.append([card1, card2])
            else:
                if suit1 == "s":
                    poss_suits_new = ["d", "h", "c"]
                elif suit1 == "d":
                    poss_suits_new = ["s", "h", "c"]
                elif suit1 == "h":
                    poss_suits_new = ["s", "d", "c"]
                else:
                    poss_suits_new = ["s", "d", "h"]
                for suit2 in poss_suits_new:
                    card2 = pair[1] + suit2
                    if card1 not in avoid_cards and card2 not in avoid_cards and [card2, card1] not in poss_options and [card1, card2] not in poss_options:
                        poss_options.append([card1, card2])
        return poss_options
    def all_Cards():
        all_cards = set()
        for val1 in {"2","3","4","5","6","7","8","9","T","J","Q","K","A"}:
            for val2 in {"s", "d", "c", "h"}:
                s = val1 + val2
                all_cards.add(s)
        return all_cards
    def all_pairs_converted():
        all_pairs_converted = set()
        rank_list = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
        for ind1 in range(len(rank_list)):
            for ind2 in range(0, ind1+1):
                for val3 in {"s", "o"}:
                    s = rank_list[ind1] + rank_list[ind2] + val3
                    if ind1 == ind2 and val3 == "o":
                        all_pairs_converted.add(s)
                    elif ind1 != ind2:
                        all_pairs_converted.add(s)
        return all_pairs_converted
        


 
