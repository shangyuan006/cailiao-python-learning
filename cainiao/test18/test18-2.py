#!/usr/bin/python

num = input('输入 1-10 之间的数字：')
times = int(input('次数：'))
s = 0

for i in range(1, times):
    print(num * i, '+', end=' ')
    s += int(num * i)

print(num * times, '=', s + int(num * times))