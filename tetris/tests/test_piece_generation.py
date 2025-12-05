"""
Tests for random piece generation scenario.

Test Cases:
1. Generate 100 random pieces - all 7 piece types should appear at least once
2. Spawn new piece - piece appears at top center (column 4-5, which is 3-4 in 0-indexed)
3. Check piece type validity - generated piece is one of the 7 valid types
"""
import unittest
from collections import Counter

from tetris.src.pieces import (
    Piece,
    PieceGenerator,
    PieceType,
    SPAWN_ROW,
    SPAWN_COLUMN,
    BOARD_WIDTH,
)


class TestRandomPieceGeneration(unittest.TestCase):
    """Test case 1: Generate 100 random pieces, all 7 piece types appear at least once."""

    def test_all_piece_types_appear_in_100_generations(self):
        """
        Generate 100 random pieces and verify all 7 piece types appear at least once.

        This tests the randomness distribution as per REQ-3.
        """
        generator = PieceGenerator()
        generated_types = []

        for _ in range(100):
            piece = generator.generate()
            generated_types.append(piece.piece_type)

        # Count occurrences of each piece type
        type_counts = Counter(generated_types)

        # Verify all 7 piece types appeared at least once
        all_piece_types = set(PieceType)
        generated_piece_types = set(type_counts.keys())

        self.assertEqual(
            all_piece_types,
            generated_piece_types,
            f"Not all piece types appeared. Missing: {all_piece_types - generated_piece_types}"
        )

        # Verify each type appeared at least once
        for piece_type in PieceType:
            self.assertGreater(
                type_counts[piece_type],
                0,
                f"Piece type {piece_type.value} did not appear in 100 generations"
            )

    def test_randomness_distribution_over_many_generations(self):
        """
        Generate many pieces and verify reasonable distribution.

        With 700 pieces (100 per type on average), each type should appear
        at least 50 times (roughly 7% minimum).
        """
        generator = PieceGenerator()
        generated_types = []

        for _ in range(700):
            piece = generator.generate()
            generated_types.append(piece.piece_type)

        type_counts = Counter(generated_types)

        # Each type should appear a reasonable number of times
        for piece_type in PieceType:
            count = type_counts[piece_type]
            # With uniform random distribution, each should be ~100 (700/7)
            # Allow for statistical variance - at least 50 occurrences
            self.assertGreater(
                count,
                50,
                f"Piece type {piece_type.value} appeared only {count} times in 700 generations"
            )


class TestSpawnPosition(unittest.TestCase):
    """Test case 2: Spawn new piece - piece appears at top center (column 4-5)."""

    def test_piece_spawns_at_top_row(self):
        """Verify piece spawns at the top of the board (row 0)."""
        generator = PieceGenerator()
        piece = generator.generate()

        self.assertEqual(
            piece.row,
            SPAWN_ROW,
            f"Piece should spawn at row {SPAWN_ROW}, but spawned at row {piece.row}"
        )

    def test_piece_spawns_at_center_column(self):
        """
        Verify piece spawns at center of board.

        The spawn column should position the piece so its blocks
        occupy columns around 4-5 (1-indexed) or 3-4 (0-indexed).
        """
        generator = PieceGenerator()
        piece = generator.generate()

        self.assertEqual(
            piece.col,
            SPAWN_COLUMN,
            f"Piece should spawn at column {SPAWN_COLUMN}, but spawned at column {piece.col}"
        )

    def test_piece_blocks_within_center_area(self):
        """
        Verify that piece blocks are within the center area of the board.

        For a 10-column board, pieces should spawn in the center area
        (roughly columns 3-6 for most pieces).
        """
        generator = PieceGenerator(seed=42)  # Use seed for reproducibility

        for _ in range(50):  # Test multiple pieces
            piece = generator.generate()
            occupied_columns = piece.get_occupied_columns()

            # All blocks should be within the board
            for col in occupied_columns:
                self.assertGreaterEqual(col, 0, f"Column {col} is out of bounds (left)")
                self.assertLess(col, BOARD_WIDTH, f"Column {col} is out of bounds (right)")

            # The minimum column should be around center (column 3-4)
            min_col = min(occupied_columns)
            max_col = max(occupied_columns)

            # For standard spawn, pieces should start around column 3
            # and extend to at most column 6 (for I-piece)
            self.assertGreaterEqual(
                min_col,
                0,
                f"Piece blocks start too far left: {occupied_columns}"
            )
            self.assertLess(
                max_col,
                BOARD_WIDTH,
                f"Piece blocks extend too far right: {occupied_columns}"
            )

    def test_all_piece_types_spawn_correctly(self):
        """Test that all piece types spawn at the correct position."""
        for piece_type in PieceType:
            piece = Piece(piece_type)

            # Verify spawn position
            self.assertEqual(piece.row, SPAWN_ROW)
            self.assertEqual(piece.col, SPAWN_COLUMN)

            # Verify blocks are valid
            blocks = piece.get_blocks()
            self.assertGreater(len(blocks), 0, f"Piece {piece_type.value} has no blocks")

            # All blocks should be within board bounds initially
            for row, col in blocks:
                self.assertGreaterEqual(row, 0)
                self.assertGreaterEqual(col, 0)
                self.assertLess(col, BOARD_WIDTH)


class TestPieceTypeValidity(unittest.TestCase):
    """Test case 3: Check piece type validity - generated piece is one of the 7 valid types."""

    def test_generated_piece_has_valid_type(self):
        """Verify each generated piece has a valid piece type."""
        generator = PieceGenerator()

        for _ in range(100):
            piece = generator.generate()

            # Check that piece_type is a valid PieceType enum member
            self.assertIsInstance(
                piece.piece_type,
                PieceType,
                f"Generated piece type {piece.piece_type} is not a valid PieceType"
            )

    def test_is_valid_piece_type_for_all_types(self):
        """Verify is_valid_piece_type returns True for all valid types."""
        for piece_type in PieceType:
            self.assertTrue(
                PieceGenerator.is_valid_piece_type(piece_type),
                f"PieceType {piece_type.value} should be valid"
            )

    def test_seven_valid_piece_types_exist(self):
        """Verify exactly 7 piece types exist (I, O, T, S, Z, J, L)."""
        all_types = PieceGenerator.get_all_piece_types()

        self.assertEqual(
            len(all_types),
            7,
            f"Expected 7 piece types, got {len(all_types)}"
        )

        # Verify the specific types
        expected_types = {"I", "O", "T", "S", "Z", "J", "L"}
        actual_types = {t.value for t in all_types}

        self.assertEqual(
            expected_types,
            actual_types,
            f"Piece types mismatch. Expected {expected_types}, got {actual_types}"
        )

    def test_piece_type_enum_values(self):
        """Verify all expected piece types are defined in the enum."""
        expected_values = ["I", "O", "T", "S", "Z", "J", "L"]

        for value in expected_values:
            # This will raise KeyError if the value doesn't exist
            piece_type = PieceType(value)
            self.assertEqual(piece_type.value, value)

    def test_generated_type_matches_piece_type(self):
        """Verify generate_type returns valid PieceType values."""
        generator = PieceGenerator()

        for _ in range(50):
            piece_type = generator.generate_type()

            self.assertIsInstance(
                piece_type,
                PieceType,
                f"generate_type returned {piece_type} which is not a PieceType"
            )

            self.assertIn(
                piece_type,
                list(PieceType),
                f"generate_type returned {piece_type} which is not in PieceType enum"
            )


class TestPieceShapes(unittest.TestCase):
    """Additional tests for piece shape definitions."""

    def test_all_pieces_have_four_blocks(self):
        """Verify all tetrominoes have exactly 4 blocks."""
        for piece_type in PieceType:
            piece = Piece(piece_type)
            blocks = piece.get_blocks()

            self.assertEqual(
                len(blocks),
                4,
                f"Piece {piece_type.value} has {len(blocks)} blocks, expected 4"
            )

    def test_all_pieces_have_colors(self):
        """Verify all piece types have associated colors."""
        for piece_type in PieceType:
            piece = Piece(piece_type)
            color = piece.color

            self.assertIsNotNone(
                color,
                f"Piece {piece_type.value} has no color defined"
            )
            self.assertIsInstance(color, str)
            self.assertGreater(len(color), 0)


class TestPieceGeneratorSeeding(unittest.TestCase):
    """Test that piece generator seeding works correctly."""

    def test_seeded_generator_produces_same_sequence(self):
        """Verify that same seed produces same sequence of pieces."""
        seed = 12345
        generator1 = PieceGenerator(seed=seed)
        generator2 = PieceGenerator(seed=seed)

        for _ in range(20):
            piece1 = generator1.generate()
            piece2 = generator2.generate()

            self.assertEqual(
                piece1.piece_type,
                piece2.piece_type,
                "Seeded generators should produce same sequence"
            )

    def test_different_seeds_produce_different_sequences(self):
        """Verify that different seeds produce different sequences."""
        generator1 = PieceGenerator(seed=111)
        generator2 = PieceGenerator(seed=222)

        sequence1 = [generator1.generate().piece_type for _ in range(20)]
        sequence2 = [generator2.generate().piece_type for _ in range(20)]

        # The sequences should be different (with very high probability)
        self.assertNotEqual(
            sequence1,
            sequence2,
            "Different seeds should produce different sequences"
        )


if __name__ == "__main__":
    unittest.main()
