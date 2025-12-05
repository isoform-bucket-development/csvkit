/**
 * Tetromino shapes module for Tetris game
 * Implements all seven standard tetromino shapes per REQ-2
 * Implements clockwise rotation per REQ-5
 */

// Standard tetromino colors
const TETROMINO_COLORS = {
  I: 'cyan',
  O: 'yellow',
  T: 'purple',
  S: 'green',
  Z: 'red',
  J: 'blue',
  L: 'orange'
};

// Tetromino shape definitions using relative cell positions
// Each shape is defined as an array of [row, col] offsets from origin
const TETROMINO_SHAPES = {
  // I-piece: 4 cells in horizontal line
  // ████
  I: [
    [0, 0], [0, 1], [0, 2], [0, 3]
  ],

  // O-piece: 2x2 square
  // ██
  // ██
  O: [
    [0, 0], [0, 1],
    [1, 0], [1, 1]
  ],

  // T-piece: T-shape
  // ███
  //  █
  T: [
    [0, 0], [0, 1], [0, 2],
    [1, 1]
  ],

  // S-piece: S-shaped zigzag
  //  ██
  // ██
  S: [
    [0, 1], [0, 2],
    [1, 0], [1, 1]
  ],

  // Z-piece: Z-shaped zigzag
  // ██
  //  ██
  Z: [
    [0, 0], [0, 1],
    [1, 1], [1, 2]
  ],

  // J-piece: J-shape
  // █
  // ███
  J: [
    [0, 0],
    [1, 0], [1, 1], [1, 2]
  ],

  // L-piece: L-shape
  //   █
  // ███
  L: [
    [0, 2],
    [1, 0], [1, 1], [1, 2]
  ]
};

/**
 * All rotation states for each tetromino type.
 * Each piece has 4 rotation states (0, 1, 2, 3) representing 0, 90, 180, 270 degrees clockwise.
 * O-piece appears the same in all rotations due to square symmetry.
 */
const ROTATION_STATES = {
  // I-piece rotations
  I: [
    // State 0: Horizontal ████
    [[0, 0], [0, 1], [0, 2], [0, 3]],
    // State 1: Vertical (rotated 90° clockwise)
    [[0, 1], [1, 1], [2, 1], [3, 1]],
    // State 2: Horizontal (rotated 180°)
    [[1, 0], [1, 1], [1, 2], [1, 3]],
    // State 3: Vertical (rotated 270°)
    [[0, 2], [1, 2], [2, 2], [3, 2]]
  ],

  // O-piece: All rotations are identical (square symmetry)
  O: [
    [[0, 0], [0, 1], [1, 0], [1, 1]],
    [[0, 0], [0, 1], [1, 0], [1, 1]],
    [[0, 0], [0, 1], [1, 0], [1, 1]],
    [[0, 0], [0, 1], [1, 0], [1, 1]]
  ],

  // T-piece rotations
  T: [
    // State 0: ███ / █
    [[0, 0], [0, 1], [0, 2], [1, 1]],
    // State 1: █ / ██ / █
    [[0, 1], [1, 0], [1, 1], [2, 1]],
    // State 2:  █ / ███
    [[1, 0], [1, 1], [1, 2], [0, 1]],
    // State 3: █ / ██ / █
    [[0, 0], [1, 0], [1, 1], [2, 0]]
  ],

  // S-piece rotations (2 visually distinct states that cycle)
  S: [
    // State 0:  ██ / ██
    [[0, 1], [0, 2], [1, 0], [1, 1]],
    // State 1: █ / ██ /  █
    [[0, 0], [1, 0], [1, 1], [2, 1]],
    // State 2:  ██ / ██ (shifted down)
    [[1, 1], [1, 2], [2, 0], [2, 1]],
    // State 3: █ / ██ /  █ (shifted right)
    [[0, 1], [1, 1], [1, 2], [2, 2]]
  ],

  // Z-piece rotations (2 visually distinct states that cycle)
  Z: [
    // State 0: ██ /  ██
    [[0, 0], [0, 1], [1, 1], [1, 2]],
    // State 1:  █ / ██ / █
    [[0, 1], [1, 0], [1, 1], [2, 0]],
    // State 2: ██ /  ██ (shifted down)
    [[1, 0], [1, 1], [2, 1], [2, 2]],
    // State 3:  █ / ██ / █ (shifted right)
    [[0, 2], [1, 1], [1, 2], [2, 1]]
  ],

  // J-piece rotations
  J: [
    // State 0: █ / ███
    [[0, 0], [1, 0], [1, 1], [1, 2]],
    // State 1: ██ / █ / █
    [[0, 0], [0, 1], [1, 0], [2, 0]],
    // State 2: ███ /   █
    [[0, 0], [0, 1], [0, 2], [1, 2]],
    // State 3:  █ /  █ / ██
    [[0, 1], [1, 1], [2, 0], [2, 1]]
  ],

  // L-piece rotations
  L: [
    // State 0:   █ / ███
    [[0, 2], [1, 0], [1, 1], [1, 2]],
    // State 1: █ / █ / ██
    [[0, 0], [1, 0], [2, 0], [2, 1]],
    // State 2: ███ / █
    [[0, 0], [0, 1], [0, 2], [1, 0]],
    // State 3: ██ /  █ /  █
    [[0, 0], [0, 1], [1, 1], [2, 1]]
  ]
};

// List of all tetromino types
const TETROMINO_TYPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];

/**
 * Tetromino class representing a single tetromino piece
 * Supports rotation per REQ-5 and collision detection per REQ-16
 */
class Tetromino {
  /**
   * Create a new tetromino
   * @param {string} type - The type of tetromino (I, O, T, S, Z, J, L)
   */
  constructor(type) {
    if (!TETROMINO_TYPES.includes(type)) {
      throw new Error(`Invalid tetromino type: ${type}`);
    }
    this.type = type;
    this.color = TETROMINO_COLORS[type];
    this.rotationState = 0; // 0, 1, 2, or 3 (0°, 90°, 180°, 270° clockwise)
    this.row = 0; // Board row position
    this.col = 0; // Board column position
    this._updateShape();
  }

  /**
   * Update the shape based on current rotation state
   * @private
   */
  _updateShape() {
    this.shape = ROTATION_STATES[this.type][this.rotationState].map(cell => [...cell]);
  }

  /**
   * Get the cells of this tetromino (relative positions)
   * @returns {Array<Array<number>>} Array of [row, col] positions relative to origin
   */
  getCells() {
    return this.shape.map(cell => [...cell]);
  }

  /**
   * Get the absolute board positions of all cells
   * @returns {Array<Array<number>>} Array of [row, col] absolute board positions
   */
  getAbsoluteCells() {
    return this.shape.map(([r, c]) => [this.row + r, this.col + c]);
  }

  /**
   * Get the color of this tetromino
   * @returns {string} The color name
   */
  getColor() {
    return this.color;
  }

  /**
   * Get the type of this tetromino
   * @returns {string} The tetromino type
   */
  getType() {
    return this.type;
  }

  /**
   * Get the number of cells in this tetromino
   * @returns {number} Number of cells
   */
  getCellCount() {
    return this.shape.length;
  }

  /**
   * Get the bounding box dimensions of this tetromino
   * @returns {{width: number, height: number}} Bounding box dimensions
   */
  getBoundingBox() {
    const rows = this.shape.map(cell => cell[0]);
    const cols = this.shape.map(cell => cell[1]);
    return {
      width: Math.max(...cols) - Math.min(...cols) + 1,
      height: Math.max(...rows) - Math.min(...rows) + 1
    };
  }

  /**
   * Get the current rotation state (0-3)
   * @returns {number} Current rotation state
   */
  getRotationState() {
    return this.rotationState;
  }

  /**
   * Set the position of this tetromino on the board
   * @param {number} row - Board row position
   * @param {number} col - Board column position
   */
  setPosition(row, col) {
    this.row = row;
    this.col = col;
  }

  /**
   * Get the current position of this tetromino
   * @returns {{row: number, col: number}} Current position
   */
  getPosition() {
    return { row: this.row, col: this.col };
  }

  /**
   * Rotate the tetromino clockwise by 90 degrees
   * This method always rotates - use canRotate() or tryRotate() for collision checking
   */
  rotateClockwise() {
    this.rotationState = (this.rotationState + 1) % 4;
    this._updateShape();
  }

  /**
   * Rotate the tetromino counter-clockwise by 90 degrees
   */
  rotateCounterClockwise() {
    this.rotationState = (this.rotationState + 3) % 4; // +3 is equivalent to -1 mod 4
    this._updateShape();
  }

  /**
   * Get the cells for the next clockwise rotation state (without modifying current state)
   * @returns {Array<Array<number>>} Array of [row, col] positions for next rotation
   */
  getNextRotationCells() {
    const nextState = (this.rotationState + 1) % 4;
    return ROTATION_STATES[this.type][nextState].map(cell => [...cell]);
  }

  /**
   * Get the absolute board positions for the next rotation state
   * @returns {Array<Array<number>>} Array of [row, col] absolute positions for next rotation
   */
  getNextRotationAbsoluteCells() {
    const nextCells = this.getNextRotationCells();
    return nextCells.map(([r, c]) => [this.row + r, this.col + c]);
  }

  /**
   * Check if the tetromino can rotate clockwise without collision
   * @param {Object} board - Game board with isValidPosition and isCellEmpty methods
   * @returns {boolean} True if rotation is valid
   */
  canRotate(board) {
    const nextCells = this.getNextRotationAbsoluteCells();

    for (const [row, col] of nextCells) {
      // Check board boundaries
      if (!board.isValidPosition(row, col)) {
        return false;
      }
      // Check for collision with existing pieces
      if (!board.isCellEmpty(row, col)) {
        return false;
      }
    }
    return true;
  }

  /**
   * Try to rotate clockwise, only succeeding if no collision occurs
   * @param {Object} board - Game board with collision detection methods
   * @returns {boolean} True if rotation succeeded, false if blocked
   */
  tryRotate(board) {
    if (this.canRotate(board)) {
      this.rotateClockwise();
      return true;
    }
    return false;
  }
}

/**
 * Factory function to create a tetromino by type
 * @param {string} type - The type of tetromino to create
 * @returns {Tetromino} A new tetromino instance
 */
function createTetromino(type) {
  return new Tetromino(type);
}

/**
 * Generate a random tetromino
 * @returns {Tetromino} A random tetromino instance
 */
function generateRandomTetromino() {
  const randomIndex = Math.floor(Math.random() * TETROMINO_TYPES.length);
  return new Tetromino(TETROMINO_TYPES[randomIndex]);
}

// Export for both CommonJS and ES modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    Tetromino,
    createTetromino,
    generateRandomTetromino,
    TETROMINO_TYPES,
    TETROMINO_COLORS,
    TETROMINO_SHAPES,
    ROTATION_STATES
  };
}
