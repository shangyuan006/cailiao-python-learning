#!/usr/bin/python

a = str(input('输入一行字符：'))

count1 = 0 # 统计英文字母个数
count2 = 0 # 统计数字个数
count3 = 0 # 统计空格个数
count4 = 0 # 统计其他字符

for i in a:
    if i.isalpha():
        count1 += 1
    elif i.isdigit():
        count2 += 1
    elif i ==' ':
        count3 += 1
    else:
        count4 += 1


print('英文字母个数：%d, 数字个数：%d, 空格个数：%d, 其他字符：%d' % (count1, count2, count3, count4))