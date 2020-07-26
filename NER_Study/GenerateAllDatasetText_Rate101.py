# -*- coding: utf-8 -*-

"""
Created on 2020/7/14
@author: Ruuku
用于生成包含只来自CVE的 train、validate、test的数据集
其中.分配比为1:0:1
"""

from CommonFunction import File_processing

all_train = ""
all_valid = ""
all_test = ""
all_train_dup = ""
all_valid_dup = ""
all_test_dup = ""

folder = 'Dataset/ner_data/'


def main():
    global all_test, all_train, all_valid, all_test_dup, all_train_dup, all_valid_dup, folder

    # read
    # read memc
    all_train_list = File_processing.read_TXTfile(folder + 'memc_train.txt').split('\n\n')
    all_valid_list = File_processing.read_TXTfile(folder + 'memc_valid.txt').split('\n\n')
    all_test_list = File_processing.read_TXTfile(folder + 'memc_test.txt').split('\n\n')
    print(len(all_train_list), len(all_valid_list), len(all_test_list))

    all_train_list_dup = File_processing.read_TXTfile(folder + 'memc_train.txt').split('\n\n')
    all_valid_list_dup = File_processing.read_TXTfile(folder + 'memc_valid.txt').split('\n\n')
    all_test_list_dup = File_processing.read_TXTfile(folder + 'memc_test.txt').split('\n\n')
    # print(len(all_train_list), len(all_valid_list), len(all_test_list))

    completed_categ = []
    file_names = File_processing.walk_L1_FileNames(folder)
    for file_name in file_names:
        categ_name = file_name.split('_')[0]

        if file_name.startswith('memc_') or file_name.startswith('.') or file_name.startswith(
                'all_') or categ_name in completed_categ:
            continue
        else:
            print('categ_name', categ_name)
            # read test
            cate_all_dataset = File_processing.read_TXTfile(folder + categ_name + '_full_dup.txt').split('\n\n')
            # aim - 过程
            # target - 最终结果
            cate_aim_dataset = []
            cate_target_dataset = []
            for cate_data in cate_all_dataset:
                # choose the dataset with cve in firstline
                line_list = cate_data.split("\n")
                third_words = line_list[0].split(" ")[5]
                if third_words.startswith('cve'):
                    temp = ""
                    for line in line_list:
                        word_list = line.split(" ")
                        if word_list[0] == "":
                            break
                        temp += word_list[0] + " " + word_list[1] + "\n"
                    cate_target_dataset.append(temp)
                    cate_aim_dataset.append(cate_data)
            len_cate_dataset = len(cate_aim_dataset)

            # print(train_dataset_list)
            # print(test_dataset_list)

            # extent dataset list
            all_train_list_dup.extend(cate_aim_dataset[:int(len_cate_dataset * 1 / 2)])
            # all_valid_list_dup.extend()
            all_test_list_dup.extend(cate_aim_dataset[int(len_cate_dataset * 1 / 2):])

            all_train_list.extend(cate_target_dataset[:int(len_cate_dataset * 1 / 2)])
            # all_valid_list.extend()
            all_test_list.extend(cate_target_dataset[int(len_cate_dataset * 1 / 2):])
            print(len(all_train_list), len(all_valid_list), len(all_test_list))

            # write categ
            cate_train = ''
            cate_valid = ''
            cate_test = ''

            cate_train_dup = ''
            cate_valid_dup = ''
            cate_test_dup = ''

            for ele in cate_aim_dataset[:int(len_cate_dataset * 1/2)]:
                cate_train_dup += ele + '\n\n'
            # for ele in cate_aim_dataset[int(len_cate_dataset * 5 / 8): int(len_cate_dataset * 6 / 8)]:
            #     cate_valid_dup += ele + '\n\n'
            for ele in cate_aim_dataset[int(len_cate_dataset * 1 / 2):]:
                cate_test_dup += ele + '\n\n'

            for ele in cate_target_dataset[:int(len_cate_dataset * 1 / 2)]:
                cate_train += ele + '\n\n'
            # for ele in cate_target_dataset[int(len_cate_dataset * 5 / 8): int(len_cate_dataset * 6 / 8)]:
            #     cate_valid += ele + '\n\n'
            for ele in cate_target_dataset[int(len_cate_dataset * 1 / 2):]:
                cate_test += ele + '\n\n'

            File_processing.write_TXTfile(folder + 'integrated_dataset/' + categ_name + '_train_dup.txt',
                                          cate_train_dup)
            File_processing.write_TXTfile(folder + 'integrated_dataset/' + categ_name + '_valid_dup.txt',
                                          cate_valid_dup)
            File_processing.write_TXTfile(folder + 'integrated_dataset/' + categ_name + '_test_dup.txt',
                                          cate_test_dup)

            File_processing.write_TXTfile(folder + 'integrated_dataset/' + categ_name + '_train.txt',
                                          cate_train)
            File_processing.write_TXTfile(folder + 'integrated_dataset/' + categ_name + '_valid.txt',
                                          cate_valid)
            File_processing.write_TXTfile(folder + 'integrated_dataset/' + categ_name + '_test.txt',
                                          cate_test)

        completed_categ.append(categ_name)

    # write all
    # org txt
    for ele in all_train_list:
        all_train += ele + '\n\n'
    for ele in all_valid_list:
        all_valid += ele + '\n\n'
    for ele in all_test_list:
        all_test += ele + '\n\n'

    for ele in all_train_list_dup:
        all_train_dup += ele + '\n\n'
    for ele in all_valid_list_dup:
        all_valid_dup += ele + '\n\n'
    for ele in all_test_list_dup:
        all_test_dup += ele + '\n\n'

    File_processing.write_TXTfile(folder + 'integrated_dataset/' + 'all_train_dup.txt', all_train_dup)
    File_processing.write_TXTfile(folder + 'integrated_dataset/' + 'all_valid_dup.txt', all_valid_dup)
    File_processing.write_TXTfile(folder + 'integrated_dataset/' + 'all_test_duptxt', all_test_dup)

    File_processing.write_TXTfile(folder + 'integrated_dataset/' + 'all_train.txt', all_train)
    File_processing.write_TXTfile(folder + 'integrated_dataset/' + 'all_valid.txt', all_valid)
    File_processing.write_TXTfile(folder + 'integrated_dataset/' + 'all_test.txt', all_test)


if __name__ == '__main__':
    main()
    print()
