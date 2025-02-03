import pickle
from custom_types.card import *
class CFR_test():
    iter = 11400
    # new_cfr = {}
    with open(f'avg_strategy_{iter}.pkl', 'rb') as file:
        strategy = pickle.load(file)
        for val in strategy:
            print(str(val), end = "")
            print(str(strategy[val]))
            print()
    # print(len(strategy))
# print(list(New_Card.all_Cards()))

    # with open(f'avg_regret_{iter}.pkl', 'rb') as file:
    #     first_regret = pickle.load(file)
    # for val in first_regret:
    #     if len(first_regret[val]) > 1:
    #         print(str(val), end = "")
    #         print(str(first_regret[val]))
    #         print()
    # with open(f'dict_inf_{iter}.pkl', 'rb') as file:
    #     first_dict = pickle.load(file)
    #     set_val = set()
    # for val in first_dict:
    #     val_tuple = first_dict[val]
    #     if len(val_tuple.community_cards) == 5:
    #         set_val.add((val_tuple.player, tuple(val_tuple.hand + val_tuple.community_cards), tuple(val_tuple.bounty)))
    # print(len(set_val))
    # with open(f'dict_inf_{10}.pkl', 'rb') as file:
    #     second_dict = pickle.load(file)
    # with open(f'dict_inf_{20}.pkl', 'rb') as file:
    #     third_dict = pickle.load(file)
    # with open(f'dict_inf_{30}.pkl', 'rb') as file:
    #     fourth_dict = pickle.load(file)
    # with open(f'dict_inf_{180}.pkl', 'rb') as file:
    #     fourth_dict = pickle.load(file)
    # with open(f'dict_inf_{190}.pkl', 'rb') as file:
    #     fifth_dict = pickle.load(file)
    # with open(f'dict_inf_{230}.pkl', 'rb') as file:
    #     sixth_dict = pickle.load(file)
    # print(len(first_dict))
    # print(len(second_dict))
    # print(len(third_dict))
    # print(len(fourth_dict))
    # print(len(fifth_dict))
    # print(len(sixth_dict))
    