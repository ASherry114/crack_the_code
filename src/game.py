#!/usr/bin/env python3

"""
Crack the code board game.
"""

from random import shuffle
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


class Player:
    """
    A player in the game.
    """

    tiles: list[Tile]
    made_guess: bool
    guessed_correctly: bool

    def __init__(self, tiles: list[Tile] = []):
        self.tiles = tiles
        self.made_guess = False
        self.guessed_correctly = False


class Game:
    """
    Crack the code game class.
    Tracks the state of the game and handles the game logic.

    Each player collects numbers which are then arranged in a specific order.
    The players must ask and answer questions to figure out what numbers the
    other players have taken, and then deduce the remaining numbers to win the
    game.
    """

    players: dict[str]
    solution: list[Tile]

    def __init__(self):
        self.players = {}
        self.solution = []

    def new_game(self, num_players: int) -> list[str]:
        """
        Start a new game.
        The number of players determines how the game is played / what the
        rules are.
        This will create a new game state with new tiles.

        Args:
            num_players (int): The number of players in the game.

        Returns:
            list[str]: The unique IDs of the players in the game.

        Raises:
            ValueError: If the number of players is not between 2 and 4
                inclusive.
        """

        # Sanity checks
        if num_players < 2 or num_players > 4:
            raise ValueError(
                "Number of players must be between 2 and 4 inclusive"
            )
        if num_players == 2:
            raise NotImplementedError(
                "2 player games are not supported at the moment"
            )

        # Wipe any existing state
        self.solution = []
        self.players = {}

        # Enumerate the tiles
        game_tiles = []
        for i in range(10):
            # The 2 number 5 tiles are green, the rest are white and black
            if i != 5:
                tile_pair = [
                    Tile(i, Colours.WHITE),
                    Tile(i, Colours.BLACK)
                ]
            else:
                tile_pair = [
                    Tile(i, Colours.GREEN),
                    Tile(i, Colours.GREEN)
                ]

            game_tiles.extend(tile_pair)

        # Shuffle tiles and split into player sets
        # 2 players = 5 tiles
        # 3 players = 5 tiles
        # 4 players = 4 tiles
        shuffle(game_tiles)
        num_tiles_pp = 5 if num_players < 4 else 4
        split_tiles = [
            game_tiles[i*num_tiles_pp:(i+1)*num_tiles_pp]
            for i in range(num_players + 1)
        ]
        self.solution = sorted(split_tiles.pop(0), key=Tile.sorting_func)
        for i, tiles in enumerate(split_tiles):
            self.players[f"token{i}"] = Player(
                sorted(tiles, key=Tile.sorting_func)
            )

        # Return player IDs
        return list(self.players.keys())

    def get_character_tiles(self, player_id: str) -> list[Tile]:
        """
        Get the character tiles for a player.

        Args:
            player_id (str): The unique ID of the player.

        Returns:
            list[int]: The character tiles for the player.

        Raises:
            ValueError: If the player ID is invalid.
        """

        # Sanity checks
        if player_id not in self.players:
            raise ValueError("Player ID is invalid")

        # Return character tiles
        return self.players[player_id].tiles

    def submit_solution(self, player_id: str, submission: list[Tile]) -> None:
        """
        Attempt to submit a solution to the game.
        NOTE: The order must be provided correctly too.

        Args:
            submission (list[int]): The submission of tiles.

        Raises:
            ValueError: If the player ID is invalid.
            ValueError: If the player can't submit.
        """

        # Sanity checks
        if player_id not in self.players:
            raise ValueError("Player ID is invalid")
        if self.players[player_id].made_guess:
            raise ValueError("Player has already submitted a guess")

        # Check the submission
        # Trivial check as tiles always in order
        self.players[player_id].made_guess = True
        if submission == self.solution:
            self.players[player_id].guessed_correctly = True

    def get_winners(self) -> list[str]:
        """
        Get the winners of the game.

        Returns:
            list[str]: The unique IDs of the winners.
        """

        return [
            player_id
            for player_id, player in self.players.items()
            if player.guessed_correctly
        ]
