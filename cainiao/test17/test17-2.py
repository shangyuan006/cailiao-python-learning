#!/usr/bin/python

a = str(input('输入一行字符：'))

count1 = 0 # 统计英文字母个数
count2 = 0 # 统计数字个数
count3 = 0 # 统计空格个数
count4 = 0 # 统计其他字符

for i in range(len(a)):
    if ("0" <= a[i] <= "9"):
        count2 += 1
    elif ("A" <= a[i] <= "Z" or "a" <= a[i] <= "z"):
        count1 += 1
    elif (a[i] == " "):
        count3 += 1

count4 = len(a) - count1 - count2 - count3

print('英文字母个数：%d, 数字个数：%d, 空格个数：%d, 其他字符：%d' % (count1, count2, count3, count4))