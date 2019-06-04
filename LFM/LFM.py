#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"
# Date: 2019/6/3

import numpy as np

import read

def lfm_train(train_data,F,alpha,beta,step):
    '''
    得到lfm模型的用户向量和电影向量
    train_data:train_data for lfm
    F:user_vector len,item_vector len
    alpha: regularization factor
    beta:learning rate
    step:iteration num
    :return:
        dic:key itemid,value:ndarray
        dic:key userid,value:ndarray
    '''
    user_vec ={}
    item_vec ={}

    for step_index in range(step):
        for data_instance in train_data:
            userid,itemid,label = data_instance
            if userid not in user_vec:
                user_vec[userid] = init_model(F)
            if itemid not in item_vec:
                item_vec[userid] = init_model(F)
        delta = label - model_predict(user_vec[userid], item_vec[itemid])
        for index in range(F):
            user_vec[userid][index] = user_vec[userid][index] - beta*(-delta*item_vec[itemid][index] + alpha*user_vec[userid][index])
            item_vec[itemid][index] = item_vec[itemid][index] - beta*(-delta*user_vec[userid][index] + alpha*item_vec[itemid][index])
        beta = beta*0.9
    return user_vec, item_vec

def init_model(vector_len):
    '''

    :param vector_len: the len of vector
    :return: ndarray
    '''
    return np.random.randn(vector_len)


def model_predict(user_vector, item_vector):
    '''

    :param user_vector: model produce user distance
    :param item_vector: model produce item distance
    :return:   a num
    '''
    res = np.dot(user_vector,item_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))
    return res

def model_train_process():
    '''
    test lfm model train
    :return:
    '''
    train_data = read.get_train_data('ratings.csv')
    user_vec,item_vec = lfm_train(train_data,50,0.01,0.1,50)

    recom_result = give_recom_result(user_vec, item_vec, '11')

    ana_recom_result(train_data, '11', recom_result)



def give_recom_result(user_vec, item_vec, userid):
    '''
    user lfm model result give fix userid recom result
    使用lfm得到的推荐结果，和得分
    :param user_vec: lfm model result
    :param item_vec: lfm model result
    :param userid: fix userid
    :return:list : [(itemid,score), (itemid1,score1)]
    '''
    if userid not in user_vec:
        return []
    record = {}
    recom_list = []
    fix_num = 5
    user_vecor = user_vec[userid]
    for itemid in item_vec:
        item_vector = item_vec[itemid]
        res = np.dot(user_vecor,item_vector)/(np.linalg.norm((user_vecor)*np.linalg.norm(item_vector)))
        record[itemid] = res                    # record={'itemid':'res'}
        record_list = list(record.items())      # record.items()=[(itemid,res),(itemid,res)]   在此用list转换格式是Python3的不兼容问题
    for zuhe in sorted(record.items(), key=lambda rec: record_list[1], reverse=True)[:fix_num]:
        itemid = zuhe[0]
        score = round(zuhe[1],3)
        recom_list.append((itemid,score))
    return recom_list


def ana_recom_result(train_data,userid,recom_list):
    '''
    分析推荐结果的好坏
    :param train_data: 之前用户对哪些电影打分高
    :param userid: 分析的用户
    :param recom_list:模型给出的推荐结果
    '''
    item_info = read.get_item_info('movies.csv')
    for data_instance in train_data:
        userid1,itemid,label = data_instance
        if userid1 == userid and label == 1:
            print(item_info[itemid])
    print('返回结果：')
    for zuhe in recom_list:
        print(item_info[zuhe[0]])


if __name__ == '__main__':
    model_train_process()



