import json
from copy import deepcopy
from itertools import chain

import Alg
from DB.db_manager import MAX_GRADE

MEMBER_COUNT = 5


class Team(list):
    project = None
    normalized_record_list = None
    __happiness_var = None

    def __init__(self, f = None):
        if f is not None:
            super().__init__(f)
        else:
            super().__init__()
        self.project = None
        self.normalized_record_list = None
        self.__happiness_var = None

    def __add__(self, record):
        if isinstance(record, Alg.Record.Record):
            self.append(record)
        else:
            raise ValueError("incorrect addend type : {}".format(type(record)))
        self.__happiness_var = None
        return self

    def __sub__(self, record):
        if isinstance(record, Alg.Record.Record):
            self.remove(record)
        else:
            raise ValueError("incorrect minuend type : {}".format(type(record)))
        self.__happiness_var = None
        return self

    def __str__(self):
        return ', '.join([str(x.student_id) for x in self])

    def happiness(self):
        if self.__happiness_var:
            return self.__happiness_var
        else:
            self.normalized_record_list = deepcopy(self)
            [x.normalize() for x in self.normalized_record_list]

            arg = [[] for x in range(len(Alg.Algorithm.priority_vector()))]
            x, i = 0, 0
            while x < len(self.normalized_record_list[0]) - 2:
                for f in range(Alg.Algorithm.priority_vector()[i][1]):
                    arg[i].append([list(self.normalized_record_list[z].values())[x] for z in range(MEMBER_COUNT)])
                    x += 1
                i += 1

            arg_priority = list([x for x in zip(arg, Alg.Algorithm.priority_vector()) if x[1][4]])

            happiness = 0
            for x in range(len(arg_priority)):
                temp = 0
                if arg_priority[x][1][0]:
                    if arg_priority[x][1][3]:
                        pass
                    else:
                        lst = [0 for x in range(MAX_GRADE + 2)]
                        for f in range(len(arg_priority[x][0])):
                            for item in arg_priority[x][0][f]:
                                lst[item] += 2 / (3 ** f)
                        temp = max(lst) * arg_priority[x][1][2]
                else:
                    if arg_priority[x][1][3]:
                        pass
                    else:
                        temp = len(set(chain(*arg_priority[x][0]))) * 10 / 4 * arg_priority[x][1][2]
                        # an attempt to normalize everything to 10
                happiness += temp
                self.__happiness_var = happiness
            return happiness
