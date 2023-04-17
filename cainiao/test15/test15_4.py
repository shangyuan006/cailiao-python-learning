#!/usr/bin/python
# -*- coding: UTF-8 -*-


#score = int(input('请输入分数：\n'))

def score(n):
    score = int(input('请输入分数：\n'))

    if score >= 90:
        grade = 'A'
    elif 60 <= score <= 89:
        grade = 'B'
    else:
        grade = 'C'

    print('%d 属于 %s' % (score, grade))

score(90)