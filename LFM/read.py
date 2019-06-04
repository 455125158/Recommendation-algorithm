#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"
# Date: 2019/6/1

import os

def get_item_info(input_file):
    '''
    get item info :[title, gemre]
    :param item
    :return: a dict: key item_id, value:[title, genre]
    '''

    if not os.path.exists(input_file):
        return {}
    linenum = 0
    item_info = {}
    fp = open(input_file, encoding='UTF-8')
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        elif len(item) == 3:
            itemid, title, genre = item[0], item[1], item[2]
        elif len(item) > 3:
            itemid = item[0]
            genre = item[-1]
            title = ','.join(item[1:-1])
        item_info[itemid] = [title, genre]
    fp.close()
    return item_info


def get_ave_score(input_file):
    '''
    get item ave reting score
    :param input_file: user rating file
    :return: dict,key:itemid,value:sve_score
    '''

    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {}
    score_dict = {}
    tp = open(input_file, encoding='UTF-8')
    for line in tp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        userid,itemid,rating = item[0],item[1],float(item[2])
        if itemid not in record_dict:
            record_dict[itemid] = [0,0]
        record_dict[itemid][0] += 1
        record_dict[itemid][1] += rating
    tp.close()
    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1]/record_dict[itemid][0],3)
        return score_dict

def get_train_data(input_file):
    '''
    get train data for LFM model train
    :param input_file:user item rating file
    :return:a list: [(userid,itemid,label),(userid1,itemid,label)]
    '''
    if not os.path.exists(input_file):
        return {}
    score_dict = get_ave_score(input_file)
    neg_dic = {}
    pos_dic = {}
    train_data = []
    linenum = 0
    with open(input_file, encoding='UTF-8') as fp:
        for line in fp:
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split(',')
            if len(item) < 4:
                continue
            userid,item,rating = item[0],item[1],float(item[2])
            if userid not in pos_dic:
                pos_dic[userid] = []
            if userid not in neg_dic:
                neg_dic[userid] = []

            if rating >= 4.0:
                pos_dic[userid].append((item, 1))
            else:
                score = score_dict.get(item, 0)
                neg_dic[userid].append((item,score))

    for userid in pos_dic:
        data_num = min(len(pos_dic[userid]), len(neg_dic.get(userid,[])))
        if data_num > 0:
            train_data += [(userid,zuhe[0],zuhe[1]) for zuhe in pos_dic[userid]][:data_num]
        else:
            continue

        sorted_neg_list = sorted(neg_dic[userid], key=lambda element : element[1], reverse=True)
        train_data += [(userid,zuhe[0],0) for zuhe in sorted_neg_list]
    return train_data


if __name__ == '__main__':
    # item_dict = get_item_info('movies.csv')
    # print(len(item_dict))
    # print(item_dict['1'])
    # print(item_dict['11'])

    score_dict = get_ave_score('ratings.csv')
    print(len(score_dict))



