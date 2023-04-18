#!/usr/bin/python

from functools import reduce

#Tn = 0
#Sn = []
n = int(input('n = '))
a = int(input('a = '))
list = []

for i in range(1, n+1):
    list.append(int("{}".format(a)*i))

s = reduce(lambda x, y : x + y, list)

print(list)
print("计算和为：", s)