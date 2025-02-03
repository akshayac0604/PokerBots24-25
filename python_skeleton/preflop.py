import eval7
from custom_types.card import *
import random
import pickle
class MonteCarlo_Preflop():
    def main():
        all_cards = New_Card.all_pairs_converted()
        pre_flop_clusters = {}
        pre_flop_clusters[0] = ["AAo", "KKo", "QQo", "JJo", "TTo"]
        pre_flop_clusters[1] = ["99o", "88o", "77o"]
        pre_flop_clusters[2] = ["66o", "55o", "44o", "33o", "22o"]
        pre_flop_clusters[3] = ["AKs", "AQs", "AJs", "ATs", "KQs", "KJs"]
        pre_flop_clusters[4] = ["KTs", "QJs", "QTs", "JTs"]
        pre_flop_clusters[5] = ["A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s"]
        pre_flop_clusters[6] = [a + str(b) + "s" for a in {"K", "Q"} for b in range(2,10)]
        pre_flop_clusters[7] = ["T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "98s", "97s", "96s", "95s", "94s", "87s", "86s", "85s", "84s", "76s", "75s", "74s", "65s", "64s", "J9s"]
        pre_flop_clusters[8] = [val for val in all_cards if val[2] == "s" and val not in pre_flop_clusters[3] + pre_flop_clusters[4] + pre_flop_clusters[5] + pre_flop_clusters[6] + pre_flop_clusters[7]]
        pre_flop_clusters[9] = ["AKo", "AQo", "AJo", "KQo"]
        pre_flop_clusters[10] = ["ATo", "KJo", "KTo", "QJo", "QTo", "JTo"]
        pre_flop_clusters[11] = [val for val in all_cards if val[2] == "o" and val not in pre_flop_clusters[0] + pre_flop_clusters[1] + pre_flop_clusters[2] +  pre_flop_clusters[9] + pre_flop_clusters[10]]
        with open('pre_flop_equity.pkl', 'wb') as file:
            pickle.dump(pre_flop_clusters, file)
MonteCarlo_Preflop.main()




    


        
