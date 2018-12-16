import copy
import time
from Initialization import *
from Diffusion_NormalIC import *

class Evaluation():
    def __init__(self, graph_dict, seed_cost_dict, product_list, pps, whether_infect_not_only_buying):
        ### graph_dict: (dict) the graph
        ### graph_dict[node1]: (dict) the set of node1's receivers
        ### graph_dict[node1][node2]: (float2) the weight one the edge of node1 to node2
        ### seed_cost_dict: (dict) the set of cost for seeds
        ### seed_cost_dict[i]: (dict) the degree of i's seed
        ### product_list: (list) the set to record products
        ### product_list[k]: (list) [k's profit, k's cost, k's price]
        ### product_list[k][]: (float2)
        ### num_node: (int) the number of nodes
        ### num_product: (int) the kinds of products
        ### diffusion_threshold: (float2) the threshold to judge whether diffusion continues
        ### pps: (int) the strategy to upadate personal prob.
        ### whether_infect_not_only_buying: (bool) if infect when only after buying, then False
        self.graph_dict = graph_dict
        self.seed_cost_dict = seed_cost_dict
        self.product_list = product_list
        self.num_node = len(seed_cost_dict)
        self.num_product = len(product_list)
        self.diffusion_threshold = 0.01
        self.pps = pps
        self.winob = whether_infect_not_only_buying

    def getSeedProfit(self, s_set, cur_w_list, pp_list):
        a_n_set = copy.deepcopy(s_set)
        seed_set, try_a_n_list = [], []
        pro_k_list = [0.0 for _ in range(self.num_product)]
        cur_profit = 0.0
        for k in range(self.num_product):
            for i in s_set[k]:
                seed_set.append([k, i, 1.0])

        # -- insert the children of seeds into try_a_n_set --
        while len(seed_set) > 0:
            seed = seed_set.pop()
            k_prod, i_node, prob = seed[0], seed[1], seed[2]
            outdict = self.graph_dict[i_node]
            for out in outdict:
                if not (float(outdict[out]) >= self.diffusion_threshold):
                    continue
                if not (out not in a_n_set[k_prod]):
                    continue
                if not (cur_w_list[int(out)] > self.product_list[k_prod][2]):
                    continue
                if not (pp_list[k_prod][int(out)] > 0):
                    continue
                # --- product, node, edge weight ---
                try_a_n_list.append([k_prod, out, float(outdict[out])])

        dnic = D_NormalIC(self.graph_dict, self.seed_cost_dict, self.product_list, self.pps, self.winob)
        # -- activate the nodes --
        while len(try_a_n_list) > 0:
            ### try_node: (list) the nodes may be activated for k-products
            try_node = try_a_n_list.pop()
            k_prod, i_node, prob = try_node[0], try_node[1], try_node[2]
            prodk = self.product_list[k_prod]
            if random.random() <= prob * pp_list[k_prod][int(i_node)]:
                a_n_set[k_prod].add(i_node)
                cur_profit += prodk[0]
                pro_k_list[k_prod] += prodk[0]
                cur_w_list[int(i_node)] -= prodk[2]
                pp_list = dnic.updatePersonalProbList(k_prod, i_node, cur_w_list, pp_list)

                if i_node not in self.graph_dict:
                    continue

                outdictw = self.graph_dict[i_node]
                for outw in outdictw:
                    if not (prob * float(outdictw[outw]) >= self.diffusion_threshold):
                        continue
                    if not (outw not in a_n_set[k_prod]):
                        continue
                    if not (cur_w_list[int(outw)] > prodk[2]):
                        continue
                    if not (pp_list[k_prod][int(outw)] > 0):
                        continue
                    try_a_n_list.append([k_prod, outw, prob * float(outdictw[outw]), pp_list[k_prod][int(outw)]])

        an_num_list = [0 for _ in range(self.num_product)]
        for k in range(self.num_product):
            an_num_list[k] += len(a_n_set[k])

        return cur_profit, pro_k_list, an_num_list

if __name__ == "__main__":
    data_name = "email"
    product_name = "item_r1p3n1"
    pp_strategy = 2
    whether_infect_not_only_buying = bool(0)

    iniG = IniGraph(data_name)
    iniP = IniProduct()

    graph_dict = iniG.constructGraphDict()
    seed_cost_dict = iniG.constructSeedCostDict()
    wallet_list = iniG.getWalletList(product_name)
    product_list, sum_price = iniP.getProductlist(product_name)
    num_node = len(seed_cost_dict)
    num_product = len(product_list)

    start_time = time.time()

    eva = Evaluation(graph_dict, seed_cost_dict, product_list, pp_strategy, whether_infect_not_only_buying)

    seed_set = [set(), {'732'}, {'52', '203'}]
    current_wallet_list = copy.deepcopy(wallet_list)
    personal_prob_list = [[1.0 for _ in range(num_node)] for _ in range(num_product)]

    profit, pro_k_list, an_num_list = eva.getSeedProfit(seed_set, current_wallet_list, personal_prob_list)
    print(round(profit, 2))
    print(pro_k_list)
    print(an_num_list)

    how_long = round(time.time() - start_time, 4)
    print("total time: " + str(how_long) + "sec")