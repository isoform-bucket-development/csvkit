/**
 * Tetromino shapes module for Tetris game
 * Implements all seven standard tetromino shapes per REQ-2
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

// List of all tetromino types
const TETROMINO_TYPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];

/**
 * Tetromino class representing a single tetromino piece
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
    this.shape = TETROMINO_SHAPES[type].map(cell => [...cell]); // Deep copy
  }

  /**
   * Get the cells of this tetromino
   * @returns {Array<Array<number>>} Array of [row, col] positions
   */
  getCells() {
    return this.shape.map(cell => [...cell]);
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
    TETROMINO_SHAPES
  };
}
