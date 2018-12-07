import time
import copy
from Initialization import *
from Diffusion_NormalIC import *

def sortSecond(val):
    return val[1]
def sortThird(val):
    return val[2]

class SeedSelection_HD():
    def __init__(self, graph_dict, seed_cost_dict, product_list, total_budget, pps, whether_infect_not_only_buying):
        ### graph_dict: (dict) the graph
        ### graph_dict[node1]: (dict) the set of node1's receivers
        ### graph_dict[node1][node2]: (float2) the weight one the edge of node1 to node2
        ### seed_cost_dict: (dict) the set of cost for seeds
        ### seed_cost_dict[i]: (dict) the degree of i's seed
        ### product_list: (list) the set to record products
        ### product_list[k]: (list) [k's profit, k's cost, k's price]
        ### product_list[k][]: (float2)
        ### total_ budget: (int) the budget to select seed
        ### num_node: (int) the number of nodes
        ### num_product: (int) the kinds of products
        ### diffusion_threshold: (float2) the threshold to judge whether diffusion continues
        ### pps: (int) the strategy to upadate personal prob.
        ### whether_infect_not_only_buying: (bool) if infect when only after buying, then False
        self.graph_dict = graph_dict
        self.seed_cost_dict = seed_cost_dict
        self.product_list = product_list
        self.total_budget = total_budget
        self.num_node = len(seed_cost_dict)
        self.num_product = len(product_list)
        self.diffusion_threshold = 0.01
        self.pps = pps
        self.winob = whether_infect_not_only_buying

    def constructDegreeDict(self, dataname):
        with open(IniGraph(dataname).data_degree_path) as f:
            degree_list = []
            for line in f:
                (node, degree) = line.split()
                degree_list.append([node, degree])
            degree_list.sort(key=sortSecond, reverse=True)
            degreedict = {}
            for i_node, i_deg in degree_list:
                if i_deg in degreedict:
                    degreedict[i_deg].add(i_node)
                else:
                    degreedict[i_deg] = {i_node}
        return degreedict

    def getHighDegreeSet(self, d_dict):
        while d_dict[max(d_dict)] == set():
            if d_dict[max(d_dict)] == set():
                del d_dict[max(d_dict)]
            if d_dict == set():
                return {}
        return d_dict[max(d_dict)]

    def getSeedExpectProfit(self, k_prod, i_node, a_n_set_k, cur_w_list, pp_list_k):
        # -- calculate the expected profit for single node when it's chosen as a seed --
        ### temp_a_n_set: (set) the union set of activated node set and temporary activated nodes when nnode is a new seed
        ### try_a_n_list: (list) the set to store the nodes may be activated for k-products
        ### try_a_n_list[][0]: (str) the receiver when i is ancestor
        ### try_a_n_list[][1]: (float4) the probability to activate the receiver from i
        ### try_a_n_list[][2]: (float2) the personal probability to activate ownself
        ### ep: (float2) the expected profit
        temp_a_n_set = {i_node}
        try_a_n_list = []
        ep = -1 * self.seed_cost_dict[i_node]

        prodk = self.product_list[k_prod]

        # -- add the receivers of nnode into try_a_n_list --
        # -- notice: prevent the node from owing no receiver --
        if i_node not in self.graph_dict:
            return 0

        outdict = self.graph_dict[i_node]
        for out in outdict:
            if not (float(outdict[out]) >= self.diffusion_threshold):
                continue
            if not (out not in a_n_set_k):
                continue
            if not (cur_w_list[int(out)] > prodk[2]):
                continue
            if not (pp_list_k[int(out)] > 0):
                continue
            # -- add the value calculated by activated probability * profit of this product --
            ep += float(outdict[out]) * pp_list_k[int(out)] * prodk[0]
            # -- activate the receivers temporally --
            # -- add the receiver of node into try_a_n_list --
            # -- notice: prevent the node from owing no receiver --
            temp_a_n_set.add(out)
            # --- node, edge weight, personal prob. ---
            try_a_n_list.append([out,  float(outdict[out])])

        while len(try_a_n_list) > 0:

            ### try_node: (list) the nodes may be activated for k-products
            try_node = try_a_n_list.pop()
            if try_node[0] not in self.graph_dict:
                continue
            outdictw = self.graph_dict[try_node[0]]
            for outw in outdictw:
                if not (try_node[1] * float(outdictw[outw]) >= self.diffusion_threshold):
                    continue
                if not (outw not in a_n_set_k):
                    continue
                if not (outw not in temp_a_n_set):
                    continue
                if not (cur_w_list[int(outw)] > prodk[2]):
                    continue
                if not (pp_list_k[int(outw)] > 0):
                    continue
                # -- add the value calculated by activated probability * profit of this product --
                ep += try_node[1] * float(outdictw[outw]) * pp_list_k[int(outw)] * prodk[0]
                # -- activate the receivers temporally --
                # -- add the receiver of node into try_a_n_list --
                # -- notice: prevent the node from owing no receiver --
                temp_a_n_set.add(outw)
                try_a_n_list.append([outw, round(try_node[1] * float(outdictw[outw]), 4)])

        return round(ep, 4)

    def calHighDegreeSeedProfit(self, hd_set, b_set, cur_budget, a_n_set, cur_w_list, pp_list):
        # -- calculate expected profit for all combinations of nodes and products --
        ### expect_profit_list: (list) the list of expected profit for all combinations of nodes and products
        ### expect_profit_list[k]: (list) the list of expected profit for k-product
        ### expect_profit_list[k][i]: (float4) the expected profit for i-node for k-product
        ep_list = [[] for _ in range(self.num_product)]

        sshd = SeedSelection_HD(self.graph_dict, self.seed_cost_dict, self.product_list, self.total_budget, self.pps, self.winob)
        for k in range(self.num_product):
            ep_listk = ep_list[k]
            for i in hd_set:
                ep = sshd.getSeedExpectProfit(k, i, a_n_set[k], cur_w_list, pp_list[k])
                # -- the cost of seed cannot exceed the budget --
                if self.seed_cost_dict[i] + cur_budget > self.total_budget:
                    b_set[k].add(i)
                    continue

                # -- the expected profit cannot be negative --
                if ep <= 0:
                    b_set[k].add(i)
                    continue

                ep_listk.append([i, ep])

        nhd_set = set()
        for i in hd_set:
            bk = 0
            for k in range(self.num_product):
                if i in b_set[k]:
                    bk += 1
            if bk == self.num_product:
                nhd_set.add(i)

        for i in nhd_set:
            hd_set.remove(i)

        return ep_list, hd_set, b_set

    def getMostValuableSeed(self, ep_list):
        # -- find the seed with maximum expected profit from all combinations of nodes and products --
        ### mep: (list) the current maximum expected profit: [expected profit, which product, which node]
        mep = [0.0, 0, '-1']

        for k in range(self.num_product):
            ep_listk = ep_list[k]
            for i, ep in ep_listk:
                # -- choose the better seed --
                if ep > mep[0]:
                    mep = [ep, k, i]

        return mep[1], mep[2]

if __name__ == "__main__":
    ### whether_infect_not_only_buying: (bool) if infect when only after buying, then False
    data_name = "email"
    product_name = "item_r1p3n1"
    total_budget = 1
    execution_times = 2
    pp_strategy = 2
    whether_infect_not_only_buying = bool(0)

    iniG = IniGraph(data_name)
    iniP = IniProduct()

    graph_dict = iniG.constructGraphDict()
    seed_cost_dict = iniG.constructSeedCostDict()
    ### wallet_list: (list) the list of node's personal budget (wallet)
    ### wallet_list[i]: (float2) the i's wallet
    wallet_list = iniG.getWalletList(product_name)
    ### product_list: (list) [profit, cost, price]
    product_list, sum_price = iniP.getProductlist(product_name)
    num_node = len(seed_cost_dict)
    num_product = len(product_list)

    start_time = time.time()

    # -- initialization for each budget --
    ### result: (list) [profit, budget, seed number per product, customer number per product, seed set] in this execution_time
    result = []
    ### avg_profit, avg_budget: (float) the average profit and budget per execution_time
    ### avg_num_k_seed: (list) the list to record the average number of seed for products per execution_time
    ### avg_num_k_seed[k]: (int) the average number of seed for k-product per execution_time
    ### avg_num_k_an: (list) the list to record the average number of activated node for products per execution_time
    ### avg_num_k_an[k]: (int) the average number of activated node for k-product per execution_time
    avg_profit, avg_budget = 0.0, 0.0
    avg_num_k_seed, avg_num_k_an = [0 for _ in range(num_product)], [0 for _ in range(num_product)]
    ### pro_k_list, bud_k_list: (list) the list to record profit and budget for products
    ### pro_k_list[k], bud_k_list[k]: (float) the list to record profit and budget for k-product
    pro_k_list, bud_k_list = [0.0 for _ in range(num_product)], [0.0 for _ in range(num_product)]

    sshd = SeedSelection_HD(graph_dict, seed_cost_dict, product_list, total_budget, pp_strategy, whether_infect_not_only_buying)
    dnic = D_NormalIC(graph_dict, seed_cost_dict, product_list, total_budget, pp_strategy, whether_infect_not_only_buying)
    degree_dict = sshd.constructDegreeDict(data_name)
    high_degree_set_o = sshd.getHighDegreeSet(degree_dict)

    # -- initialization for each execution_times --
    ### now_profit, now_budget: (float) the profit and budget in this execution_time
    now_profit, now_budget = 0.0, 0.0
    ### seed_set: (list) the seed set
    ### seed_set[k]: (set) the seed set for k-product
    ### activated_node_set: (list) the activated node set
    ### activated_node_set[k]: (set) the activated node set for k-product
    ### ban_set: (list) the set to record the node that will be banned
    ### ban_set[k]: (set) the set to record the node that will be banned for k-product
    seed_set, activated_node_set, ban_set = [set() for _ in range(num_product)], [set() for _ in range(num_product)], [set() for _ in range(num_product)]
    ### personal_prob_list: (list) the list of personal prob. for all combinations of nodes and products
    ### personal_prob_list[k]: (list) the list of personal prob. for k-product
    ### personal_prob_list[k][i]: (float2) the personal prob. for i-node for k-product
    personal_prob_list = [[1.0 for _ in range(num_node)] for _ in range(num_product)]
    current_wallet_list = copy.deepcopy(wallet_list)
    high_degree_set = copy.deepcopy(high_degree_set_o)

    # print("getMostValuableSeed")
    expect_profit_list, high_degree_set, ban_set = sshd.calHighDegreeSeedProfit(high_degree_set, ban_set, now_budget, activated_node_set, current_wallet_list, personal_prob_list)
    mep_k_prod, mep_i_node = sshd.getMostValuableSeed(expect_profit_list)

    # -- main --
    while now_budget < total_budget and mep_i_node != '-1':
        # print("addSeedIntoSeedSet")
        high_degree_set.remove(mep_i_node)
        seed_set, activated_node_set, current_k_profit, current_k_budget, current_wallet_list, personal_prob_list = \
            dnic.insertSeedIntoSeedSet(mep_k_prod, mep_i_node, seed_set, activated_node_set, current_wallet_list, personal_prob_list)
        pro_k_list[mep_k_prod] += round(current_k_profit, 4)
        bud_k_list[mep_k_prod] += round(current_k_budget, 4)
        now_profit += current_k_profit
        now_budget += current_k_budget
        if len(high_degree_set) == 0:
            high_degree_set = sshd.getHighDegreeSet(degree_dict)
        expect_profit_list, high_degree_set, ban_set = sshd.calHighDegreeSeedProfit(high_degree_set, ban_set, now_budget, activated_node_set, current_wallet_list, personal_prob_list)
        mep_k_prod, mep_i_node = sshd.getMostValuableSeed(expect_profit_list)

    # print("result")
    now_num_k_seed, now_num_k_an = [len(k) for k in seed_set], [len(k) for k in activated_node_set]
    result.append([round(now_profit, 4), round(now_budget, 4), now_num_k_seed, now_num_k_an, seed_set])
    avg_profit += now_profit
    avg_budget += now_budget
    for k in range(num_product):
        avg_num_k_seed[k] += now_num_k_seed[k]
        avg_num_k_an[k] += now_num_k_an[k]
    how_long = round(time.time() - start_time, 4)
    print(result)
    print(round(avg_profit, 4), round(avg_budget, 4))
    print("total time: " + str(how_long) + "sec")