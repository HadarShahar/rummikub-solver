from tile import Tile
from constants import MIN_LEN


class Run(object):
    """
    A run is composed of three or more, same-colored tiles, in consecutive number order.
    For example: red 1, red 2, red 3
    """

    def __init__(self, color: str, numbers: list):
        self.color = color
        self.numbers = sorted(numbers)

    def can_add(self, tile: Tile) -> bool:
        return tile.color == self.color and \
            (tile.number == self.numbers[0] -
             1 or tile.number == self.numbers[-1] + 1)

    def add(self, tile: Tile):
        if tile.number == self.numbers[0] - 1:
            self.numbers.insert(0, tile.number)
        elif tile.number == self.numbers[-1] + 1:
            self.numbers.append(tile.number)

    def get_tiles(self) -> list:
        return [Tile(num, self.color) for num in self.numbers]

    def __repr__(self):
        return f'Run({self.color}, [{", ".join(str(n) for n in self.numbers)}])'
        # return ', '.join([repr(tile) for tile in self.get_tiles()])

    @staticmethod
    def is_valid(tiles: list) -> bool:
        if len(tiles) < MIN_LEN:
            return False
        colors = [tile.color for tile in tiles]
        if len(set(colors)) != 1:  # all the colors should be equal
            return False
        numbers = sorted([tile.number for tile in tiles])
        for i in range(1, len(numbers)):
            if numbers[i] - numbers[i - 1] != 1:  # the numbers should be in consecutive order
                return False
        return True
