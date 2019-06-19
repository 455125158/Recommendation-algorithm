#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"
# Date: 2019/6/15

'''
personal rank main algo
'''
from __future__ import division
import numpy as np
import read
import operator
import 矩阵personal_rank as mat_util
from scipy.sparse.linalg import gmres


def personal_rank(graph, root, alpha, iter_num, recom_num=10):
    '''
    param
        graph:user item graph
        root: the recommend for the fixed user
        alpha: the probability to go random walk
        iter_num: iteration num
        recon_num: recommend item num
    :return: a dict,key:itemid , value:PR
    '''

    rank = {}               # 所有顶点对于root顶点的PR值
    rank = {i: 0 for i in graph}
    rank[root] = 1
    recon_result ={}            # 输出
    for iter_dex in range(iter_num):
        tmp_rank = {}       # 记录该迭代轮次下，其他顶点对root顶点的PR值
        tmp_rank = {i: 0 for i in graph}
        for out_userid, out_dict in graph.items():
            # out_point是userid，out_dict是userid评分高于4.5分的电影字典{'item_10': 1}
            # 代表着二分图中用户指向物品的箭头
            for inner_itemid, value in graph[out_userid].items():
                # graph[out_point]:{'item_1196': 1}
                tmp_rank[inner_itemid] += round(alpha*rank[out_userid]/len(out_dict), 4)
                if inner_itemid == root:
                    tmp_rank[inner_itemid] += round(1-alpha,4)
        if tmp_rank == rank:
            print('out'+str(iter_dex))
            break
        rank = tmp_rank

    # 排序
    right_num = 0
    for zuhe in sorted(rank.items(), key=operator.itemgetter(1), reverse=True):
        point_item, pr_score = zuhe[0], zuhe[1]
        if len(point_item.split('_')) < 2:     # 若这个顶点不是item顶点就过滤掉
            continue
        if point_item in graph[root]:          # 若这个item被当前的user行为过，就过滤
            continue
        recon_result[point_item] = pr_score
        right_num += 1
        if right_num > recom_num:
            break
    return recon_result


def personal_rank_matrix(graph,root,alpha,recom_num=10):
    '''
    矩阵形式的
    :param graph:user and item graph
    :param root: the fix user to recommend
    :param alpha: probability to random walk
    :param recom_num:item num
    :return: a dict:{key:item,value:pr_score}
    '''
    m, vertex, address_dict = mat_util.graph_to_m(graph)   # address_dict 所有顶点的行号
    if root not in address_dict:
        return {}

    pr_score_dict = {}                # 未排序pr值
    pr_recom_dic = {}                 # 已排序pr值

    mat_all = mat_util.mat_all_point(m,vertex,alpha)   # A
    index = address_dict[root]
    initial_r0_list = [[0] for i in range(len(vertex))]
    print(initial_r0_list)
    initial_r0_list[index] = [1]
    r0_array = np.array(initial_r0_list)

    res = gmres(mat_all, r0_array, tol=1e-8)[0]   # r = A*r0

    # 存储、排序 pr值
    for i in range(len(res)):
        point = vertex[i]
        if len(point.strip().split('_')) < 2:
            continue
        if point in graph[root]:
            continue
        pr_score_dict[point] = round(res[i], 3)
    for zuhe in sorted(pr_score_dict.items(), key=operator.itemgetter(1), reverse=True)[:recom_num]:
        point, pr_score = zuhe[0], zuhe[1]
        pr_recom_dic[point] = pr_score
    return pr_recom_dic





def get_one_recom():
    '''
    give one fixed user , recommend result
    :return:
    '''
    user = "1"
    alpha = 0.8
    graph = read.get_graph_from_data('ratings.csv')
    iter_num = 100
    pr_recom_result = personal_rank(graph, user, alpha, iter_num, 100)
    return pr_recom_result


    '''
    item_info = read.get_item_info('movies.csv')  # {itemid:[title,genre]}

    for itemid in graph[user]:
        pure_itemid = itemid.split('_')[1]
        print(item_info[pure_itemid])
    print('--------------------------推荐结果-----------------------------')
    for itemid in recom_result:
        pure_itemid = itemid.split('_')[1]
        print(item_info[pure_itemid])
        print(recom_result[itemid])
    '''


def test_one_user_by_matrix():
    '''
    give one fixed user , recommend result,by matrix
    :return:
    '''
    user = "1"
    alpha = 0.8
    graph = read.get_graph_from_data('ratings.csv')
    pr_recom_resuit = personal_rank_matrix(graph, user, alpha, 100)
    return pr_recom_resuit



if __name__ == "__main__":
    recom_resuit_base = get_one_recom()
    recom_resuit_matrix = test_one_user_by_matrix()
    num = 0
    for i in recom_resuit_base:
        if i in recom_resuit_matrix:
            num += 1
    print(num)


