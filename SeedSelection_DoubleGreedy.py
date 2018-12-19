from SeedSelection_NaiveGreedy import *

class SeedSelection_DG():
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

    def getCandidateSeedSet(self, k_prod, seed_set, nban_set, cur_w_list, pp_list):
        # -- get the candidate seed set for k-product --
        ### ban_set: (set) record the impossible seeds
        ### s_set: (set) the S set for all products
        ### nb_set: (set) the T set for all products
        ### mep_k: (list) the current maximum expected profit: [expected profit, which product, which node]
        ban_set = set()
        s_set = copy.copy(seed_set)
        nb_set = copy.copy(nban_set)
        mep_k = [0.0, k_prod, '-1']
        eva = Evaluation(self.graph_dict, self.seed_cost_dict, self.product_list, self.pps, self.winob)

        ### s_cost: (float) the cost of S set
        ### s_profit: (float) the profit of S set
        s_cost = 0.0
        for i in s_set[k_prod]:
            s_cost += self.seed_cost_dict[i]
        s_profit = eva.getSeedProfit(s_set, cur_w_list, pp_list)[0]
        s_profit = s_profit - s_cost

        ### nb_cost: (float) the cost of T set
        ### nb_profit: (float) the profit of T set
        # -- set the nb_set, nb_cur_w_list, nb_pp_list for T set --
        for k in range(self.num_product):
            if k != k_prod:
                nb_set[k] = set()
        nb_cost = 0.0
        nb_cur_w_list = copy.deepcopy(cur_w_list)
        nb_pp_list = copy.deepcopy(pp_list)
        for i in nb_set[k_prod]:
            nb_cost += self.seed_cost_dict[i]
            nb_cur_w_list[int(i)] = 0
            nb_pp_list[k_prod][int(i)] = 0
        nb_profit = eva.getSeedProfit(nb_set, nb_cur_w_list, nb_pp_list)[0]
        nb_profit = nb_profit - nb_cost

        # -- select the possible seeds --
        possible_seed_set = nb_set[k_prod].difference(seed_set[k_prod])
        for i in possible_seed_set:
            # -- calculate the marginal profit for inserting i into S set --
            ### s_plus_set: (set) the S set inserting i for all products
            ### s_plus_cost: (float) the cost of S set inserting i
            ### s_plus_profit: (float) the profit of S set inserting i
            ### marginal_s: (float) tht marginal profit for inserting i into S set
            s_plus_set = copy.deepcopy(s_set)
            s_plus_set[k_prod].add(i)
            s_plus_cost = s_cost + self.seed_cost_dict[i]
            cur_w_list_plus = copy.deepcopy(cur_w_list)
            cur_w_list_plus[int(i)] = 0
            pp_list_plus = copy.deepcopy(pp_list)
            pp_list_plus[k_prod][int(i)] = 0
            s_plus_profit = eva.getSeedProfit(s_plus_set, cur_w_list_plus, pp_list_plus)[0]
            s_plus_profit = s_plus_profit - s_plus_cost
            marginal_s = s_plus_profit - s_profit

            # -- calculate the marginal profit for removing i from T set --
            ### nb_minus_set: (set) the T set removing i for all products
            ### s_plus_cost: (float) the cost of T set removing i
            ### s_plus_profit: (float) the profit of T set removing i
            ### marginal_nb: (float) tht marginal profit for removing i from T set
            nb_minus_set = copy.deepcopy(nb_set)
            nb_minus_set[k_prod].remove(i)
            nb_minus_cost = nb_cost - self.seed_cost_dict[i]
            cur_w_list_minus = copy.deepcopy(cur_w_list)
            pp_list_minus = copy.deepcopy(pp_list)
            for ii in nb_minus_set[k_prod]:
                cur_w_list_minus[int(ii)] = 0
                pp_list_minus[k_prod][int(ii)] = 0
            nb_minus_profit = eva.getSeedProfit(nb_minus_set, cur_w_list_minus, pp_list_minus)[0]
            nb_minus_profit = nb_minus_profit - nb_minus_cost
            marginal_nb = nb_minus_profit - nb_profit

            if marginal_s < marginal_nb:
                ban_set.add(i)
                continue
            if marginal_s >= mep_k[0]:
                mep_k = [marginal_s, k_prod, i]

        for i in ban_set:
            nb_set[k_prod].remove(i)
        nban_set[k_prod] = nb_set[k_prod]

        return nban_set, mep_k

if __name__ == "__main__":
    data_name = "email"
    product_name = "item_r1p3n1"
    total_budget = 1
    execution_times = 10
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

    # -- initialization for each budget --
    result = []
    avg_profit, avg_budget = 0.0, 0.0
    avg_num_k_seed, avg_num_k_an = [0 for _ in range(num_product)], [0 for _ in range(num_product)]
    pro_k_list, bud_k_list = [0.0 for _ in range(num_product)], [0.0 for _ in range(num_product)]

    ssdg = SeedSelection_DG(graph_dict, seed_cost_dict, product_list, total_budget, pp_strategy, whether_infect_not_only_buying)
    eva = Evaluation(graph_dict, seed_cost_dict, product_list, pp_strategy, whether_infect_not_only_buying)

    # -- initialization for each sample_number --
    now_budget = 0.0
    seed_set, activated_node_set = [set() for _ in range(num_product)], [set() for _ in range(num_product)]
    personal_prob_list = [[1.0 for _ in range(num_node)] for _ in range(num_product)]
    current_wallet_list = copy.deepcopy(wallet_list)
    notban_set = [set(graph_dict.keys()) for _ in range(num_product)]

    # print("getCandidateSeedSet")
    mep = [0.0, 0, '-1']
    for k in range(num_product):
        notban_set, mep_k = ssdg.getCandidateSeedSet(k, seed_set, notban_set, current_wallet_list, personal_prob_list)
        if mep_k[0] >= mep[0]:
            mep = mep_k

    # -- main --
    while now_budget < total_budget and mep[2] != '-1':
        # print("insertSeedIntoSeedSet")
        seed_set[mep[1]].add(mep[2])
        bud_k_list[mep[1]] += round(seed_cost_dict[mep[2]], 4)
        now_budget += seed_cost_dict[mep[2]]
        ban_set = [set() for _ in range(num_product)]
        for k in range(num_product):
            for i in notban_set[k]:
                if now_budget + seed_cost_dict[i] > total_budget:
                    ban_set[k].add(i)

        for k in range(num_product):
            for i in ban_set[k]:
                notban_set[k].remove(i)
        # print("getCandidateSeedSet")
        mep = [0.0, 0, '-1']
        for k in range(num_product):
            notban_set, mep_k = ssdg.getCandidateSeedSet(k, seed_set, notban_set, current_wallet_list, personal_prob_list)
            if mep_k[0] >= mep[0]:
                mep = mep_k
        print(now_budget)

    # print("result")
    now_profit, now_pro_k_list, now_num_k_an = eva.getSeedProfit(seed_set, wallet_list, [[1.0 for _ in range(num_node)] for _ in range(num_product)])

    now_num_k_seed = [len(k) for k in seed_set]
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