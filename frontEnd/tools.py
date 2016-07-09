# coding: utf-8

# 验证邮箱的函数

import re
import base64


def process_mail(input_mail):
    is_match = bool(
        re.match(r"^[a-zA-Z](([a-zA-Z0-9]*\.[a-zA-Z0-9]*)|[a-zA-Z0-9]*)[a-zA-Z]@([a-z0-9A-Z]+\.)+[a-zA-Z]{2,}$",
                 input_mail, re.VERBOSE));
    if is_match:
        return True
    else:
        return False


def checklen(pwd):
    return len(pwd) >= 8


def checkContainUpper(pwd):
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def checkContainLetter(pwd):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def checkContainNum(pwd):
    pattern = re.compile('[0-9]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def process_passwd(passwd):
    upper_flag = checkContainUpper(passwd)
    num_flag = checkContainNum(passwd)
    letter_flag = checkContainLetter(passwd)
    len_flag = checklen(passwd)

    if upper_flag and num_flag and letter_flag and len_flag:
        return True
    else:
        return False


def judge_limit(low, height):
    if low <= height:
        return True
    else:
        return False


def judge_gender(gender):
    if gender == u'男' or gender == u'女':
        return True
    else:
        return False


