import pickle
import pprint
import random
import numpy as np
import math
import eval7
from custom_types.card import *
NUM_OF_PREFLOP_CLUSTERS = 12
class New_Clusters():
    pre_flop_dict = {}
    with open('pre_flop_equity.pkl', 'rb') as file:
        pre_flop_dict = pickle.load(file)
    # for val in pre_flop_dict:
    #     print(pre_flop_dict[val][len(pre_flop_dict[val])//2])
    pre_flop_cfr = {}
    for val in pre_flop_dict:
        pre_flop_cfr[2*val] = [(val, True) for val in pre_flop_dict[val]]
        pre_flop_cfr[2*val+1] = [(val, False) for val in pre_flop_dict[val]]
    post_flop_dict = {}
    with open('post_flop_equity.pkl', 'rb') as file:
        post_flop_dict = pickle.load(file)
    post_turn_dict = {}
    with open('post_turn_equity.pkl', 'rb') as file:
        post_turn_dict = pickle.load(file)
    with open('post_river_equity.pkl', 'rb') as file:
        post_river_dict = pickle.load(file)
    def simulate_hand(my_cards, given_community, opp_range):
        new_opp_range = []
        for c in opp_range:
            new_opp_range = new_opp_range + New_Card.convert_back_avoid(c, my_cards + given_community)
        new_opp_range = ["".join(val) for val in new_opp_range]
        # print("Opponent Range: " + str(new_opp_range))
        new_opp_range = new_opp_range[::15]
        # first_3 = new_opp_range[:3]
        # last_3 = new_opp_range[-3:]
        # last_3 = [val for val in last_3 if val not in first_3]
        # new_opp_range = first_3 + last_3
        # print("New Opponent Range: " + str(new_opp_range))
        # print("Avoid Cards: " + str(my_cards + given_community))
        # print()
        new_opp_range = eval7.HandRange(",".join(new_opp_range))
        my_cards = [eval7.Card(c) for c in my_cards]
        given_community = [eval7.Card(c) for c in given_community]
        equity = eval7.py_hand_vs_range_exact(my_cards, new_opp_range, given_community)
        return equity
    def simulation(my_cards, given_community, pre_flop_clusters):
        winner = [0 for _ in range(NUM_OF_PREFLOP_CLUSTERS)]
        win = [0 for _ in range(NUM_OF_PREFLOP_CLUSTERS)]
        for i in range(NUM_OF_PREFLOP_CLUSTERS):
            opp_range_i = pre_flop_clusters[i]
            win[i] = New_Clusters.simulate_hand(my_cards, given_community, opp_range_i)
        winner = [winner[i] + win[i] for i in range(NUM_OF_PREFLOP_CLUSTERS)]
        return winner
    def calc_equity(hand):
        my_cards = [hand[:2], hand[2:4]]
        community_cards = hand[4:]
        num_community = len(community_cards)
        community_cards = [community_cards[i:i+2] for i in range(0, num_community, 2)]
        point = New_Clusters.simulation(my_cards, community_cards, New_Clusters.pre_flop_dict)
        return point
    def closest_equity(equity, dict_points):
        min_dist = 10000
        closest_clus = 0
        for val in dict_points:
            dist = math.dist(equity, dict_points[val])
            if dist < min_dist:
                min_dist = dist
                closest_clus = val
        return (closest_clus, dict_points[closest_clus], min_dist)
    def dist(equity1, equity2):
        return abs(sum(equity1) - sum(equity2))
    def closest_cluster(hand):
        dict_cen = {}
        if len(hand) == 4:
            centers = ["QQo", "88o", "44o", "AJs", "QTs", "A6s", "K2s", "94s", "93s", "AJo", "QJo", "A6o"]
            new_hand = New_Card.convert([hand[:2], hand[2:4]])
            for val in New_Clusters.pre_flop_dict:
                if new_hand in New_Clusters.pre_flop_dict[val]:
                    return "".join(New_Card.convert_back(centers[val]))
        if len(hand) == 10:
            with open('post_flop_clusters_3.pkl', 'rb') as file:
                dict_cen = pickle.load(file)
        elif len(hand) == 12:
            with open('post_flop_clusters_4.pkl', 'rb') as file:
                dict_cen = pickle.load(file)
        else:
            with open('post_flop_clusters_5.pkl', 'rb') as file:
                dict_cen = pickle.load(file)
        equity_hand = New_Clusters.calc_equity(hand)
        min_dist = 10000
        closest_clus = 0
        for val in dict_cen:
            dist = New_Clusters.dist(equity_hand, dict_cen[val])
            if dist < min_dist:
                min_dist = dist
                closest_clus = val 
        return closest_clus

