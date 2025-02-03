import pickle
from node import *
import pprint
class CFR_convert():
    iter = 14760
    with open(f'avg_strategy_{iter}.pkl', 'rb') as file:
        strategy = pickle.load(file)
    with open(f'dict_inf_{iter}.pkl', 'rb') as file:
        dict_inf = pickle.load(file)
    def thresholding(threshold):
        new_avg_strategy = {}
        for val in CFR_convert.strategy:
            new_strategy = {}
            normalizingSum = 0
            for action in val[5]:
                if CFR_convert.strategy[val][action] < threshold:
                    new_strategy[action] = 0
                else:
                    new_strategy[action] = CFR_convert.strategy[val][action]
                normalizingSum += new_strategy[action]
            for action in val[5]:
                new_strategy[action] = new_strategy[action] / normalizingSum
            new_avg_strategy[val] = new_strategy
        return new_avg_strategy
    def convert_to_last(n, strategy_dict):
        new_avg_strategy = {}
        for val in strategy_dict:
            history = val[4]
            history = history[-n:]
            new_val = (val[0], val[1], val[2], val[3], history, val[5])
            if new_val in new_avg_strategy:
                for action in new_avg_strategy[new_val]:
                    new_avg_strategy[new_val][action] = new_avg_strategy[new_val][action] + strategy_dict[val][action]
            else:
                new_avg_strategy[new_val] = {}
                for action in strategy_dict[val]:
                    new_avg_strategy[new_val][action] = strategy_dict[val][action]
        for val in new_avg_strategy:
            normalizingSum = 0
            for action in new_avg_strategy[val]:
                normalizingSum += new_avg_strategy[val][action]
            for action in new_avg_strategy[val]:
                new_avg_strategy[val][action] = new_avg_strategy[val][action]/normalizingSum
        with open(f'convert_to_last_{CFR_convert.iter}_{n}.pkl', "wb") as file:
            pickle.dump(new_avg_strategy, file)
    def convert_without_actions(n, strategy_dict):
        new_avg_strategy = {}
        for val in strategy_dict:
            history = val[4]
            history = history[-n:]
            new_val = (val[0], val[1], val[2], val[3], history)
            if new_val in new_avg_strategy:
                poss_actions = list(new_avg_strategy[new_val].keys())
                if list(val[5]) == poss_actions:
                    for action in strategy_dict[val]:
                        new_avg_strategy[new_val][action] = new_avg_strategy[new_val][action] + strategy_dict[val][action]
            else:
                new_avg_strategy[new_val] = {}
                for action in strategy_dict[val]:
                    new_avg_strategy[new_val][action] = strategy_dict[val][action]
        for val in new_avg_strategy:
            normalizingSum = 0
            for action in new_avg_strategy[val]:
                normalizingSum += new_avg_strategy[val][action]
            for action in new_avg_strategy[val]:
                new_avg_strategy[val][action] = new_avg_strategy[val][action]/normalizingSum
        with open(f'convert_to_last_{CFR_convert.iter}_{n}_without_actions.pkl', "wb") as file:
            pickle.dump(new_avg_strategy, file) 

strategy_dict = CFR_convert.thresholding(0.2)
CFR_convert.convert_to_last(3, strategy_dict)
CFR_convert.convert_to_last(1, strategy_dict)
CFR_convert.convert_without_actions(1, strategy_dict)
# with open(f'convert_to_last_{CFR_convert.iter}_1.pkl', 'rb') as file:
#     strategy = pickle.load(file)
#     for val in strategy:
#         if len(strategy[val]) > 1:
#             print(val, end = "")
#             print(str(strategy[val]))
#             print()           




    # with open(f'avg_thresholding_strategy_{590}.pkl', 'rb') as file:
    #     strategy = pickle.load(file)
    # for val in strategy:
    #     if len(strategy[val]) > 1:
    #         print(val, end = "")
    #         print(str(strategy[val]))
    #         print()
    # with open(f'avg_strategy_{iter}.pkl', 'rb') as file:
    #     strategy = pickle.load(file)
    # for val in strategy:
    #     if len(strategy[val]) > 1:
    #         print(val, end = "")
    #         print(str(strategy[val]))
    #         print()
        