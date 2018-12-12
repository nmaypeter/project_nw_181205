import os
from shutil import copyfile

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
            execution_times, etimes = 100, 10
            num_exe = int(execution_times / etimes)
            for total_budget in range(1, 11):
                for e in range(num_exe):
                    result_name = "result/" + model_name + str(pps) + "/" + data_name + "_" + product_name + "/" + \
                                  data_name + "_" + product_name + "_b" + str(total_budget) + "_i" + str((e + 1) * etimes) + ".txt"
                    # try:
                        # print(result_name)
                    with open(result_name) as f:
                        mrss_times, mrss_pro, mrss_set = [], [], []
                        mrss = [0, 0.0, ""]
                        for lnum, line in enumerate(f):
                            if lnum <= 10:
                                continue
                            else:
                                (l) = line.split('[')
                                (pro) = float((l[0].split(' '))[1])
                                a_mrss_set = ('[' + l[-1]).rstrip()
                                if a_mrss_set not in mrss_set:
                                    mrss_times.append(1)
                                    mrss_pro.append(pro)
                                    mrss_set.append(a_mrss_set)
                                else:
                                    i = mrss_set.index(a_mrss_set)
                                    mrss_times[i] += 1
                                    mrss_pro[i] += pro

                                i = mrss_set.index(a_mrss_set)
                                if (mrss_times[i] > mrss[0]) or ((mrss_times[i] == mrss[0]) and (mrss_pro[i] / mrss_times[i]) > (mrss[1] / mrss[0])):
                                    mrss = [mrss_times[i], mrss_pro[i], a_mrss_set]
                                    continue
                        mrss = [mrss[0], round(mrss[1] / mrss[0], 2), mrss[2]]
                        # print(mrss)
                        fw = open("temp.txt", 'w')
                        with open(result_name) as f:
                            for lnum, line in enumerate(f):
                                if lnum == 4:
                                    fw.write(line.replace(":", " ="))
                                    continue
                                fw.write(line)
                                if lnum == 10:
                                    fw.write(str(mrss[0]) + ", " + str(mrss[1]) + ", " + str(mrss[2]) + "\n\n")
                        f.close()
                        fw.close()

                        # try:
                        copyfile("temp.txt", result_name)
                        # except:
                        #     print(result_name + ", copy")
                        #     continue
                    # except:
                    #     print(result_name)
                    #     continue
os.remove("temp.txt")