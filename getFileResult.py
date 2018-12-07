for pps in range(1, 2):
    for setting in range(1, 2):
        data_name, product_name = "", ""
        if setting == 1:
            data_name = "email"
            product_name = "item_r1p3n1"
        elif setting == 2:
            data_name = "email"
            product_name = "item_r1p3n2"
        num_ratio, num_price = int(list(product_name)[list(product_name).index('r') + 1]), int(list(product_name)[list(product_name).index('p') + 1])
        num_product = num_ratio * num_price
        ratio_profit, ratio_budget = [[] for _ in range(num_product)], [[] for _ in range(num_product)]
        number_seed, number_customer = [[] for _ in range(num_product)], [[] for _ in range(num_product)]
        for total_budget in range(1, 2):
            try:
                result_name = "result/mngic_pps" + str(pps) + "/" + data_name + "_" + product_name + "/" + data_name + "_" + product_name + "_b" + str(total_budget) + "_i1.txt"

                lnum = 0
                with open(result_name) as f:
                    for line in f:
                        lnum += 1
                        if lnum <= 6:
                            continue
                        elif lnum == 7:
                            (l) = line.split()
                            for nl in range(2, len(l)):
                                ratio_profit[nl-2].append(l[nl])
                        elif lnum == 8:
                            (l) = line.split()
                            for nl in range(2, len(l)):
                                ratio_budget[nl-2].append(l[nl])
                        elif lnum == 9:
                            (l) = line.split()
                            for nl in range(2, len(l)):
                                number_seed[nl-2].append(l[nl])
                        elif lnum == 10:
                            (l) = line.split()
                            for nl in range(2, len(l)):
                                number_customer[nl-2].append(l[nl])
                        else:
                            break
                f.close()
            except FileNotFoundError:
                continue

        fw = open("result/mngic_pps" + str(pps) + "/" + data_name + "_" + product_name + "_ratio_profit.txt", 'w')
        for line in ratio_profit:
            for l in line:
                fw.write(str(l) + "\t")
            fw.write("\n")
        fw.close()
        fw = open("result/mngic_pps" + str(pps) + "/" + data_name + "_" + product_name + "_ratio_budget.txt", 'w')
        for line in ratio_budget:
            for l in line:
                fw.write(str(l) + "\t")
            fw.write("\n")
        fw.close()
        fw = open("result/mngic_pps" + str(pps) + "/" + data_name + "_" + product_name + "_number_seed.txt", 'w')
        for line in number_seed:
            for l in line:
                fw.write(str(l) + "\t")
            fw.write("\n")
        fw.close()
        fw = open("result/mngic_pps" + str(pps) + "/" + data_name + "_" + product_name + "_number_customer.txt", 'w')
        for line in number_customer:
            for l in line:
                fw.write(str(l) + "\t")
            fw.write("\n")
        fw.close()