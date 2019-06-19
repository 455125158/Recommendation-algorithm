'''
@-*- coding: utf-8 -*-
@__author__ = "陈宸"
@Project: personal rank
@FileName: 矩阵personal_rank.py
@Date: 2019/6/17

matrix personal rank algorithm
1、用二分图得到M矩阵
2、求公式
'''

from __future__ import division
from scipy.sparse import coo_matrix
import numpy as np
import read

def graph_to_m(graph):
    '''

    :param graph: user and item graph
    :return:matrix M, a list 所有(item+user)顶点, a dict 所有(item+user)顶点位置
    '''

    vertex = list(graph.keys())   # 所有(item+user)顶点
    address_dict = {}       # 所有(item+user)顶点位置
    total_len = len(vertex)
    for index in range(len(vertex)):
        address_dict[vertex[index]] = index  # 每一行对应一个顶点
    row = []
    col = []
    data = []
    for element in graph:                         # element所有item+user的顶点
        weight = round(1/len(graph[element]), 3)  # graph[element]二分图中所有和element相连接的顶点
        row_index = address_dict[element]
        for element in graph[element]:
            col_index = address_dict[element]
            row.append(row_index)
            col.append(col_index)
            data.append(weight)


    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    m = coo_matrix((data,(row,col)), shape=(total_len,total_len))
    return m, vertex, address_dict

def mat_all_point(m_matrix, vertex, alpha):
    '''
    矩阵算法personal_rank的公式
    :param m_matrix:
    :param vertex: 所有(item+user)顶点
    :param alpha: 随机游走的概率
    :return:  矩阵
    '''

    # 初始化单位矩阵（如果使用numpy创建，容易超内存）
    total_len = len(vertex)
    row = []
    col = []
    data = []
    for index in range(total_len):
        row.append(index)
        col.append(index)
        data.append(1)
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    eye_t = coo_matrix((data,(row,col)), shape=(total_len,total_len))
    return eye_t.tocsr() - alpha*m_matrix.tocsr().transpose()

if __name__ == '__main__':
    graph = read.get_graph_from_data('log')
    m, vertex, address_dict = graph_to_m(graph)
    print(address_dict)