from SeedSelection_NaiveGreedy import *

if __name__ == "__main__":
    for pp_strategy in range(1, 4):
        data_name, product_name = "", ""
        for setting in range(1, 2):
            # print("setting = " + str(setting))
            if setting == 1:
                data_name = "email"
                product_name = "item_r1p3n1"
            elif setting == 2:
                data_name = "email"
                product_name = "item_r1p3n2"
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

                result_profit_list = [[] for _ in range(int(execution_times / etimes))]
                result_budget_list = [[] for _ in range(int(execution_times / etimes))]
                result_avgtime_list = [[] for _ in range(int(execution_times / etimes))]
                result_totaltime_list = [[] for _ in range(int(execution_times / etimes))]
                result_numseed_list = [[0 for _ in range(num_product)] for _ in range(int(execution_times / etimes))]
                result_numan_list = [[0 for _ in range(num_product)] for _ in range(int(execution_times / etimes))]
                for bud in range(1, total_budget + 1):
                    # print("bud = " + str(bud))
                    start_time = time.time()
                    result = []
                    avg_profit, avg_budget = 0.0, 0.0
                    pro_k_list, bud_k_list = [0.0 for _ in range(num_product)], [0.0 for _ in range(num_product)]
                    avg_num_k_seed, avg_num_k_an = [0 for _ in range(num_product)], [0 for _ in range(num_product)]

                    ssng = SeedSelection_NG(graph_dict, seed_cost_dict, product_list, bud, pp_strategy, whether_infect_not_only_buying)
                    dnic = D_NormalIC(graph_dict, seed_cost_dict, product_list, bud, pp_strategy, whether_infect_not_only_buying)

                    # print("calAllSeedProfit")
                    all_profit_list, notban_set = ssng.calAllSeedProfit(wallet_list)

                    for times in range(execution_times):
                        # print("times = " + str(times))
                        print("budget = " + str(bud) + ", iteration = " + str(times) + ", pp_strategy = " + str(pp_strategy) +
                              ", whether_infect_not_only_buying = " + str(whether_infect_not_only_buying))
                        now_profit, now_budget = 0.0, 0.0
                        seed_set, activated_node_set = [set() for _ in range(num_product)], [set() for _ in range(num_product)]
                        personal_prob_list = [[1.0 for _ in range(num_node)] for _ in range(num_product)]
                        current_wallet_list = copy.deepcopy(wallet_list)
                        expect_profit_list = copy.deepcopy(all_profit_list)
                        nban_set = copy.deepcopy(notban_set)

                        # print("getMostValuableSeed")
                        mep_k_prod, mep_i_node, nban_set = ssng.getMostValuableSeed(expect_profit_list, nban_set)

                        # -- main --
                        while now_budget < bud and mep_i_node != '-1':
                            # print("addSeedIntoSeedSet")
                            seed_set, activated_node_set, nban_set, current_k_profit, current_k_budget, current_wallet_list, personal_prob_list = \
                                dnic.insertSeedIntoSeedSet(mep_k_prod, mep_i_node, seed_set, activated_node_set, nban_set, current_wallet_list, personal_prob_list)
                            pro_k_list[mep_k_prod] += round(current_k_profit, 4)
                            bud_k_list[mep_k_prod] += round(current_k_budget, 4)
                            now_profit += current_k_profit
                            now_budget += current_k_budget
                            # print("updateProfitList")
                            expect_profit_list = ssng.updateProfitList(expect_profit_list, nban_set, now_budget, activated_node_set, current_wallet_list, personal_prob_list)
                            # print("getMostValuableSeed")
                            mep_k_prod, mep_i_node, nban_set = ssng.getMostValuableSeed(expect_profit_list, nban_set)

                        # print("result")
                        now_num_k_seed, now_num_k_an = [len(k) for k in seed_set], [len(k) for k in activated_node_set]
                        result.append([round(now_profit, 4), round(now_budget, 4), now_num_k_seed, now_num_k_an, seed_set])
                        avg_profit += now_profit
                        avg_budget += now_budget
                        for k in range(num_product):
                            avg_num_k_seed[k] += now_num_k_seed[k]
                            avg_num_k_an[k] += now_num_k_an[k]

                        how_long = round(time.time() - start_time, 4)
                        print("total_time: " + str(how_long) + "sec")
                        print(result[times])
                        print("avg_profit = " + str(round(avg_profit / (times+1), 4)) + ", avg_budget = " + str(round(avg_budget / (times+1), 4)))

                        if (times + 1) % etimes == 0:
                            # print("output1")
                            fw = open("result/mngic_pps" + str(pp_strategy) + "_winob" * whether_infect_not_only_buying + "/" +
                                      data_name + "_" + product_name + "/" +
                                      data_name + "_" + product_name + "_b" + str(bud) + "_i" + str(times + 1) + ".txt", 'w')
                            fw.write("data = " + data_name + ", total_budget = " + str(bud) + ", iteration_times = " + str(times + 1) + "\n" +
                                     "whether_infect_not_only_buying = " + str(whether_infect_not_only_buying) + "\n" +
                                     "avg_profit_per_iteration = " + str(round(avg_profit / (times + 1), 4)) + "\n" +
                                     "avg_budget_per_iteration = " + str(round(avg_budget / (times + 1), 4)) + "\n" +
                                     "total_time: " + str(how_long) + ", avg_time = " + str(round(how_long / (times + 1), 4)) + "\n")
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
                            fw.write("\n")

                            for t, r in enumerate(result):
                                fw.write("\n" + str(t) + " " + str(round(r[0], 4)) + " " + str(round(r[1], 4)) + " " + str(r[2]) + " " + str(r[3]) + " " + str(r[4]))
                            fw.close()

                            # -- append the budget result behind per etime list --
                            result_profit_list[int((times + 1) / etimes) - 1].append(str(round(avg_profit / (times + 1), 4)) + "\t")
                            result_budget_list[int((times + 1) / etimes) - 1].append(str(round(avg_budget / (times + 1), 4)) + "\t")
                            result_avgtime_list[int((times + 1) / etimes) - 1].append(str(round(how_long / (times + 1), 4)) + "\t")
                            result_totaltime_list[int((times + 1) / etimes) - 1].append(str(how_long) + "\t")

                # print("output2")
                fw = open("result/mngic_pps" + str(pp_strategy) + "_winob" * whether_infect_not_only_buying + "/" +
                          data_name + "_" + product_name + "_profit.txt", 'w')
                for line in result_profit_list:
                    for l in line:
                        fw.write(str(l))
                    fw.write("\n")
                fw.close()
                fw = open("result/mngic_pps" + str(pp_strategy) + "_winob" * whether_infect_not_only_buying + "/" +
                          data_name + "_" + product_name + "_avgtime.txt", 'w')
                for line in result_avgtime_list:
                    for l in line:
                        fw.write(str(l))
                    fw.write("\n")
                fw.close()
                fw = open("result/mngic_pps" + str(pp_strategy) + "_winob" * whether_infect_not_only_buying + "/" +
                          data_name + "_" + product_name + "_totaltime.txt", 'w')
                for line in result_totaltime_list:
                    for l in line:
                        fw.write(str(l))
                    fw.write("\n")
                fw.close()