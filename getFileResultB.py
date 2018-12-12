for m in range(1, 2):
    model_name = ""
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
            ratio_profit, ratio_budget = [[] for _ in range(num_product)], [[] for _ in range(num_product)]
            number_seed, number_customer = [[] for _ in range(num_product)], [[] for _ in range(num_product)]
            for total_budget in range(1, 10):
                try:
                    result_name = "result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "/" + \
                                  data_name + "_" + product_name + "_b" + str(total_budget) + "_i100.txt"

                    with open(result_name) as f:
                        for lnum, line in enumerate(f):
                            if lnum <= 5:
                                continue
                            elif lnum == 6:
                                (l) = line.split()
                                for nl in range(2, len(l)):
                                    ratio_profit[nl-2].append(l[nl])
                            elif lnum == 7:
                                (l) = line.split()
                                for nl in range(2, len(l)):
                                    ratio_budget[nl-2].append(l[nl])
                            elif lnum == 8:
                                (l) = line.split()
                                for nl in range(2, len(l)):
                                    number_seed[nl-2].append(l[nl])
                            elif lnum == 9:
                                (l) = line.split()
                                for nl in range(2, len(l)):
                                    number_customer[nl-2].append(l[nl])
                            else:
                                break
                    f.close()
                except FileNotFoundError:
                    continue

            fw = open("result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "_ratio_profit.txt", 'w')
            for line in ratio_profit:
                for l in line:
                    fw.write(str(l) + "\t")
                fw.write("\n")
            fw.close()
            fw = open("result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "_ratio_budget.txt", 'w')
            for line in ratio_budget:
                for l in line:
                    fw.write(str(l) + "\t")
                fw.write("\n")
            fw.close()
            fw = open("result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "_number_seed.txt", 'w')
            for line in number_seed:
                for l in line:
                    fw.write(str(l) + "\t")
                fw.write("\n")
            fw.close()
            fw = open("result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "_number_customer.txt", 'w')
            for line in number_customer:
                for l in line:
                    fw.write(str(l) + "\t")
                fw.write("\n")
            fw.close()