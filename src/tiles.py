#!/usr/bin/env python3

from typing import Any, Callable
from enum import Enum


class Colours(Enum):
    WHITE = "white"
    BLACK = "black"
    GREEN = "green"


class Tile:
    """
    A tile in the game.
    """

    number: int
    colour: Colours

    def __init__(self, number: int, colour: Colours | str):
        # Sanity checks
        if number < 0 or number > 9:
            raise ValueError("Number must be between 0 and 9 inclusive")
        if isinstance(colour, str):
            colour = Colours(colour)
        if colour not in [Colours.WHITE, Colours.BLACK, Colours.GREEN]:
            raise ValueError("Colour must be white, black or green")

        self.number = number
        self.colour = colour

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Tile):
            return False

        return self.number == __value.number and self.colour == __value.colour

    def __repr__(self) -> str:
        return f"Tile({self.number}, {self.colour})"

    @staticmethod
    def sorting_func(t: 'Tile') -> int:
        """
        Sorting function for tiles.
        Tiles should be ordered lowest to highest, with White tiles before
        black tiles.

        Returns:
            str: A unique value for the tile.
        """

        res = t.number * 10
        if t.colour == Colours.BLACK:
            res += 1

        return res


class Query:
    description: str

    def __init__(self, description: str):
        self.description = description

    def __repr__(self) -> str:
        return self.description

    def answer(self, tiles: list[Tile]) -> Any:
        """
        NOTE: This method is only here to allow for a "computer" player.
        A major part of the game is to have the player figure out the answer
        to the query questions themselves.
        """

        raise NotImplementedError(
            "This method must be implemented by the subclass"
        )


class SumQuery(Query):
    """
    Query for a sum of the numbers on the tiles.
    """

    def __init__(
        self,
        location: str,
        subset_func: Callable[[list[Tile]], list[Tile]],
    ):
        """
        A query that asks for the sum of the numbers on the tiles.

        args:
            location (str): The description of the location of the tiles.
            subset_func (function): A function which returns the subset of
                tiles to sum.
        """
        super().__init__(
            f"What is the sum of the {location} tiles?"
        )
        self.subset_func = subset_func

    def answer(self, tiles: list[Tile]) -> int:
        """
        Answer the sum of the numbers on the tiles.

        Returns:
            int: The sum of the numbers on the tiles.
        """

        return sum([
            t.number
            for t in self.subset_func(tiles)
        ])


class CountQuery(Query):
    """
    Query for the number of tiles which match a feature (number or colour).
    """

    def __init__(
        self,
        feature: str,
        truthy_func: Callable[[Tile], bool],
    ):
        """
        A query that asks for the count of the tiles.

        args:
            feature (str): The description of the feature of the tiles.
            subset_func (function): A function which determines if a tile has
                the feature.
        """
        super().__init__(
            f"How many {feature} tiles are there?"
        )
        self.truthy_func = truthy_func

    def answer(self, tiles: list[Tile]) -> int:
        """
        Answer the count of the tiles.

        Returns:
            int: The number of tiles which match the feature.
        """

        return [
            self.truthy_func(t)
            for t in tiles
        ].count(True)


class AdjacencyQuery(Query):
    """
    Query for which adjacent tiles are related.
    """

    def __init__(
        self,
        feature: str,
        truthy_func: Callable[[Tile, Tile], bool],
    ):
        """
        A query that asks which adjacent tiles are related in some way.

        args:
            feature (str): The description of the feature of the tiles.
            subset_func (function): A function which determines if two
                adjacent tiles are related.
        """
        super().__init__(
            f"Which adjacent tiles are {feature}?"
        )
        self.truthy_func = truthy_func

    def answer(self, tiles: list[Tile]) -> list[int]:
        """
        Answer which adjacent tiles are related.

        Returns:
            list[int]: A list of the indices of the adjacent tiles that are
                related.
        """

        ret = set()
        for i in range(len(tiles) - 1):
            if self.truthy_func(tiles[i], tiles[i + 1]):
                ret.add(i)
                ret.add(i + 1)

        return list(ret)


def clue_factory() -> list[Query]:
    """
    Factory function for creating the queries for the game.
    Always returns the same queries for the same number of players.

    returns:
        list[Query]: The queries for the game.
    """

    queries = [
        # Sum Queries
        SumQuery(
            "white",
            lambda tiles: [t for t in tiles if t.colour == Colours.WHITE]
        ),
        SumQuery(
            "black",
            lambda tiles: [t for t in tiles if t.colour == Colours.BLACK]
        ),
        SumQuery(
            "green",
            lambda tiles: [t for t in tiles if t.colour == Colours.GREEN]
        ),
        SumQuery(
            "right",
            lambda tiles: reversed(tiles[-1:-4:-1])
        ),
        SumQuery(
            "left",
            lambda tiles: tiles[:3]
        ),

        # Count Queries
        CountQuery(
            "even",
            lambda t: t.number % 2 == 0
        ),
        CountQuery(
            "odd",
            lambda t: t.number % 2 == 1
        ),
        CountQuery(
            "white",
            lambda t: t.colour == Colours.WHITE
        ),
        CountQuery(
            "black",
            lambda t: t.colour == Colours.BLACK
        ),
        CountQuery(
            "greater than 5",
            lambda t: t.number > 5
        ),
        CountQuery(
            "less than 5",
            lambda t: t.number < 5
        ),

        # Adjacency Queries
        AdjacencyQuery(
            "the same colour",
            lambda t1, t2: t1.colour == t2.colour
        ),
        AdjacencyQuery(
            "sequential",
            lambda t1, t2: t1.number + 1 == t2.number
        )
    ]

    return queries
