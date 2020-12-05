from constants import START_RANGE, END_RANGE, COLORS


class Tile(object):
    """
    A single tile in the game.
    """

    def __init__(self, number: int, color: str):
        assert START_RANGE <= number <= END_RANGE, \
            f"Number isn't in range ({START_RANGE - END_RANGE})."
        assert color in COLORS, "Invalid color."
        self.number = number
        self.color = color

    def __repr__(self):
        return f'Tile({self.number}, {self.color})'
        # return f'({self.number} {self.color})'

    def __eq__(self, other):
        """ Override the default == operator """
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self):
        return hash(str(self))
