from pprint import pprint


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution


class Backtracking(Algorithm):
    def get_algorithm_steps(self, tiles, variables, words):
        domains = {var: [word for word in words] for var in variables}
        discard_incorrect_size_words(variables, domains)
        pprint(domains)
        return None


def discard_incorrect_size_words(variables: dict, domains: dict):
    for position, words in domains.items():
        domains[position] = list(filter(lambda word: len(word) == variables[position], words))

