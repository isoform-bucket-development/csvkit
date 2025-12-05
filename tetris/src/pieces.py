"""
Tetris piece definitions and piece generator.

This module defines all seven standard tetromino shapes and provides
a random piece generator with proper spawn positioning.
"""
import random
from enum import Enum
from typing import List, Tuple


class PieceType(Enum):
    """Enumeration of all seven standard tetromino types."""
    I = "I"
    O = "O"
    T = "T"
    S = "S"
    Z = "Z"
    J = "J"
    L = "L"


# Shape definitions for each piece type
# Each shape is defined as a list of (row, col) offsets from the piece's origin
# Shapes are defined in their spawn orientation
PIECE_SHAPES = {
    PieceType.I: [
        (0, 0), (0, 1), (0, 2), (0, 3)  # Horizontal I-piece: ████
    ],
    PieceType.O: [
        (0, 0), (0, 1),  # ██
        (1, 0), (1, 1)   # ██
    ],
    PieceType.T: [
        (0, 0), (0, 1), (0, 2),  # ███
        (1, 1)                    #  █
    ],
    PieceType.S: [
        (0, 1), (0, 2),  #  ██
        (1, 0), (1, 1)   # ██
    ],
    PieceType.Z: [
        (0, 0), (0, 1),  # ██
        (1, 1), (1, 2)   #  ██
    ],
    PieceType.J: [
        (0, 0),          # █
        (1, 0), (1, 1), (1, 2)  # ███
    ],
    PieceType.L: [
        (0, 2),          #   █
        (1, 0), (1, 1), (1, 2)  # ███
    ],
}

# Colors for each piece type (as defined in PRD)
PIECE_COLORS = {
    PieceType.I: "cyan",
    PieceType.O: "yellow",
    PieceType.T: "purple",
    PieceType.S: "green",
    PieceType.Z: "red",
    PieceType.J: "blue",
    PieceType.L: "orange",
}

# Board dimensions (standard Tetris)
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Spawn column - pieces spawn horizontally centered (columns 3-6 for most pieces)
# For a 10-column board, center is around column 3-4 (0-indexed)
# The spawn position puts pieces so they appear in columns 4-5 (1-indexed) which is 3-4 (0-indexed)
SPAWN_COLUMN = 3
SPAWN_ROW = 0


class Piece:
    """
    Represents a tetromino piece with its type, position, and shape.
    """

    def __init__(self, piece_type: PieceType, row: int = SPAWN_ROW, col: int = SPAWN_COLUMN):
        """
        Initialize a new piece.

        Args:
            piece_type: The type of tetromino (I, O, T, S, Z, J, L)
            row: Starting row position (default: top of board)
            col: Starting column position (default: center of board)
        """
        self.piece_type = piece_type
        self.row = row
        self.col = col
        self.rotation = 0  # 0, 1, 2, or 3 (0, 90, 180, 270 degrees)

    @property
    def shape(self) -> List[Tuple[int, int]]:
        """Get the shape blocks for this piece type."""
        return PIECE_SHAPES[self.piece_type]

    @property
    def color(self) -> str:
        """Get the color for this piece type."""
        return PIECE_COLORS[self.piece_type]

    def get_blocks(self) -> List[Tuple[int, int]]:
        """
        Get the absolute board positions of all blocks in this piece.

        Returns:
            List of (row, col) tuples representing board positions
        """
        return [(self.row + dr, self.col + dc) for dr, dc in self.shape]

    def get_occupied_columns(self) -> List[int]:
        """
        Get the columns occupied by this piece.

        Returns:
            List of column indices occupied by this piece
        """
        return sorted(set(col for _, col in self.get_blocks()))


class PieceGenerator:
    """
    Generates random tetromino pieces.

    Implements random piece generation as specified in REQ-3.
    """

    def __init__(self, seed: int = None):
        """
        Initialize the piece generator.

        Args:
            seed: Optional random seed for reproducible generation (useful for testing)
        """
        self._random = random.Random(seed)
        self._piece_types = list(PieceType)

    def generate(self) -> Piece:
        """
        Generate a new random tetromino piece.

        The piece is spawned at the top center of the board.

        Returns:
            A new Piece instance with a random type
        """
        piece_type = self._random.choice(self._piece_types)
        return Piece(piece_type, row=SPAWN_ROW, col=SPAWN_COLUMN)

    def generate_type(self) -> PieceType:
        """
        Generate a random piece type without creating a full Piece object.

        Returns:
            A random PieceType
        """
        return self._random.choice(self._piece_types)

    @staticmethod
    def get_all_piece_types() -> List[PieceType]:
        """
        Get all valid piece types.

        Returns:
            List of all PieceType values
        """
        return list(PieceType)

    @staticmethod
    def is_valid_piece_type(piece_type: PieceType) -> bool:
        """
        Check if a piece type is valid.

        Args:
            piece_type: The piece type to validate

        Returns:
            True if the piece type is one of the 7 valid types
        """
        return piece_type in PieceType
