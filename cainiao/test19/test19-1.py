#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Arlene'

def fun(num):
    sum = 1  # 1要加上，所以默认赋值为1
    for i in range(2, num):  # 因子不包括本身，
        if num % i == 0:
            sum += i
    if sum == num:
        return num
result = []
for num in range(2, 1000):
    test = fun(num)
    if test:   # 去掉空值
        result.append(test)
print("完数有：", result)
