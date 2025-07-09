from utils.settings import *
from utils.math_utils import prob

from random import randint, choice

class Agent:
    def __init__(self, pos, time, groups):
        # initialization
        self.pos = pos
        self.time = time
        self.groups = groups
        self.add_groups()
        
    def add_groups(self):
        self.groups = self.groups if type(self.groups) == list else [self.groups]
        for group in self.groups:
            group.add(self)

    def death(self):
        try:
            for group in self.groups:
                group.remove(self)
            del self
        except:
            pass


class Animal(Agent):
    def __init__(self, pos, genes, time, groups, **kwargs):
        super().__init__(pos, time, groups)
        self.next_pos = pos

        # genetic
        self.genes = genes
        self.gender = choice(['male', 'female'])

        # age
        self.age = 0
        self.longevity = kwargs['longevity']

        # hunger
        self.satiety = 0
        self.max_satiety = kwargs['max_satiety']
        self.hunger_rate = kwargs['hunger_rate']

        # mating
        self.recipient = None
        self.senders = []
        self.mate_probability = kwargs['mate_probability']

    def move(self):
        self.next_pos = (self.pos[0] + randint(-1, 1), self.pos[1] + randint(-1, 1))

        if self.next_pos[0] < 0:
            self.next_pos = (ROWS - 1, self.next_pos[1])
        elif self.next_pos[0] == ROWS:
            self.next_pos = (0, self.next_pos[1])

        if self.next_pos[1] < 0:
            self.next_pos = (self.next_pos[0], COLS - 1)
        elif self.next_pos[1] == COLS:
            self.next_pos = (self.next_pos[0], 0)

    def send_request(self, recipient):
        recipient.senders.append(self)
        self.recipient = recipient

    def mate(self, partners):
        # if there are other agents
        if len(partners):
            self.send_request(choice(partners))
        else:
            self.move()

    def give_birth(self):
        if self.recipient in self.senders:
            self.satiety -= self.max_satiety
            if self.genes is not None:
                genes = tuple([choice(pair) for pair in zip(self.genes, self.recipient.genes)])    # crossing-over
                self.__class__(self.pos, genes, self.time, self.groups)
            else:
                self.__class__(self.pos, self.time, self.groups)

    def hunger(self):
        # hunger
        if prob(self.hunger_rate):
            self.satiety -= 1
            if self.satiety <= -self.max_satiety:
                self.death()

    def update(self, partners, eat_func):
        # update position
        self.pos = self.next_pos

        # generate offspring
        self.give_birth()
        
        # reset
        self.recipient = None
        self.senders = []

        # hunger
        self.hunger()

        # age
        self.age += 1
        if self.age > self.longevity:
            self.death()

        # mate, eat or move
        elif self.satiety > 0 and prob(self.mate_probability):
            self.mate(partners)
        elif self.satiety < self.max_satiety:
            eat_func()