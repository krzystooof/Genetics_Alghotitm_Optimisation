# TODO imports



# TODO wywal komentarz jak przeczytasz @Grzegorz
# Twoje zadanie:
# Napisz w tym pliku kod tak, aby nie zmieniając innych plików
# main_alg dobrze się odpalał


class Algorithm:
    def __init__(self, function_type,
                 values,
                 population,
                 accuracy,
                 rand_low,
                 rand_high,
                 reverse):
        self.reverse = reverse
        self.rand_high = rand_high
        self.rand_low = rand_low
        self.accuracy = accuracy
        self.population = population
        self.values = values
        self.function_type = function_type

    def run(self):
        return 0