from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from g_state import *
from terminal_node import *
from node import *
import pickle
NUM_OF_ITERATIONS = 10000000000
# information set: maps converted node to node
class CFR:
    def cfr_forward(game_state, type_of_node, n, visited_nodes, dict_inf):
        visited_nodes.append((game_state, type_of_node, n))
        curr_player = game_state.player
        if len(game_state.history) == 0: # initial node
            information_set_key = Node.convert(n)
            dict_inf[information_set_key].visits = 1
            dict_inf[information_set_key].p_sum = [1, 1]
        if type_of_node == "player":
            realization_weight = n.p_sum[0] if curr_player == 0 else n.p_sum[1]
            new_s = Node.getStrategy(n, realization_weight)
            n.strategy = new_s[0]
            n.strategySum = new_s[1]
            for action in n.actions:
                new_game_state_type = G_State.update_state(game_state, action)
                new_game_state = new_game_state_type[0]
                new_type = new_game_state_type[1]
                c = Node(new_game_state, new_type)
                information_set_key = Node.convert(c)
                if information_set_key not in dict_inf:
                    dict_inf[information_set_key] = c
                dict_inf[information_set_key].visits = dict_inf[information_set_key].visits + n.visits
                dict_inf[information_set_key].p_sum[0] = dict_inf[information_set_key].p_sum[0] + (n.strategy[action] * n.p_sum[0] if n.player == 0 else n.p_sum[1])
                dict_inf[information_set_key].p_sum[1] = dict_inf[information_set_key].p_sum[1] + (n.strategy[action] * n.p_sum[1] if n.player == 1 else n.p_sum[0])
                CFR.cfr_forward(new_game_state, new_type, dict_inf[information_set_key], visited_nodes, dict_inf)
            return
        return
    def cfr_backward(visited_nodes, dict_inf):
        for val in reversed(visited_nodes):
            game_state = val[0]
            type_of_node = val[1]
            n = val[2]
            if type_of_node == "player":
                n.v = 0
                n.v_action = {}
                poss_actions = n.actions
                cfp = n.p_sum[1] if n.player == 0 else n.p_sum[0]
                for action in poss_actions:
                    new_game_state_type = G_State.update_state(game_state, action)
                    new_game_state = new_game_state_type[0]
                    new_type = new_game_state_type[1]
                    c = Node(new_game_state, new_type)
                    information_set_key = Node.convert(c)
                    c = dict_inf[information_set_key]
                    n.v_action[action] = c.v if n.player == c.player else -c.v
                    n.v = n.v + n.strategy[action] * n.v_action[action]
                for action in poss_actions: 
                    n.regret[action] = max((n.T * n.regret[action] + n.visits * cfp * (n.v_action[action] - n.v))/(n.T + n.visits),0)
                n.T = n.T + n.visits
            elif type_of_node == "terminal":
                terminal_state = Terminal_Node(game_state)
                # if len(game_state.community_cards) == 5:
                    # print("Community:" + str(game_state.community_cards))
                n.v = Terminal_Node.calc_utility(terminal_state)[n.player]
                # print("Player" + str(n.player))
                # print("History" + str(n.history))
                # print("EV: " + str(n.v))
                # print()
                # print()
            n.visits = 0
            n.p_sum = [0, 0]
    def cfr():
        with open(f"dict_inf_2200.pkl", "rb") as file:
            dict_inf = pickle.load(file)
        for iter in range(2201, NUM_OF_ITERATIONS):
            game_state_initial = G_State.initial_game_state() 
            visited_nodes = []
            type_of_node_initial = "player"
            n_initial = Node(game_state_initial, type_of_node_initial)
            information_set_key = Node.convert(n_initial)
            if information_set_key not in dict_inf:
                dict_inf[information_set_key] = n_initial
            print("forward: " + str(iter))
            CFR.cfr_forward(game_state_initial, type_of_node_initial, dict_inf[information_set_key], visited_nodes, dict_inf)
            # for val in visited_nodes:
            #     n = val[2]
            #     print(n, end = " ")
            #     print(n.visits, end = " ")
            #     print(n.T)
            # print(len(visited_nodes))
            # print(len(dict_inf))
            # print()
            # print()
            # print()
            print("backward: " + str(iter))
            CFR.cfr_backward(visited_nodes, dict_inf)
            # for val in visited_nodes:
            #     n = val[2]
            #     print(n, end = " ")
            #     print(n.visits, end = " ")
            #     print(n.T, end = " ")
            #     print(n.v)

            if iter % 10 == 0:
                avg_strategy = {}
                avg_regret = {}
                for k in dict_inf:
                    avg_strategy[k] = Node.getAverageStrategy(dict_inf[k])
                    avg_regret[k] = dict_inf[k].regret
                with open(f'avg_strategy_{iter}.pkl', "wb") as file:
                    pickle.dump(avg_strategy, file)
                with open(f'avg_regret_{iter}.pkl', "wb") as file:
                    pickle.dump(avg_regret, file)
                with open(f'dict_inf_{iter}.pkl', "wb") as file:
                    pickle.dump(dict_inf, file)
CFR.cfr()
                 





                





        





