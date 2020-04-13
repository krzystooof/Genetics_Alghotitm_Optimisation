class Member:
    pass

class Population:
    __member_list = []
    __population_size = 0
    __population_discard = 0.0

    def __init__(self):
        self.__load_population_size()
        self.__load_population_discard()
        self.__member_list.append(self, Member)

    def __load_population_size(self):
        self.__population_size = 0

    def __load_population_discard(self):
        self.__population_discard = 0.0
