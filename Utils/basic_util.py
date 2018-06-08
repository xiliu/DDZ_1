# coding: utf-8

import operator
import random
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_factorial_value(n):
    if n==1:
        return n
    else:
        return n * get_factorial_value(n-1)

def gen_combination_value(n, m):
    first = get_factorial_value(n)
    second = get_factorial_value(m)
    third = get_factorial_value((n - m))
    return first / (second * third)

