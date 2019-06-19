#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"
# Date: 2019/6/15

'''
get graph from user data
'''


import os

def get_item_info(input_file):
    '''
    get item info:[title,genre]
    :param input_file:
    :return: a dict:{itemid:[title,genre]}
    '''
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    item_info = {}
    with open(input_file, encoding='UTF-8') as fp:
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
                genre = item[2]
                title = ','.join(item[1:-1])
            item_info[itemid] = [title, genre]
    return item_info




def get_graph_from_data(input_file):
    '''

    :param input_file: user to rating of item file
    :return:
        a dict:{userA:{itemb:1,itemc:1},itemb:{userA:1}}
        以user为key，value是user行为过的item
        以item为key，value是item被行为过的user
    '''

    if not os.path.exists(input_file):
        print('文件不存在')
        return {}

    graph = {}
    linenum = 0
    with open(input_file, encoding='utf-8') as fp:
        for line in fp:
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split(',')
            if len(item) < 3:
                continue
            userid,itamid,rating = item[0], "item_"+item[1], item[2]
            if float(rating) < 4.5:
                continue
            if userid not in graph:
                graph[userid] = {}
            graph[userid][itamid] = 1
            if itamid not in graph:
                graph[itamid] = {}
            graph[itamid][userid] = 1
        return graph




if __name__ == "__main__":
    list = [1, 1, 1, 1]
    list[1] = [2]
    print(list)
