import random

class D_NormalIC():
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

    def insertSeedIntoSeedSet(self, k_prod, i_node, s_set, a_n_set, cur_w_list, pp_list):
        # -- add the seed with maximum expected profit into seed set --
        s_set[k_prod].add(i_node)
        a_n_set[k_prod].add(i_node)
        for k in range(self.num_product):
            pp_list[k][int(i_node)] = 0
        # print("into seedset: " + str(mep[2]))
        prodk = self.product_list[k]
        ppk = pp_list[k_prod]
        cur_profit = prodk[0]
        cur_budget = self.seed_cost_dict[i_node]
        cur_w_list[int(i_node)] = 0

        ### try_a_n_list: (list) the set to store the nodes may be activated for some products
        ### try_a_n_list[][0]: (str) the receiver when seed is ancestor
        ### try_a_n_list[][1]: (float4) the probability to activate the receiver from seed
        try_a_n_list = []
        # -- add the receivers of seed into try_a_n_list --
        # -- notice: prevent the seed from owing no receiver --
        if i_node not in self.graph_dict:
            return s_set, a_n_set, cur_profit, cur_budget, cur_w_list, pp_list

        outdict = self.graph_dict[i_node]
        for out in outdict:
            if not (float(outdict[out]) >= self.diffusion_threshold):
                continue
            if not (out not in a_n_set):
                continue
            if not (cur_w_list[int(out)] > prodk[2]):
                continue
            if not (ppk[int(out)] > 0):
                continue
            # --- node, edge weight, personal prob. ---
            try_a_n_list.append([out, float(outdict[out]), ppk[int(out)]])

        # -- activate the candidate nodes actually --
        dnic = D_NormalIC(self.graph_dict, self.seed_cost_dict, self.product_list, self.total_budget, self.pps, self.winob)

        while len(try_a_n_list) > 0:
            ### try_node: (list) the nodes may be activated for k-products
            try_node = try_a_n_list.pop()
            if random.random() <= try_node[1] * try_node[2]:
                a_n_set[k_prod].add(try_node[0])
                cur_profit += prodk[0]
                cur_w_list[int(try_node[0])] -= prodk[2]
                pp_list = dnic.updatePersonalProbList(k_prod, try_node[0], cur_w_list, pp_list)

                if try_node[0] not in self.graph_dict:
                    continue

                outdictw = self.graph_dict[try_node[0]]
                for outw in outdictw:
                    if not (try_node[1] * float(outdictw[outw]) >= self.diffusion_threshold):
                        continue
                    if not (outw not in a_n_set[k_prod]):
                        continue
                    if not (cur_w_list[int(outw)] > prodk[2]):
                        continue
                    if not (ppk[int(outw)] > 0):
                        continue
                    try_a_n_list.append([outw, try_node[1] * float(outdictw[outw]), ppk[int(outw)]])
        return s_set, a_n_set, cur_profit, cur_budget, cur_w_list, pp_list

    def updatePersonalProbList(self, k_prod, i_node, cur_w_list, pp_list):
        prodprice = self.product_list[k_prod][2]
        if self.pps == -1:
            # -- buying products are independent --
            pp_list[k_prod][int(i_node)] = 0
        elif self.pps == 0:
            # -- a node can only buy a product --
            for k in range(self.num_product):
                pp_list[k][int(i_node)] = 0
        elif self.pps == 1:
            # -- after buying a product, the prob. to buy another product will decrease randomly --
            for k in range(self.num_product):
                if k == k_prod:
                    pp_list[k][int(i_node)] = 0
                else:
                    pp_list[k][int(i_node)] = round(random.uniform(0, pp_list[k][int(i_node)]), 4)
        elif self.pps == 2:
            # -- choose as expensive as possible --
            for k in range(self.num_product):
                if k == k_prod or cur_w_list[int(i_node)] == 0:
                    pp_list[k][int(i_node)] = 0
                else:
                    pp_list[k][int(i_node)] = max(round((prodprice / cur_w_list[int(i_node)]), 4), 0)
        elif self.pps == 3:
            # -- choose as cheap as possible --
            for k in range(self.num_product):
                if k == k_prod or cur_w_list[int(i_node)] == 0:
                    pp_list[k][int(i_node)] = 0
                else:
                    pp_list[k][int(i_node)] = min(round(1 - (prodprice / cur_w_list[int(i_node)]), 4), 0)

        minprice = 1.0
        for k in range(self.num_product):
            minprice = min(minprice, self.product_list[k][2])
        for i in range(self.num_node):
            if cur_w_list[i] < minprice:
                for k in range(self.num_product):
                    pp_list[k][i] = 0.0
        return pp_list