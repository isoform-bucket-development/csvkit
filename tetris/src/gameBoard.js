/**
 * GameBoard - Tetris Game Board Implementation
 *
 * This module implements the game board for Tetris with standard dimensions
 * (10 columns x 20 rows) as specified in REQ-1.
 *
 * The board is represented as a 2D array where:
 * - Each cell can be empty (0) or contain a piece color value (1-7)
 * - Row 0 is the top of the board, Row 19 is the bottom
 * - Column 0 is the leftmost, Column 9 is the rightmost
 */

// Board Constants - Standard Tetris dimensions per REQ-1
const BOARD_WIDTH = 10;
const BOARD_HEIGHT = 20;
const EMPTY_CELL = 0;

// Rendering Constants
const DEFAULT_CELL_SIZE = 30; // pixels per cell
const GRID_LINE_COLOR = '#333333';
const BACKGROUND_COLOR = '#000000';
const BORDER_COLOR = '#666666';

/**
 * GameBoard class represents the Tetris playing field.
 * Handles board state management and rendering.
 */
class GameBoard {
  /**
   * Creates a new GameBoard instance with an empty grid.
   * @param {number} cellSize - Size of each cell in pixels (default: 30)
   */
  constructor(cellSize = DEFAULT_CELL_SIZE) {
    this.width = BOARD_WIDTH;
    this.height = BOARD_HEIGHT;
    this.cellSize = cellSize;
    this.grid = this._createEmptyGrid();
  }

  /**
   * Creates an empty 2D grid array filled with EMPTY_CELL values.
   * @returns {number[][]} Empty grid with dimensions BOARD_HEIGHT x BOARD_WIDTH
   * @private
   */
  _createEmptyGrid() {
    const grid = [];
    for (let row = 0; row < this.height; row++) {
      grid.push(new Array(this.width).fill(EMPTY_CELL));
    }
    return grid;
  }

  /**
   * Gets the width of the board in cells.
   * @returns {number} Board width (10)
   */
  getWidth() {
    return this.width;
  }

  /**
   * Gets the height of the board in cells.
   * @returns {number} Board height (20)
   */
  getHeight() {
    return this.height;
  }

  /**
   * Gets the cell size in pixels.
   * @returns {number} Cell size in pixels
   */
  getCellSize() {
    return this.cellSize;
  }

  /**
   * Gets the total board width in pixels.
   * @returns {number} Board width in pixels
   */
  getPixelWidth() {
    return this.width * this.cellSize;
  }

  /**
   * Gets the total board height in pixels.
   * @returns {number} Board height in pixels
   */
  getPixelHeight() {
    return this.height * this.cellSize;
  }

  /**
   * Returns a deep copy of the current grid state.
   * This prevents external code from directly mutating the internal grid.
   * @returns {number[][]} Copy of the grid
   */
  getGrid() {
    return this.grid.map(row => [...row]);
  }

  /**
   * Gets the value of a cell at the specified position.
   * @param {number} row - Row index (0-19)
   * @param {number} col - Column index (0-9)
   * @returns {number} Cell value (EMPTY_CELL or piece color)
   * @throws {Error} If position is out of bounds
   */
  getCellAt(row, col) {
    if (row < 0 || row >= this.height || col < 0 || col >= this.width) {
      throw new Error(`Position (${row}, ${col}) is out of bounds`);
    }
    return this.grid[row][col];
  }

  /**
   * Sets the value of a cell at the specified position.
   * @param {number} row - Row index (0-19)
   * @param {number} col - Column index (0-9)
   * @param {number} value - Cell value to set
   * @throws {Error} If position is out of bounds
   */
  setCellAt(row, col, value) {
    if (row < 0 || row >= this.height || col < 0 || col >= this.width) {
      throw new Error(`Position (${row}, ${col}) is out of bounds`);
    }
    this.grid[row][col] = value;
  }

  /**
   * Checks if the entire board is empty (no pieces placed).
   * @returns {boolean} True if all cells are empty
   */
  isEmpty() {
    for (let row = 0; row < this.height; row++) {
      for (let col = 0; col < this.width; col++) {
        if (this.grid[row][col] !== EMPTY_CELL) {
          return false;
        }
      }
    }
    return true;
  }

  /**
   * Resets the board to an empty state.
   */
  reset() {
    this.grid = this._createEmptyGrid();
  }

  /**
   * Checks if a cell position is within the board bounds.
   * @param {number} row - Row index
   * @param {number} col - Column index
   * @returns {boolean} True if position is within bounds
   */
  isValidPosition(row, col) {
    return row >= 0 && row < this.height && col >= 0 && col < this.width;
  }

  /**
   * Checks if a cell is empty at the specified position.
   * @param {number} row - Row index
   * @param {number} col - Column index
   * @returns {boolean} True if cell is empty or out of bounds (top only)
   */
  isCellEmpty(row, col) {
    if (row < 0) {
      return true; // Above the board is considered empty
    }
    if (!this.isValidPosition(row, col)) {
      return false; // Out of bounds (sides/bottom) is not empty
    }
    return this.grid[row][col] === EMPTY_CELL;
  }

  /**
   * Renders the game board to a canvas context.
   * Draws the background, grid lines, and any placed pieces.
   * @param {CanvasRenderingContext2D} ctx - Canvas rendering context
   * @param {number} offsetX - X offset for rendering (default: 0)
   * @param {number} offsetY - Y offset for rendering (default: 0)
   */
  render(ctx, offsetX = 0, offsetY = 0) {
    const width = this.getPixelWidth();
    const height = this.getPixelHeight();

    // Clear the board area
    ctx.clearRect(offsetX, offsetY, width, height);

    // Draw background
    ctx.fillStyle = BACKGROUND_COLOR;
    ctx.fillRect(offsetX, offsetY, width, height);

    // Draw cells
    for (let row = 0; row < this.height; row++) {
      for (let col = 0; col < this.width; col++) {
        const cellValue = this.grid[row][col];
        const x = offsetX + col * this.cellSize;
        const y = offsetY + row * this.cellSize;

        if (cellValue !== EMPTY_CELL) {
          // Draw filled cell (piece)
          ctx.fillStyle = this._getCellColor(cellValue);
          ctx.fillRect(x + 1, y + 1, this.cellSize - 2, this.cellSize - 2);
        }
      }
    }

    // Draw grid lines for clear boundaries
    ctx.strokeStyle = GRID_LINE_COLOR;
    ctx.beginPath();

    // Vertical lines
    for (let col = 0; col <= this.width; col++) {
      const x = offsetX + col * this.cellSize;
      ctx.moveTo(x, offsetY);
      ctx.lineTo(x, offsetY + height);
    }

    // Horizontal lines
    for (let row = 0; row <= this.height; row++) {
      const y = offsetY + row * this.cellSize;
      ctx.moveTo(offsetX, y);
      ctx.lineTo(offsetX + width, y);
    }

    ctx.stroke();

    // Draw border
    ctx.strokeStyle = BORDER_COLOR;
    ctx.strokeRect(offsetX, offsetY, width, height);
  }

  /**
   * Gets the color for a cell value (tetromino type).
   * @param {number} value - Cell value (1-7 for different pieces)
   * @returns {string} CSS color string
   * @private
   */
  _getCellColor(value) {
    const colors = {
      1: '#00FFFF', // I - Cyan
      2: '#FFFF00', // O - Yellow
      3: '#800080', // T - Purple
      4: '#00FF00', // S - Green
      5: '#FF0000', // Z - Red
      6: '#0000FF', // J - Blue
      7: '#FFA500'  // L - Orange
    };
    return colors[value] || '#FFFFFF';
  }
}

module.exports = {
  GameBoard,
  BOARD_WIDTH,
  BOARD_HEIGHT,
  EMPTY_CELL,
  DEFAULT_CELL_SIZE
};
