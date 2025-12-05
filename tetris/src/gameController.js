/**
 * GameController - Tetris Game Controller Implementation
 *
 * This module implements the game controller for Tetris, managing:
 * - Piece movement and positioning
 * - Drop mechanics (normal drop, soft drop per REQ-6)
 * - Input handling for keyboard controls
 * - Game timing and speed
 */

const { GameBoard, BOARD_WIDTH, BOARD_HEIGHT, EMPTY_CELL } = require('./gameBoard');
const { createTetromino, generateRandomTetromino, TETROMINO_TYPES } = require('./tetromino');

// Drop speed constants (in milliseconds)
const NORMAL_DROP_INTERVAL = 1000; // 1 second per row at level 1
const SOFT_DROP_INTERVAL = 50;     // 50ms per row when soft dropping (20x faster)
const LEVEL_SPEED_MULTIPLIER = 0.85; // Each level is 15% faster

// Color value mapping for tetrominoes
const TETROMINO_COLOR_VALUES = {
  'I': 1,
  'O': 2,
  'T': 3,
  'S': 4,
  'Z': 5,
  'J': 6,
  'L': 7
};

/**
 * Represents an active piece on the board with position and rotation state
 */
class ActivePiece {
  /**
   * Creates a new active piece
   * @param {Tetromino} tetromino - The tetromino instance
   * @param {number} row - Starting row position
   * @param {number} col - Starting column position
   */
  constructor(tetromino, row = 0, col = 3) {
    this.tetromino = tetromino;
    this.row = row;
    this.col = col;
    this.rotation = 0;
  }

  /**
   * Gets the absolute board positions of all cells in this piece
   * @returns {Array<{row: number, col: number}>} Array of cell positions
   */
  getBoardPositions() {
    const cells = this.tetromino.getCells();
    return cells.map(([cellRow, cellCol]) => ({
      row: this.row + cellRow,
      col: this.col + cellCol
    }));
  }

  /**
   * Gets the color value for this piece type
   * @returns {number} Color value (1-7)
   */
  getColorValue() {
    return TETROMINO_COLOR_VALUES[this.tetromino.getType()];
  }
}

/**
 * GameController class manages the Tetris game state and logic
 */
class GameController {
  /**
   * Creates a new GameController instance
   * @param {GameBoard} board - Optional existing game board
   */
  constructor(board = null) {
    this.board = board || new GameBoard();
    this.activePiece = null;
    this.nextPiece = null;
    this.score = 0;
    this.level = 1;
    this.linesCleared = 0;
    this.gameState = 'idle'; // 'idle', 'playing', 'paused', 'gameover'

    // Drop state
    this.softDropActive = false;
    this.lastDropTime = 0;
    this.dropInterval = NORMAL_DROP_INTERVAL;

    // Input state tracking
    this.inputState = {
      left: false,
      right: false,
      down: false,     // Soft drop (Down Arrow)
      softDrop: false, // Alternative soft drop (S key)
      rotate: false,
      hardDrop: false
    };

    // Bind event handlers
    this._handleKeyDown = this._handleKeyDown.bind(this);
    this._handleKeyUp = this._handleKeyUp.bind(this);
  }

  /**
   * Gets the current drop interval based on soft drop state and level
   * @returns {number} Drop interval in milliseconds
   */
  getDropInterval() {
    const baseInterval = this.softDropActive ? SOFT_DROP_INTERVAL : NORMAL_DROP_INTERVAL;
    // Apply level speed multiplier
    return baseInterval * Math.pow(LEVEL_SPEED_MULTIPLIER, this.level - 1);
  }

  /**
   * Gets the normal drop interval (without soft drop)
   * @returns {number} Normal drop interval in milliseconds
   */
  getNormalDropInterval() {
    return NORMAL_DROP_INTERVAL * Math.pow(LEVEL_SPEED_MULTIPLIER, this.level - 1);
  }

  /**
   * Gets the soft drop interval
   * @returns {number} Soft drop interval in milliseconds
   */
  getSoftDropInterval() {
    return SOFT_DROP_INTERVAL;
  }

  /**
   * Checks if soft drop is currently active
   * @returns {boolean} True if soft dropping
   */
  isSoftDropActive() {
    return this.softDropActive;
  }

  /**
   * Activates soft drop mode (piece falls faster)
   * Per REQ-6: Allow player to accelerate tetromino descent
   */
  activateSoftDrop() {
    if (!this.softDropActive) {
      this.softDropActive = true;
      this.dropInterval = this.getSoftDropInterval();
    }
  }

  /**
   * Deactivates soft drop mode (piece returns to normal speed)
   */
  deactivateSoftDrop() {
    if (this.softDropActive) {
      this.softDropActive = false;
      this.dropInterval = this.getNormalDropInterval();
    }
  }

  /**
   * Spawns a new piece at the top of the board
   * @returns {boolean} True if piece was spawned successfully
   */
  spawnPiece() {
    const tetromino = this.nextPiece || generateRandomTetromino();
    this.nextPiece = generateRandomTetromino();

    // Spawn at top center (row 0, col 3 for most pieces)
    const startCol = Math.floor((BOARD_WIDTH - 4) / 2);
    this.activePiece = new ActivePiece(tetromino, 0, startCol);

    // Check if spawn position is valid (game over check)
    if (!this._isValidPosition(this.activePiece)) {
      this.gameState = 'gameover';
      return false;
    }

    return true;
  }

  /**
   * Checks if a piece position is valid (within bounds and not colliding)
   * @param {ActivePiece} piece - The piece to check
   * @returns {boolean} True if position is valid
   */
  _isValidPosition(piece) {
    const positions = piece.getBoardPositions();
    for (const pos of positions) {
      // Check bounds
      if (pos.col < 0 || pos.col >= BOARD_WIDTH) {
        return false;
      }
      if (pos.row >= BOARD_HEIGHT) {
        return false;
      }
      // Skip cells above the board (can spawn above)
      if (pos.row < 0) {
        continue;
      }
      // Check collision with placed pieces
      if (!this.board.isCellEmpty(pos.row, pos.col)) {
        return false;
      }
    }
    return true;
  }

  /**
   * Moves the active piece down by one row
   * @returns {boolean} True if piece moved, false if it landed
   */
  moveDown() {
    if (!this.activePiece || this.gameState !== 'playing') {
      return false;
    }

    // Try moving down
    this.activePiece.row++;

    if (!this._isValidPosition(this.activePiece)) {
      // Revert and lock piece
      this.activePiece.row--;
      this._lockPiece();
      return false;
    }

    return true;
  }

  /**
   * Moves the active piece left
   * @returns {boolean} True if piece moved
   */
  moveLeft() {
    if (!this.activePiece || this.gameState !== 'playing') {
      return false;
    }

    this.activePiece.col--;
    if (!this._isValidPosition(this.activePiece)) {
      this.activePiece.col++;
      return false;
    }
    return true;
  }

  /**
   * Moves the active piece right
   * @returns {boolean} True if piece moved
   */
  moveRight() {
    if (!this.activePiece || this.gameState !== 'playing') {
      return false;
    }

    this.activePiece.col++;
    if (!this._isValidPosition(this.activePiece)) {
      this.activePiece.col--;
      return false;
    }
    return true;
  }

  /**
   * Locks the current piece in place on the board
   * @private
   */
  _lockPiece() {
    if (!this.activePiece) return;

    const positions = this.activePiece.getBoardPositions();
    const colorValue = this.activePiece.getColorValue();

    for (const pos of positions) {
      if (pos.row >= 0 && pos.row < BOARD_HEIGHT) {
        this.board.setCellAt(pos.row, pos.col, colorValue);
      }
    }

    // Clear completed lines
    this._clearLines();

    // Spawn next piece
    this.activePiece = null;
    this.spawnPiece();
  }

  /**
   * Clears completed lines and updates score
   * @private
   */
  _clearLines() {
    let linesCleared = 0;
    const grid = this.board.getGrid();

    for (let row = BOARD_HEIGHT - 1; row >= 0; row--) {
      const isComplete = grid[row].every(cell => cell !== EMPTY_CELL);
      if (isComplete) {
        // Remove the line and add empty line at top
        for (let r = row; r > 0; r--) {
          for (let col = 0; col < BOARD_WIDTH; col++) {
            this.board.setCellAt(r, col, this.board.getCellAt(r - 1, col));
          }
        }
        // Clear top row
        for (let col = 0; col < BOARD_WIDTH; col++) {
          this.board.setCellAt(0, col, EMPTY_CELL);
        }
        linesCleared++;
        row++; // Check the same row again
      }
    }

    if (linesCleared > 0) {
      this.linesCleared += linesCleared;
      this._updateScore(linesCleared);
      this._checkLevelUp();
    }
  }

  /**
   * Updates score based on lines cleared
   * @param {number} lines - Number of lines cleared
   * @private
   */
  _updateScore(lines) {
    const pointsTable = { 1: 100, 2: 300, 3: 500, 4: 800 };
    this.score += (pointsTable[lines] || 0) * this.level;
  }

  /**
   * Checks if level should increase
   * @private
   */
  _checkLevelUp() {
    const newLevel = Math.floor(this.linesCleared / 10) + 1;
    if (newLevel > this.level) {
      this.level = newLevel;
      // Update drop interval for new level (unless soft dropping)
      if (!this.softDropActive) {
        this.dropInterval = this.getNormalDropInterval();
      }
    }
  }

  /**
   * Starts a new game
   */
  startGame() {
    this.board.reset();
    this.score = 0;
    this.level = 1;
    this.linesCleared = 0;
    this.gameState = 'playing';
    this.softDropActive = false;
    this.dropInterval = this.getNormalDropInterval();
    this.lastDropTime = Date.now();
    this.nextPiece = generateRandomTetromino();
    this.spawnPiece();
  }

  /**
   * Updates the game state (call this in game loop)
   * @param {number} currentTime - Current timestamp
   */
  update(currentTime) {
    if (this.gameState !== 'playing' || !this.activePiece) {
      return;
    }

    const elapsed = currentTime - this.lastDropTime;
    if (elapsed >= this.dropInterval) {
      this.moveDown();
      this.lastDropTime = currentTime;
    }
  }

  /**
   * Handles keydown events for game controls
   * @param {KeyboardEvent} event - The keyboard event
   * @private
   */
  _handleKeyDown(event) {
    if (this.gameState !== 'playing') return;

    switch (event.key) {
      case 'ArrowDown':
        // Soft drop via Down Arrow - REQ-6
        event.preventDefault();
        this.activateSoftDrop();
        this.inputState.down = true;
        break;
      case 's':
      case 'S':
        // Soft drop via S key - REQ-6 alternative control
        event.preventDefault();
        this.activateSoftDrop();
        this.inputState.softDrop = true;
        break;
      case 'ArrowLeft':
      case 'a':
      case 'A':
        event.preventDefault();
        this.inputState.left = true;
        this.moveLeft();
        break;
      case 'ArrowRight':
      case 'd':
      case 'D':
        event.preventDefault();
        this.inputState.right = true;
        this.moveRight();
        break;
      case 'ArrowUp':
      case 'w':
      case 'W':
        event.preventDefault();
        this.inputState.rotate = true;
        // Rotation would be implemented here
        break;
      case ' ':
        event.preventDefault();
        this.inputState.hardDrop = true;
        // Hard drop would be implemented here
        break;
    }
  }

  /**
   * Handles keyup events for game controls
   * @param {KeyboardEvent} event - The keyboard event
   * @private
   */
  _handleKeyUp(event) {
    switch (event.key) {
      case 'ArrowDown':
        this.inputState.down = false;
        // Only deactivate if S key is also not pressed
        if (!this.inputState.softDrop) {
          this.deactivateSoftDrop();
        }
        break;
      case 's':
      case 'S':
        this.inputState.softDrop = false;
        // Only deactivate if Down Arrow is also not pressed
        if (!this.inputState.down) {
          this.deactivateSoftDrop();
        }
        break;
      case 'ArrowLeft':
      case 'a':
      case 'A':
        this.inputState.left = false;
        break;
      case 'ArrowRight':
      case 'd':
      case 'D':
        this.inputState.right = false;
        break;
      case 'ArrowUp':
      case 'w':
      case 'W':
        this.inputState.rotate = false;
        break;
      case ' ':
        this.inputState.hardDrop = false;
        break;
    }
  }

  /**
   * Enables keyboard input handling
   * @param {Document|Window} target - The event target (default: document in browser)
   */
  enableInput(target) {
    if (target && typeof target.addEventListener === 'function') {
      target.addEventListener('keydown', this._handleKeyDown);
      target.addEventListener('keyup', this._handleKeyUp);
    }
  }

  /**
   * Disables keyboard input handling
   * @param {Document|Window} target - The event target
   */
  disableInput(target) {
    if (target && typeof target.removeEventListener === 'function') {
      target.removeEventListener('keydown', this._handleKeyDown);
      target.removeEventListener('keyup', this._handleKeyUp);
    }
  }

  /**
   * Gets the current game state
   * @returns {string} Current game state
   */
  getGameState() {
    return this.gameState;
  }

  /**
   * Gets the active piece
   * @returns {ActivePiece|null} The active piece or null
   */
  getActivePiece() {
    return this.activePiece;
  }

  /**
   * Gets the current score
   * @returns {number} Current score
   */
  getScore() {
    return this.score;
  }

  /**
   * Gets the current level
   * @returns {number} Current level
   */
  getLevel() {
    return this.level;
  }

  /**
   * Gets the number of lines cleared
   * @returns {number} Lines cleared
   */
  getLinesCleared() {
    return this.linesCleared;
  }
}

module.exports = {
  GameController,
  ActivePiece,
  NORMAL_DROP_INTERVAL,
  SOFT_DROP_INTERVAL,
  LEVEL_SPEED_MULTIPLIER,
  TETROMINO_COLOR_VALUES
};
