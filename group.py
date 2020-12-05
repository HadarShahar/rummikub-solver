from tile import Tile
from constants import MIN_LEN


class Group(object):
    """
    A group is made from three or four same-value tiles in distinct colors.
    For example: red 3, blue 3, black 3
    """

    def __init__(self, number: int, colors: list):
        self.number = number
        self.colors = sorted(colors)

    def can_add(self, tile: Tile) -> bool:
        return tile.number == self.number and tile.color not in self.colors

    def add(self, tile: Tile):
        self.colors.append(tile.color)

    def get_tiles(self) -> list:
        return [Tile(self.number, color) for color in self.colors]

    def __repr__(self):
        return f'Group({self.number}, [{", ".join(self.colors)}])'
        # return ', '.join([repr(tile) for tile in self.get_tiles()])

    @staticmethod
    def is_valid(tiles: list) -> bool:
        if len(tiles) < MIN_LEN:
            return False
        numbers = [tile.number for tile in tiles]
        if len(set(numbers)) != 1:  # all the numbers should be equal
            return False
        colors = [tile.color for tile in tiles]
        if len(set(colors)) != len(colors):  # all the colors should be unique
            return False
        return True
