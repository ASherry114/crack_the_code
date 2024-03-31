#!/usr/bin/env python3

"""
Crack the code board game.
"""

from random import shuffle

from src.tiles import clue_factory, Colours, Tile


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
    backlog_queries: list[str]
    current_queries: list[str]

    def __init__(self):
        self.players = {}
        self.solution = []
        self.backlog_queries = []
        self.current_queries = []

    def new_game(self, num_players: int) -> list[str]:
        """
        Start a new game.
        The number of players determines how the game is played / what the
        rules are.
        This will create a new game state with new tiles.
        The clues in the file is what the players use to determine the
        solution.

        Args:
            num_players (int): The number of players in the game.

        Returns:
            list[str]: The unique IDs of the players in the game.

        Raises:
            ValueError: If the number of players is not between 2 and 4
                inclusive.
            ValueError: If the clues file is invalid.
        """

        # Wipe any existing state
        self.solution = []
        self.players = {}
        self.backlog_queries = []
        self.current_queries = []

        # Sanity checks
        if num_players < 2 or num_players > 4:
            raise ValueError(
                "Number of players must be between 2 and 4 inclusive"
            )
        if num_players == 2:
            raise NotImplementedError(
                "2 player games are not supported at the moment"
            )

        # Load the clues
        self.backlog_queries = clue_factory()
        shuffle(self.backlog_queries)
        self.current_queries = [
            self.backlog_queries.pop(0)
            for _ in range(min(6, len(self.backlog_queries)))
        ]

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

    def expend_query(self, idx: int) -> None:
        """
        Expend a query from the current list of queries and obtain a new one.

        Args:
            idx (int): The index of the query to expend.

        Raises:
            ValueError: If the index is invalid.
        """

        # Sanity checks
        if idx < 0 or idx >= len(self.current_queries):
            raise ValueError("Index is invalid")

        # Replace the clue
        if len(self.backlog_queries) > 0:
            self.current_queries[idx] = self.backlog_queries.pop(0)
        else:
            self.current_queries.pop(idx)
