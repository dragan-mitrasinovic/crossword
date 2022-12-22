from pprint import pprint


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):

    # tiles je bool matrica gde je True prepreka
    # variables za kljuceve ima 0h, 0v, itd. Za vrednosti duzine reci koje idu na to mesto
    # variables deluje beskorisno nakon discard_incorrect_size_words
    # words je lista reci
    #
    # return je lista listi od 3 promenljive
    # prva je oznaka izabrane pozicije
    # indeks vrednosti izabrane promenljive iz njenog domena, None ako se radi backtrack
    # recnik domains, kljucevi su oznake svih promenljivih, vrednosti lista mogucih reci
    def get_algorithm_steps(self, tiles, variables, words):
        pprint(variables)
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
        solutions = []
        indexes_to_pick = [0] * len(variables)
        backtrack_search(tiles, variables, domains, solutions, 0, indexes_to_pick)
        return solutions


def discard_incorrect_size_words(variables: dict, domains: dict):
    for position, words in domains.items():
        domains[position] = list(filter(lambda word: len(word) == variables[position], words))


def backtrack_search(tiles, variables: dict, domains, solutions, level, indexes_to_pick):
    if level == len(variables):
        return
    current_variable = list(variables.keys())[level]
    if indexes_to_pick[level] == len(domains[current_variable]):
        solutions.append([current_variable, None, domains])
        delete_word(tiles, current_variable, variables[current_variable])
        indexes_to_pick[level] = 0
        backtrack_search(tiles, variables, domains, solutions, level - 1, indexes_to_pick)
        return
    current_value_index = indexes_to_pick[level]
    indexes_to_pick[level] += 1
    if is_consistent_assignment(tiles, current_variable, domains[current_variable][current_value_index]):
        solutions.append([current_variable, current_value_index, domains])
        add_word(tiles, current_variable, domains[current_variable][current_value_index])
        backtrack_search(tiles, variables, domains, solutions, level + 1, indexes_to_pick)
    else:
        backtrack_search(tiles, variables, domains, solutions, level, indexes_to_pick)
    return


def is_consistent_assignment(tiles: list, variable: str, word: str):
    width = len(tiles[0])
    start_index = int(variable[:-1])
    is_horizontal = variable[-1] == "h"
    coordinates = [start_index // width, start_index % width]
    for char in word:
        if tiles[coordinates[0]][coordinates[1]] not in [False, char]:
            return False
        if is_horizontal:
            coordinates[1] += 1
        else:
            coordinates[0] += 1
    return True


def delete_word(tiles: list, variable, length):
    width = len(tiles[0])
    start_index = int(variable[:-1])
    is_horizontal = variable[-1] == "h"
    coordinates = [start_index // width, start_index % width]
    for i in range(length):
        tiles[coordinates[0]][coordinates[1]] = False
        if is_horizontal:
            coordinates[1] += 1
        else:
            coordinates[0] += 1


def add_word(tiles, variable, word: str):
    width = len(tiles[0])
    start_index = int(variable[:-1])
    is_horizontal = variable[-1] == "h"
    coordinates = [start_index // width, start_index % width]
    for char in word:
        tiles[coordinates[0]][coordinates[1]] = char
        if is_horizontal:
            coordinates[1] += 1
        else:
            coordinates[0] += 1
