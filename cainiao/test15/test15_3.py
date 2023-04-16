#!/usr/bin/python
# -*- coding: UTF-8 -*-

score = int(input('请输入分数：\n')) #in range(0, 100)

if score in range(90, 100):
    grade = 'A'
elif score in range(60, 89):
    grade = 'B'
else:
    grade = 'C'


# if not isinstance(score, int):
#     print('请输入一个正确的数字！')
#     exit(0)
# else:
print('%d 属于 %s' % (score, grade))
