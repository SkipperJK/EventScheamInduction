import logging
from unittest import TestCase


class TripleBigram:

    def __init__(self, id_t1, id_t2, dist, count=0, e11=0, e12=0, e21=0, e22=0):
        self.id_t1 = id_t1
        self.id_t2 = id_t2
        self.dist = dist
        self.count = count
        self.e11 = e11
        self.e12 = e12
        self.e21 = e21
        self.e22 = e22


    def to_string(self):
        return "{:s}, Count:{:d}, E11:{:d}, E12:{:d}, E21:{:d}, E22:{:d}".format(
            str(self),
            self.count,
            self.e11,
            self.e12,
            self.e21,
            self.e22
        )


    def __str__(self):
        return "T1:{:d} T2:{:d} Dist:{:d}".format(self.id_t1, self.id_t2, self.dist)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)


class TestTripleBigram(TestCase):

    def test_t(self):
        tb = TripleBigram(1,2,1)
        print(tb)
        print(tb.to_string())
        tbo = TripleBigram(1,2,1, count=100)
        d = {}
        d[tb] = 10
        print(d[tbo])
