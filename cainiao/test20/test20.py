#!/usr/bin/python
# -*- coding: utf-8 -*-

tour = []
height = []

hei = 100.0 # 起始高度
tim = 10 # 次数

for i in range(1, tim + 1):
    # 从第二次开始，落地时的距离应该是反弹高度乘以2（弹到最高点再落下）
    if i == 1:
        