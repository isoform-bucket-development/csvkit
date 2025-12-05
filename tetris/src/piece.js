/**
 * Piece Module - Active Tetromino Management
 *
 * This module handles the active falling tetromino, including:
 * - Position tracking (row, column)
 * - Horizontal movement (left/right) per REQ-4
 * - Collision detection per REQ-16
 * - Input handling for keyboard controls
 */

const { BOARD_WIDTH, BOARD_HEIGHT, EMPTY_CELL } = require('./gameBoard');

/**
 * Control key mappings per PRD specifications
 * Move Left: Left Arrow or A
 * Move Right: Right Arrow or D
 */
const CONTROLS = {
  LEFT: ['ArrowLeft', 'a', 'A'],
  RIGHT: ['ArrowRight', 'd', 'D'],
  ROTATE: ['ArrowUp', 'w', 'W'],
  SOFT_DROP: ['ArrowDown', 's', 'S'],
  HARD_DROP: [' ', 'Space']
};

/**
 * ActivePiece class represents the currently falling tetromino
 * Handles position, movement, and collision detection
 */
class ActivePiece {
  /**
   * Create a new active piece
   * @param {Tetromino} tetromino - The tetromino shape
   * @param {GameBoard} board - The game board for collision detection
   * @param {number} row - Initial row position (default: 0)
   * @param {number} col - Initial column position (default: 3, centered)
   */
  constructor(tetromino, board, row = 0, col = 3) {
    this.tetromino = tetromino;
    this.board = board;
    this.row = row;
    this.col = col;
  }

  /**
   * Get the current row position
   * @returns {number} Current row
   */
  getRow() {
    return this.row;
  }

  /**
   * Get the current column position
   * @returns {number} Current column
   */
  getColumn() {
    return this.col;
  }

  /**
   * Get the tetromino shape
   * @returns {Tetromino} The tetromino
   */
  getTetromino() {
    return this.tetromino;
  }

  /**
   * Get the absolute cell positions on the board
   * @returns {Array<Array<number>>} Array of [row, col] positions
   */
  getAbsoluteCells() {
    const cells = this.tetromino.getCells();
    return cells.map(([relRow, relCol]) => [
      this.row + relRow,
      this.col + relCol
    ]);
  }

  /**
   * Check if a position is valid (no collision)
   * @param {number} newRow - Row to check
   * @param {number} newCol - Column to check
   * @returns {boolean} True if position is valid
   */
  canMoveTo(newRow, newCol) {
    const cells = this.tetromino.getCells();

    for (const [relRow, relCol] of cells) {
      const absRow = newRow + relRow;
      const absCol = newCol + relCol;

      // Check left boundary
      if (absCol < 0) {
        return false;
      }

      // Check right boundary
      if (absCol >= BOARD_WIDTH) {
        return false;
      }

      // Check bottom boundary
      if (absRow >= BOARD_HEIGHT) {
        return false;
      }

      // Check collision with placed pieces (only if row is visible)
      if (absRow >= 0 && !this.board.isCellEmpty(absRow, absCol)) {
        return false;
      }
    }

    return true;
  }

  /**
   * Move the piece left by one column
   * Per REQ-4: Allow player to move tetrominoes left
   * @returns {boolean} True if move was successful
   */
  moveLeft() {
    const newCol = this.col - 1;

    if (this.canMoveTo(this.row, newCol)) {
      this.col = newCol;
      return true;
    }

    return false;
  }

  /**
   * Move the piece right by one column
   * Per REQ-4: Allow player to move tetrominoes right
   * @returns {boolean} True if move was successful
   */
  moveRight() {
    const newCol = this.col + 1;

    if (this.canMoveTo(this.row, newCol)) {
      this.col = newCol;
      return true;
    }

    return false;
  }

  /**
   * Move the piece down by one row (soft drop step)
   * @returns {boolean} True if move was successful
   */
  moveDown() {
    const newRow = this.row + 1;

    if (this.canMoveTo(newRow, this.col)) {
      this.row = newRow;
      return true;
    }

    return false;
  }

  /**
   * Check if the piece can move down (not locked)
   * @returns {boolean} True if piece can move down
   */
  canMoveDown() {
    return this.canMoveTo(this.row + 1, this.col);
  }
}

/**
 * InputHandler class handles keyboard input for piece movement
 * Implements controls per PRD User Interaction Patterns
 */
class InputHandler {
  /**
   * Create an input handler for the active piece
   * @param {ActivePiece} activePiece - The piece to control
   */
  constructor(activePiece) {
    this.activePiece = activePiece;
  }

  /**
   * Set the active piece to control
   * @param {ActivePiece} activePiece - The new active piece
   */
  setActivePiece(activePiece) {
    this.activePiece = activePiece;
  }

  /**
   * Handle keydown events
   * @param {KeyboardEvent|Object} event - The keyboard event
   * @returns {boolean} True if the event was handled
   */
  handleKeyDown(event) {
    if (!this.activePiece) {
      return false;
    }

    const key = event.key;

    // Left movement (Arrow Left or A)
    if (CONTROLS.LEFT.includes(key)) {
      return this.activePiece.moveLeft();
    }

    // Right movement (Arrow Right or D)
    if (CONTROLS.RIGHT.includes(key)) {
      return this.activePiece.moveRight();
    }

    return false;
  }
}

module.exports = {
  ActivePiece,
  InputHandler,
  CONTROLS
};
