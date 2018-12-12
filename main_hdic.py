from SeedSelection_HighDegree import *

if __name__ == "__main__":
    for pp_strategy in range(1, 2):
        data_name, product_name = "", ""
        for setting in range(1, 2):
            # print("setting = " + str(setting))
            if setting == 1:
                data_name = "email"
                product_name = "item_r1p3n1"
            elif setting == 2:
                data_name = "email"
                product_name = "item_r1p3n2"
            elif setting == 3:
                data_name = "email"
                product_name = "item_r1p3n1_a"
            elif setting == 4:
                data_name = "email"
                product_name = "item_r1p3n2_a"
            total_budget = 1
            execution_times, etimes = 2, 1

            iniG = IniGraph(data_name)
            iniP = IniProduct()

            graph_dict = iniG.constructGraphDict()
            seed_cost_dict = iniG.constructSeedCostDict()
            wallet_list = iniG.getWalletList(product_name)
            product_list, sum_price = iniP.getProductlist(product_name)
            num_node = len(seed_cost_dict)
            num_product = len(product_list)

            for winob in range(1):
                # print("winob = " + str(winob))
                whether_infect_not_only_buying = bool(winob)

                result_numseed_list = [[0 for _ in range(num_product)] for _ in range(int(execution_times / etimes))]
                result_numan_list = [[0 for _ in range(num_product)] for _ in range(int(execution_times / etimes))]
                for bud in range(1, total_budget + 1):
                    # print("bud = " + str(bud))
                    start_time = time.time()
                    result = []
                    avg_profit, avg_budget = 0.0, 0.0
                    pro_k_list, bud_k_list = [0.0 for _ in range(num_product)], [0.0 for _ in range(num_product)]
                    avg_num_k_seed, avg_num_k_an = [0 for _ in range(num_product)], [0 for _ in range(num_product)]
                    mrss_times, mrss_pro, mrss_set = [], [], []
                    mrss = [0, 0.0, ""]

                    sshd = SeedSelection_HD(graph_dict, seed_cost_dict, product_list, bud, pp_strategy, whether_infect_not_only_buying)
                    dnic = D_NormalIC(graph_dict, seed_cost_dict, product_list, bud, pp_strategy, whether_infect_not_only_buying)
                    degree_dict_o = sshd.constructDegreeDict(data_name)

                    for times in range(execution_times):
                        # print("times = " + str(times))
                        print("budget = " + str(bud) + ", iteration = " + str(times) + ", pp_strategy = " + str(pp_strategy) +
                              ", whether_infect_not_only_buying = " + str(whether_infect_not_only_buying))
                        now_profit, now_budget = 0.0, 0.0
                        seed_set, activated_node_set, ban_set = [set() for _ in range(num_product)], [set() for _ in range(num_product)], [set() for _ in range(num_product)]
                        personal_prob_list = [[1.0 for _ in range(num_node)] for _ in range(num_product)]
                        current_wallet_list = copy.deepcopy(wallet_list)

                        degree_dict = copy.deepcopy(degree_dict_o)
                        # print("getHighDegreeSet")
                        high_degree_set = sshd.getHighDegreeSet(degree_dict)
                        # print("calHighDegreeSeedProfit")
                        expect_profit_list, high_degree_set, ban_set = sshd.calHighDegreeSeedProfit(high_degree_set, ban_set, now_budget, activated_node_set, current_wallet_list, personal_prob_list)
                        # print("getMostValuableSeed")
                        mep_k_prod, mep_i_node = sshd.getMostValuableSeed(expect_profit_list)

                        # -- main --
                        while now_budget < bud and mep_i_node != '-1':
                            # print("insertSeedIntoSeedSet")
                            high_degree_set.remove(mep_i_node)
                            seed_set, activated_node_set, current_k_profit, current_k_budget, current_wallet_list, personal_prob_list = \
                                dnic.insertSeedIntoSeedSet(mep_k_prod, mep_i_node, seed_set, activated_node_set, current_wallet_list, personal_prob_list)
                            pro_k_list[mep_k_prod] += round(current_k_profit, 4)
                            bud_k_list[mep_k_prod] += round(current_k_budget, 4)
                            now_profit += current_k_profit
                            now_budget += current_k_budget
                            if len(high_degree_set) == 0:
                                high_degree_set = sshd.getHighDegreeSet(degree_dict)
                            # print("calHighDegreeSeedProfit")
                            expect_profit_list, high_degree_set, ban_set = sshd.calHighDegreeSeedProfit(high_degree_set, ban_set, now_budget, activated_node_set, current_wallet_list, personal_prob_list)
                            # print("getMostValuableSeed")
                            mep_k_prod, mep_i_node = sshd.getMostValuableSeed(expect_profit_list)

                        # print("result")
                        now_num_k_seed, now_num_k_an = [len(k) for k in seed_set], [len(k) for k in activated_node_set]
                        result.append([round(now_profit, 4), round(now_budget, 4), now_num_k_seed, now_num_k_an, seed_set])
                        avg_profit += now_profit
                        avg_budget += now_budget
                        for k in range(num_product):
                            avg_num_k_seed[k] += now_num_k_seed[k]
                            avg_num_k_an[k] += now_num_k_an[k]

                        if seed_set not in mrss_set:
                            mrss_times.append(1)
                            mrss_pro.append(now_profit)
                            mrss_set.append(seed_set)
                        else:
                            i = mrss_set.index(seed_set)
                            mrss_times[i] += 1
                            mrss_pro[i] += now_profit
                        i = mrss_set.index(seed_set)
                        if (mrss_times[i] > mrss[0]) or (
                                (mrss_times[i] == mrss[0]) and (mrss_pro[i] / mrss_times[i]) > (mrss[1] / mrss[0])):
                            mrss = [mrss_times[i], mrss_pro[i], seed_set]

                        how_long = round(time.time() - start_time, 4)
                        print("total_time: " + str(how_long) + "sec")
                        print(result[times])
                        print("avg_profit = " + str(round(avg_profit / (times+1), 4)) + ", avg_budget = " + str(round(avg_budget / (times+1), 4)))
                        print("------------------------------------------")

                        if (times + 1) % etimes == 0:
                            # print("output1")
                            fw = open("result/mhdic_pps" + str(pp_strategy) + "_winob" * whether_infect_not_only_buying + "/" +
                                      data_name + "_" + product_name + "/" +
                                      data_name + "_" + product_name + "_b" + str(bud) + "_i" + str(times + 1) + ".txt", 'w')
                            fw.write("data = " + data_name + ", total_budget = " + str(bud) + ", iteration_times = " + str(times + 1) + "\n" +
                                     "whether_infect_not_only_buying = " + str(whether_infect_not_only_buying) + "\n" +
                                     "avg_profit_per_iteration = " + str(round(avg_profit / (times + 1), 4)) + "\n" +
                                     "avg_budget_per_iteration = " + str(round(avg_budget / (times + 1), 4)) + "\n" +
                                     "total_time = " + str(how_long) + ", avg_time = " + str(round(how_long / (times + 1), 4)) + "\n")
                            fw.write("\nprofit_ratio =")
                            for k in range(num_product):
                                fw.write(" " + str(round(pro_k_list[k] / (times + 1), 4)))
                            fw.write("\nbudget_ratio =")
                            for k in range(num_product):
                                fw.write(" " + str(round(bud_k_list[k] / (times + 1), 4)))
                            fw.write("\nseed_number =")
                            for k in range(num_product):
                                fw.write(" " + str(round(avg_num_k_seed[k] / (times + 1), 4)))
                            fw.write("\ncustomer_number =")
                            for k in range(num_product):
                                fw.write(" " + str(round(avg_num_k_an[k] / (times + 1), 4)))
                            fw.write("\n\n")
                            mrss = [mrss[0], round(mrss[1] / mrss[0], 2), mrss[2]]
                            fw.write(str(mrss[0]) + ", " + str(mrss[1]) + ", " + str(mrss[2]) + "\n")

                            for t, r in enumerate(result):
                                fw.write("\n" + str(t) + " " + str(round(r[0], 4)) + " " + str(round(r[1], 4)) + " " + str(r[2]) + " " + str(r[3]) + " " + str(r[4]))
                            fw.close()