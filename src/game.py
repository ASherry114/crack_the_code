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


class Game:
    """
    Crack the code game class.
    Tracks the state of the game and handles the game logic.

    Each player collects numbers which are then arranged in a specific order.
    The players must ask and answer questions to figure out what numbers the
    other players have taken, and then deduce the remaining numbers to win the
    game.
    """

    def __init__(self):
        self.players = {}
        self.tiles = []

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
        self.tiles = []
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
        self.tiles = split_tiles.pop(0)  # The "solution"
        for i, tiles in enumerate(split_tiles):
            self.players[f"token{i}"] = tiles

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

        # Return character tiles
