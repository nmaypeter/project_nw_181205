for m in range(1, 2):
    model_name = " "
    if m == 1:
        model_name = "mngic_pps"
    elif m == 2:
        model_name = "mhdic_pps"
    elif m == 3:
        model_name = "mric_pps"
    for pps in range(1, 4):
        for setting in range(1, 5):
            data_name, product_name = "", ""
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
            num_ratio, num_price = int(list(product_name)[list(product_name).index('r') + 1]), int(list(product_name)[list(product_name).index('p') + 1])
            num_product = num_ratio * num_price
            execution_times, etimes = 100, 10
            num_exe = int(execution_times / etimes)
            avgtime, totaltime, profit, budget = [[] for _ in range(num_exe)], [[] for _ in range(num_exe)], [[] for _ in range(num_exe)], [[] for _ in range(num_exe)]
            for total_budget in range(1, 10):
                for e in range(num_exe):
                    # try:
                    result_name = "result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "/" + \
                                  data_name + "_" + product_name + "_b" + str(total_budget) + "_i" + str((e + 1) * etimes) + ".txt"
                    print(result_name)
                    with open(result_name) as f:
                        for lnum, line in enumerate(f):
                            if lnum <= 1:
                                continue
                            elif lnum == 2:
                                (l) = line.split()
                                profit[e].append(l[-1])
                            elif lnum == 3:
                                (l) = line.split()
                                budget[e].append(l[-1])
                            elif lnum == 4:
                                (l) = line.split()
                                totaltime[e].append(l[2].rstrip(','))
                                avgtime[e].append(l[-1])
                            else:
                                break
                    f.close()
                    # except FileNotFoundError:
                    #     continue

            fw = open("result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "_avgtime.txt", 'w')
            for line in avgtime:
                for l in line:
                    fw.write(str(l) + "\t")
                fw.write("\n")
            fw.close()
            fw = open("result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "_totaltime.txt", 'w')
            for line in totaltime:
                for l in line:
                    fw.write(str(l) + "\t")
                fw.write("\n")
            fw.close()
            fw = open("result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "_profit.txt", 'w')
            for line in profit:
                for l in line:
                    fw.write(str(l) + "\t")
                fw.write("\n")
            fw.close()
            fw = open("result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "_budget.txt", 'w')
            for line in budget:
                for l in line:
                    fw.write(str(l) + "\t")
                fw.write("\n")
            fw.close()