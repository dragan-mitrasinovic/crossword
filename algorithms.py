import copy
import itertools


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
    def get_algorithm_steps(self, tiles: list, variables: dict, words: list):
        domains = {var: [word for word in words] for var in variables}
        discard_incorrect_size_words(variables, domains)
        solutions = []
        indexes_to_pick = [0] * len(variables)
        backtrack_search(tiles, variables, domains, solutions, indexes_to_pick)
        return solutions


class ForwardChecking(Algorithm):
    def get_algorithm_steps(self, tiles: list, variables: dict, words: list):
        domains = {var: [word for word in words] for var in variables}
        discard_incorrect_size_words(variables, domains)
        solutions = []
        indexes_to_pick = [0] * len(variables)
        forward_check_search(tiles, variables, domains, solutions, indexes_to_pick)
        return solutions


class ArcConsistency(Algorithm):
    def get_algorithm_steps(self, tiles: list, variables: dict, words: list):
        domains = {var: [word for word in words] for var in variables}
        discard_incorrect_size_words(variables, domains)
        solutions = []
        indexes_to_pick = [0] * len(variables)
        arc_consistency_search(tiles, variables, domains, solutions, indexes_to_pick)
        return solutions


def discard_incorrect_size_words(variables: dict, domains: dict):
    for position, words in domains.items():
        domains[position] = list(filter(lambda word: len(word) == variables[position], words))


def backtrack_search(tiles: list, variables: dict, domains: dict, solutions: list, indexes_to_pick: list):
    level = 0
    while level != len(variables):
        current_variable = list(variables.keys())[level]

        if indexes_to_pick[level] == len(domains[current_variable]):
            solutions.append([current_variable, None, domains])
            last_variable = list(variables.keys())[level - 1]
            delete_word(tiles, last_variable, variables[last_variable])
            indexes_to_pick[level] = 0
            level -= 1
            continue

        current_value_index = indexes_to_pick[level]
        indexes_to_pick[level] += 1
        if is_consistent_assignment(tiles, current_variable, domains[current_variable][current_value_index]):
            solutions.append([current_variable, current_value_index, domains])
            add_word(tiles, current_variable, domains[current_variable][current_value_index])
            level += 1
        continue


def forward_check_search(tiles: list, variables: dict, domains: dict, solutions: list, indexes_to_pick: list):
    level = 0
    while level != len(variables):
        current_variable = list(variables.keys())[level]

        if any_domain_is_empty(domains):
            domains = solutions[-2][2]
            last_variable = list(variables.keys())[level - 1]
            delete_word(tiles, last_variable, variables[last_variable])
            level -= 1
            continue

        current_value_index = indexes_to_pick[level]
        indexes_to_pick[level] += 1
        if is_consistent_assignment(tiles, current_variable, domains[current_variable][current_value_index]):
            forward_check(tiles, variables, domains, level, domains[current_variable][current_value_index])
            solutions.append([current_variable, current_value_index, copy.deepcopy(domains)])
            add_word(tiles, current_variable, domains[current_variable][current_value_index])
            level += 1
        continue


def arc_consistency_search(tiles: list, variables: dict, domains: dict, solutions: list, indexes_to_pick: list):
    level = 0
    while level != len(variables):
        current_variable = list(variables.keys())[level]

        if any_domain_is_empty(domains):
            domains = solutions[-2][2]
            last_variable = list(variables.keys())[level - 1]
            delete_word(tiles, last_variable, variables[last_variable])
            level -= 1
            continue

        current_value_index = indexes_to_pick[level]
        indexes_to_pick[level] += 1
        if is_consistent_assignment(tiles, current_variable, domains[current_variable][current_value_index]):
            old_domains = domains
            if arc_consistency_check_fails(tiles, variables, domains, level):
                domains = old_domains
                continue
            forward_check(tiles, variables, domains, level, domains[current_variable][current_value_index])
            solutions.append([current_variable, current_value_index, copy.deepcopy(domains)])
            add_word(tiles, current_variable, domains[current_variable][current_value_index])
            level += 1
        continue


def is_consistent_assignment(tiles: list, variable: str, word: str):
    index = int(variable[:-1])
    is_horizontal = variable[-1] == "h"

    for char in word:
        current_mark = get_matrix_element(tiles, index)
        if not (current_mark is False or char in current_mark):
            return False

        index = inc_matrix_index(tiles, index, is_horizontal)
    return True


def forward_check(tiles: list, variables: dict, domains: dict, level: int, word: str):
    new_word_letter_positions = get_index_list(tiles, variables, list(variables.keys())[level])

    for variable in list(variables.keys())[level + 1:]:
        variable_letter_positions = get_index_list(tiles, variables, variable)
        possible_conflict_positions = list(set(new_word_letter_positions).intersection(variable_letter_positions))

        if len(possible_conflict_positions) == 0:
            continue

        for possible_word in list(domains[variable]):
            for conflict_index in possible_conflict_positions:
                added_char = word[new_word_letter_positions.index(conflict_index)]
                words_char = possible_word[variable_letter_positions.index(conflict_index)]
                if words_char != added_char:
                    domains[variable].remove(possible_word)
                    break
    return True


def arc_consistency_check_fails(tiles: list, variables: dict, domains: dict, level: int):
    new_word_letter_positions = get_index_list(tiles, variables, list(variables.keys())[level])
    possibly_impacted_variables = []

    for variable in list(variables.keys())[level + 1:]:
        variable_letter_positions = get_index_list(tiles, variables, variable)
        possible_conflict_positions = list(set(new_word_letter_positions).intersection(variable_letter_positions))
        if len(possible_conflict_positions) != 0:
            possibly_impacted_variables.append(variable)

    combinations = itertools.product(possibly_impacted_variables, list(variables.keys())[level + 1:])

    for x, y in combinations:
        x_letter_positions = get_index_list(tiles, variables, x)
        y_letter_positions = get_index_list(tiles, variables, y)
        possible_conflict_positions = list(set(x_letter_positions).intersection(y_letter_positions))
        if len(possible_conflict_positions) == 0:
            continue
        for word_x in list(domains[x]):
            breaks_consistency = True
            for word_y in domains[y]:
                if are_compatible(x_letter_positions, y_letter_positions, word_x, word_y):
                    breaks_consistency = False
                    break
            if breaks_consistency:
                domains[x].remove(word_x)
    return any_domain_is_empty(domains)


def are_compatible(x_letter_positions: range, y_letter_positions: range, word_x: str, word_y: str):
    possible_conflict_positions = list(set(x_letter_positions).intersection(y_letter_positions))

    for index in possible_conflict_positions:
        if word_x[x_letter_positions.index(index)] != word_y[y_letter_positions.index(index)]:
            return False
    return True


def delete_word(tiles: list, variable: str, length: int):
    index = int(variable[:-1])
    is_horizontal = variable[-1] == "h"

    for i in range(length):
        current_mark = get_matrix_element(tiles, index)
        if len(current_mark) == 1:
            set_matrix_element(tiles, index, False)
        else:
            set_matrix_element(tiles, index, current_mark[:-1])

        index = inc_matrix_index(tiles, index, is_horizontal)
    return


def add_word(tiles: list, variable: str, word: str):
    index = int(variable[:-1])
    is_horizontal = variable[-1] == "h"

    for char in word:
        current_mark = get_matrix_element(tiles, index)
        if not current_mark:
            set_matrix_element(tiles, index, char)
        else:
            append_to_matrix_element(tiles, index, char)

        index = inc_matrix_index(tiles, index, is_horizontal)
    return


def get_index_list(tiles: list, variables: dict, variable: str):
    width = len(tiles[0])
    start_index = int(variable[:-1])
    is_horizontal = variable[-1] == "h"

    if is_horizontal:
        return range(start_index, start_index + variables[variable])
    else:
        return range(start_index, start_index + width * variables[variable], width)


def get_matrix_element(tiles: list, index: int):
    width = len(tiles[0])
    return tiles[index // width][index % width]


def set_matrix_element(tiles: list, index: int, value):
    width = len(tiles[0])
    tiles[index // width][index % width] = value


def append_to_matrix_element(tiles: list, index: int, postfix):
    width = len(tiles[0])
    tiles[index // width][index % width] += postfix


def inc_matrix_index(tiles: list, index: int, is_horizontal_mode: bool):
    width = len(tiles[0])

    if is_horizontal_mode:
        index += 1
    else:
        index += width
    return index


def any_domain_is_empty(domains: dict):
    for domain in domains.values():
        if len(domain) == 0:
            return True
    return False
