from random import random, choice

def counter():
    x = 0
    while True:
        yield x
        x += 1

def prob(probability):
    return random() * 100 < probability
