from collections import Counter
import copy
from tile import Tile
from run import Run
from group import Group
from constants import *


def nCr(lst: list, k: int) -> list:
    """
    returns a list with all the combinations of binomial coefficient (nCr)
    for example:
    :param lst: [1, 2, 3]
    :param k: 2
    :return: [[1, 2], [1, 3], [2, 3]]
    """
    if k <= 1:
        return [[n] for n in lst]
    combinations = []
    for i, num in enumerate(lst):
        for comb in nCr(lst[i + 1:], k - 1):
            combinations.append([num] + comb)
    return combinations


def lists_difference(lst1: list, lst2: list) -> list:
    """
    returns a list with all the items that
    exists in lst1 and don't exist in lst2.
    works for duplicates as well.
    for example:
    :param lst1: [1, 1, 2, 3]
    :param lst2: [1, 2]
    :return: [1, 3]
    """
    c1 = Counter(lst1)
    c1.subtract(Counter(lst2))
    return list(c1.elements())


def get_possible_series(original_numbers: list, target_num: int) -> list:
    """
    given a sorted list of numbers returns a list with all the valid rummikub series
    that contain the target_num and their length is at least MIN_LEN

    for example:
    :param original_numbers: [[1, 2, 4, 5, 6, 7, 10]
    :param target_num: 5
    :return: [[4, 5, 6], [5, 6, 7], [4, 5, 6, 7]]
    """
    try:
        index = original_numbers.index(target_num)
        # create a new list - numbers, with all the numbers that can be in a series with target_num
        numbers = []
        for i in range(index, -1, -1):
            if i + 1 == len(original_numbers):  # if it's the last number in the list
                if original_numbers[i] == target_num:
                    numbers.insert(0, original_numbers[i])
                continue
            if original_numbers[i + 1] - original_numbers[i] == 1:
                numbers.insert(0, original_numbers[i])
            else:
                break
        for i in range(index + 1, len(original_numbers)):
            if original_numbers[i] - original_numbers[i - 1] == 1:
                numbers.append(original_numbers[i])
            else:
                break

        # TODO better algorithm
        index = numbers.index(target_num)
        series_list = []
        # for i in range(max(index+1, len(lst)-index)):
        for i in range(len(numbers)):
            dist = MIN_LEN + i  # distance from the index of num in the list
            start = max(0, index + 1 - dist)
            # end = index + dist
            # print(start, end)
            for j in range(start, index + 1):
                series = numbers[j: j + dist]
                if len(series) == dist:
                    series_list.append(series)
        #             print(series)
        #         else:
        #             print('skip')
        #     print('='*40)
        # print(series_list)
        return series_list
        # first_half = numbers[:index + 1]
        # second_half = numbers[index:]
        # print(first_half, second_half)
        # print()
        # first_half_series = []
        # for i in range(len(first_half) - MIN_LEN + 1):
        #     series = first_half[i:]
        #     print(series)
        #     first_half_series.append(series)
        # print()
        # second_half_series = []
        # for i in range(len(second_half) - MIN_LEN + 1, len(second_half) + 1):
        #     series = second_half[:i]
        #     print(series)
        #     second_half_series.append(series)
        # print()
        # for s1 in first_half_series:
        #     for s2 in second_half_series:
        #         print(s1 + s2[1:])
    except ValueError:
        return []


def possible_sets(target: Tile, free_tiles: list) -> list:
    print('target:', target)
    print('free_tiles:', free_tiles)
    all_tiles = free_tiles + [target]
    sets = []

    ###################################################################################################
    # add all the possible Groups sets that contains the target tile

    same_num_tiles = list(filter(lambda tile: tile.number == target.number and
                                 tile.color != target.color, free_tiles))
    same_num_tiles = list(set(same_num_tiles))  # remove duplicates
    # other_tiles = lists_difference(free_tiles, same_num_tiles)
    same_num_colors = [t.color for t in same_num_tiles]  # keep just the colors

    # same_num_colors = []
    # other_tiles = []
    # for tile in tiles:
    #     if tile.number == target.number and tile.color != target.color and \
    #             tile.color not in same_num_colors:
    #         same_num_colors.append(tile.color)
    #     else:
    #         other_tiles.append(tile)

    combs = nCr(same_num_colors, MIN_LEN - 1)

    if len(same_num_colors) == MIN_LEN:
        combs.append(same_num_colors)

    for comb in combs:
        group = Group(target.number, [target.color] + comb)
        other_tiles = lists_difference(all_tiles, group.get_tiles())
        sets.append(([group], other_tiles))
    ###################################################################################################
    # add all the possible Run sets that contains the target tile

    same_color_tiles = list(filter(lambda t: t.color == target.color and
                                   t.number != target.number, free_tiles))
    same_color_tiles = list(set(same_color_tiles))  # remove duplicates
    same_color_numbers = sorted(
        [target.number] + [t.number for t in same_color_tiles])  # keep just the numbers

    # add all the series with the minimum length that contains the target number
    # for i in range(0, len(same_color_numbers) - MIN_LEN + 1):
    #     series = same_color_numbers[i: i + MIN_LEN]
    #     numbers_diff = [series[j + 1] - series[j] for j in range(len(series) - 1)]
    #     if set(numbers_diff) == {1}:  # all te differences should be 1
    #         run = Run(target.color, series)
    #         other_tiles = lists_difference(all_tiles, run.get_tiles())
    #         sets.append(([run], other_tiles))

    # add all the possible series that contains the target number
    for series in get_possible_series(same_color_numbers, target.number):
        run = Run(target.color, series)
        other_tiles = lists_difference(all_tiles, run.get_tiles())
        sets.append(([run], other_tiles))

    if len(sets) == 0:
        sets.append(([], all_tiles))

    return sets


def rearrange(tiles: list) -> list:
    sets = possible_sets(tiles[0], tiles[1:])
    print('=' * 150)
    print('sets:')
    for s, other_tiles in sets:
        if len(s) == 0 or len(other_tiles) == 0:
            return s

        print(f'{s}{" " * (50 - len(str(s)))}{other_tiles}')
        arrangement = rearrange(other_tiles)
        if len(arrangement) != 0:
            return [s] + arrangement
    return []


def main():
    board = [
        Run(BLUE, [7, 8, 9, 10]),
        Group(11, [BLACK, BLUE, RED, ORANGE]),
        Run(BLACK, [7, 8, 9, 10, 11, 12]),
        Group(7, [BLACK, RED, ORANGE])
    ]
    # target_tile = Tile(9, BLUE)
    # tiles = [target_tile]

    tiles = [Tile(6, BLACK), Tile(10, BLACK)]
    for s in board:
        tiles += s.get_tiles()

    # for s in board:
    #     print(s)

    tiles_copy = copy.deepcopy(tiles)
    tiles_copy = rearrange(tiles_copy)
    print('*'*100)
    print('*'*100)
    print('*'*100)
    print(tiles_copy)

    # for s in board:
    #     if s.can_add(target_tile):
    #         s.add(target_tile)
    #         print('added')


if __name__ == '__main__':
    main()
    # tiles = [Tile(10, BLUE), Tile(11, BLACK), Tile(11, BLUE), Tile(11, ORANGE), Tile(11, RED), Tile(9, ORANGE)]
    # rearrange(tiles)
